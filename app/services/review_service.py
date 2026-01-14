from __future__ import annotations

from sqlalchemy.orm import Session
from app.models.review import Review


class ReviewService:
    def replace_for_place(self, db: Session, *, job_id: str, place_id: str, reviews: list[dict]) -> int:
        db.query(Review).filter(Review.job_id == job_id, Review.place_id == place_id).delete()
        for r in reviews:
            item = Review(
                job_id=job_id,
                place_id=place_id,
                author_name=r.get("author_name", ""),
                rating=r.get("rating"),
                text=r.get("text", ""),
                relative_time_description=r.get("relative_time_description", ""),
                language=r.get("language", ""),
            )
            db.add(item)
        db.commit()
        return len(reviews)

    def list_by_place(self, db: Session, *, job_id: str, place_id: str, limit: int = 50, offset: int = 0) -> list[Review]:
        return (
            db.query(Review)
            .filter(Review.job_id == job_id, Review.place_id == place_id)
            .order_by(Review.id.asc())
            .offset(offset)
            .limit(limit)
            .all()
        )
