from __future__ import annotations

import asyncio
import logging
import time
import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.job import Job, JobStatus
from app.services.places_client import PlacesClient
from app.services.business_service import BusinessService
from app.services.review_service import ReviewService
from app.utils.validation import clamp_int

logger = logging.getLogger(__name__)

# In-process task registry. For multi-worker setups, swap to a real queue.
TASKS: dict[str, asyncio.Task] = {}


def new_job_id() -> str:
    return "job_" + uuid.uuid4().hex


class JobService:
    def __init__(self):
        self.places = PlacesClient()
        self.businesses = BusinessService()
        self.reviews = ReviewService()

    def create_job(
        self,
        db: Session,
        *,
        query: str,
        location: str,
        max_results: int | None,
        max_pages: int | None,
    ) -> Job:
        job_id = new_job_id()
        max_results = clamp_int(max_results or settings.default_max_results, 1, 500)
        max_pages = clamp_int(max_pages or settings.default_max_pages, 1, 10)

        job = Job(
            id=job_id,
            query=query.strip(),
            location=(location or "").strip(),
            status=JobStatus.queued,
            max_results=max_results,
            max_pages=max_pages,
            last_error="",
        )
        db.add(job)
        db.commit()
        db.refresh(job)
        return job

    def get(self, db: Session, job_id: str) -> Job | None:
        return db.query(Job).filter(Job.id == job_id).first()

    def start_job(self, db: Session, *, job_id: str, include_reviews: bool, language: str | None) -> None:
        job = self.get(db, job_id)
        if not job:
            raise ValueError("Job not found")
        if job.status in (JobStatus.running, JobStatus.completed):
            return

        job.status = JobStatus.running
        job.started_at = datetime.now(timezone.utc)
        db.commit()

        task = asyncio.create_task(self._run_job(job_id, include_reviews=include_reviews, language=language), name=f"job-{job_id}")
        TASKS[job_id] = task

    async def _run_job(self, job_id: str, *, include_reviews: bool, language: str | None) -> None:
        # Create an isolated DB session for this task
        from app.db.session import SessionLocal

        db = SessionLocal()
        try:
            job = self.get(db, job_id)
            if not job:
                return

            query = job.query
            # Optional: help the query if location is provided
            if job.location and job.location.lower() not in query.lower():
                query = f"{query} in {job.location}"

            fields = ",".join(
                [
                    "place_id",
                    "name",
                    "types",
                    "formatted_address",
                    "geometry/location",
                    "rating",
                    "user_ratings_total",
                    "formatted_phone_number",
                    "website",
                    "url",
                    "reviews",
                ]
            )

            results_count = 0
            page = 0
            next_token: str | None = None

            while page < job.max_pages and results_count < job.max_results:
                data = await self.places.text_search(query=query, pagetoken=next_token, language=language)
                items = data.get("results", []) or []

                # When a pagetoken is returned, Google may require a short delay before it's valid.
                next_token = data.get("next_page_token")
                page += 1

                for it in items:
                    if results_count >= job.max_results:
                        break

                    place_id = it.get("place_id")
                    if not place_id:
                        continue

                    details = await self.places.place_details(place_id=place_id, fields=fields, language=language)
                    d = (details.get("result") or {})

                    record = {
                        "place_id": d.get("place_id", place_id),
                        "name": d.get("name", it.get("name", "")),
                        "primary_category": (d.get("types") or [""])[0] if isinstance(d.get("types"), list) and d.get("types") else "",
                        "categories": d.get("types") or it.get("types") or [],
                        "rating": d.get("rating"),
                        "reviews_count": d.get("user_ratings_total"),
                        "formatted_address": d.get("formatted_address") or it.get("formatted_address") or "",
                        "location": (d.get("geometry") or {}).get("location") or (it.get("geometry") or {}).get("location") or {},
                        "phone": d.get("formatted_phone_number") or "",
                        "website": d.get("website") or "",
                        "google_maps_url": d.get("url") or "",
                    }
                    self.businesses.upsert(db, job_id=job_id, record=record)

                    if include_reviews:
                        reviews = d.get("reviews") or []
                        # Keep a small amount by default; API can return up to 5 in many configs.
                        normalized = [
                            {
                                "author_name": r.get("author_name", ""),
                                "rating": r.get("rating"),
                                "text": r.get("text", ""),
                                "relative_time_description": r.get("relative_time_description", ""),
                                "language": r.get("language", ""),
                            }
                            for r in reviews
                        ]
                        self.reviews.replace_for_place(db, job_id=job_id, place_id=record["place_id"], reviews=normalized)

                    results_count += 1

                if next_token:
                    await asyncio.sleep(2.0)  # recommended small wait before using next_page_token
                else:
                    break

            job.status = JobStatus.completed
            job.completed_at = datetime.now(timezone.utc)
            db.commit()

        except Exception as e:
            logger.exception("Job failed: %s", job_id)
            job = self.get(db, job_id)
            if job:
                job.status = JobStatus.failed
                job.last_error = str(e)
                job.completed_at = datetime.now(timezone.utc)
                db.commit()
        finally:
            db.close()
            TASKS.pop(job_id, None)
