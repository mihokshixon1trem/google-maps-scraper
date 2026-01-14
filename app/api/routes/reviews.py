from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_authed_db
from app.services.review_service import ReviewService
from app.services.job_service import JobService

router = APIRouter(prefix="/reviews", tags=["reviews"])
reviews = ReviewService()
jobs = JobService()


@router.get("")
def list_reviews(job_id: str, place_id: str, limit: int = 50, offset: int = 0, db: Session = Depends(get_authed_db)):
    job = jobs.get(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    items = reviews.list_by_place(db, job_id=job_id, place_id=place_id, limit=min(limit, 200), offset=max(offset, 0))
    return [
        {
            "place_id": r.place_id,
            "author_name": r.author_name,
            "rating": r.rating,
            "text": r.text,
            "relative_time_description": r.relative_time_description,
            "language": r.language,
        }
        for r in items
    ]
