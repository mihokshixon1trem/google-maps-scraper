from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from app.api.deps import get_authed_db
from app.models.job import JobStatus
from app.services.job_service import JobService
from app.utils.validation import CreateJobRequest

router = APIRouter(prefix="/jobs", tags=["jobs"])
svc = JobService()


@router.post("", status_code=201)
def create_job(payload: CreateJobRequest, bg: BackgroundTasks, db: Session = Depends(get_authed_db)):
    job = svc.create_job(
        db,
        query=payload.query,
        location=payload.location,
        max_results=payload.max_results,
        max_pages=payload.max_pages,
    )
    # Start immediately in background (in-process). For production, swap to a queue.
    svc.start_job(db, job_id=job.id, include_reviews=payload.include_reviews, language=payload.language)
    return {
        "id": job.id,
        "query": job.query,
        "location": job.location,
        "status": job.status.value,
        "max_results": job.max_results,
        "max_pages": job.max_pages,
        "created_at": job.created_at,
    }


@router.get("/{job_id}")
def get_job(job_id: str, db: Session = Depends(get_authed_db)):
    job = svc.get(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {
        "id": job.id,
        "query": job.query,
        "location": job.location,
        "status": job.status.value,
        "max_results": job.max_results,
        "max_pages": job.max_pages,
        "created_at": job.created_at,
        "started_at": job.started_at,
        "completed_at": job.completed_at,
        "last_error": job.last_error,
    }
