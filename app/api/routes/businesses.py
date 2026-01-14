from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_authed_db
from app.services.business_service import BusinessService
from app.services.job_service import JobService

router = APIRouter(prefix="/businesses", tags=["businesses"])
biz = BusinessService()
jobs = JobService()


@router.get("")
def list_businesses(job_id: str, limit: int = 200, offset: int = 0, db: Session = Depends(get_authed_db)):
    job = jobs.get(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    items = biz.list_by_job(db, job_id=job_id, limit=min(limit, 500), offset=max(offset, 0))
    return [
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
        for b in items
    ]
