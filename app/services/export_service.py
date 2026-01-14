from __future__ import annotations

import csv
import io
import json
from sqlalchemy.orm import Session

from app.models.business import Business
from app.models.review import Review


class ExportService:
    def export_json(self, db: Session, *, job_id: str) -> bytes:
        businesses = db.query(Business).filter(Business.job_id == job_id).order_by(Business.id.asc()).all()
        reviews = db.query(Review).filter(Review.job_id == job_id).order_by(Review.id.asc()).all()

        out = {
            "job_id": job_id,
            "businesses": [
                {
                    "place_id": b.place_id,
                    "name": b.name,
                    "primary_category": b.primary_category,
                    "categories": [c for c in (b.categories or "").split(",") if c],
                    "rating": b.rating,
                    "reviews_count": b.reviews_count,
                    "formatted_address": b.formatted_address,
                    "location": {"lat": b.lat, "lng": b.lng},
                    "phone": b.phone,
                    "website": b.website,
                    "google_maps_url": b.google_maps_url,
                }
                for b in businesses
            ],
            "reviews": [
                {
                    "place_id": r.place_id,
                    "author_name": r.author_name,
                    "rating": r.rating,
                    "text": r.text,
                    "relative_time_description": r.relative_time_description,
                    "language": r.language,
                }
                for r in reviews
            ],
        }
        return json.dumps(out, ensure_ascii=False, indent=2).encode("utf-8")

    def export_csv(self, db: Session, *, job_id: str) -> bytes:
        businesses = db.query(Business).filter(Business.job_id == job_id).order_by(Business.id.asc()).all()
        buf = io.StringIO()
        writer = csv.DictWriter(
            buf,
            fieldnames=[
                "place_id",
                "name",
                "primary_category",
                "categories",
                "rating",
                "reviews_count",
                "formatted_address",
                "lat",
                "lng",
                "phone",
                "website",
                "google_maps_url",
            ],
        )
        writer.writeheader()
        for b in businesses:
            writer.writerow(
                {
                    "place_id": b.place_id,
                    "name": b.name,
                    "primary_category": b.primary_category,
                    "categories": b.categories,
                    "rating": b.rating,
                    "reviews_count": b.reviews_count,
                    "formatted_address": b.formatted_address,
                    "lat": b.lat,
                    "lng": b.lng,
                    "phone": b.phone,
                    "website": b.website,
                    "google_maps_url": b.google_maps_url,
                }
            )
        return buf.getvalue().encode("utf-8")
