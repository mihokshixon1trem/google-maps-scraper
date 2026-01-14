from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.api.deps import get_authed_db
from app.services.export_service import ExportService
from app.services.job_service import JobService

router = APIRouter(prefix="/exports", tags=["exports"])
exports = ExportService()
jobs = JobService()


@router.get("/json")
def export_json(job_id: str, db: Session = Depends(get_authed_db)):
    job = jobs.get(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    data = exports.export_json(db, job_id=job_id)
    return Response(content=data, media_type="application/json")


@router.get("/csv")
def export_csv(job_id: str, db: Session = Depends(get_authed_db)):
    job = jobs.get(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    data = exports.export_csv(db, job_id=job_id)
    return Response(content=data, media_type="text/csv")
