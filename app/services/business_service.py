from __future__ import annotations

from sqlalchemy.orm import Session
from app.models.business import Business


class BusinessService:
    def upsert(self, db: Session, *, job_id: str, record: dict) -> Business:
        place_id = record["place_id"]
        item = db.query(Business).filter(Business.job_id == job_id, Business.place_id == place_id).first()
        if not item:
            item = Business(job_id=job_id, place_id=place_id, name=record.get("name", ""))
            db.add(item)

        item.name = record.get("name", item.name)
        item.primary_category = record.get("primary_category", "")
        item.categories = ",".join(record.get("categories", [])) if isinstance(record.get("categories"), list) else (record.get("categories") or "")
        item.rating = record.get("rating")
        item.reviews_count = record.get("reviews_count")

        item.formatted_address = record.get("formatted_address", "")
        loc = record.get("location") or {}
        item.lat = loc.get("lat")
        item.lng = loc.get("lng")

        item.phone = record.get("phone", "")
        item.website = record.get("website", "")
        item.google_maps_url = record.get("google_maps_url", "")

        db.commit()
        db.refresh(item)
        return item

    def list_by_job(self, db: Session, *, job_id: str, limit: int = 200, offset: int = 0) -> list[Business]:
        return (
            db.query(Business)
            .filter(Business.job_id == job_id)
            .order_by(Business.id.asc())
            .offset(offset)
            .limit(limit)
            .all()
        )
