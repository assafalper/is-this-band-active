from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies.auth import verify_admin
from app.models import Band, BandSubmission


router = APIRouter()

@router.get("/admin/review/", dependencies=[Depends(verify_admin)])
def list_submissions(db: Session = Depends(get_db)):
    return db.query(BandSubmission).all()

@router.post("/admin/review/{submission_id}/approve", dependencies=[Depends(verify_admin)])
def approve_submission(submission_id: int, db: Session = Depends(get_db)):
    submission = db.query(BandSubmission).filter(BandSubmission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    band = Band(
        name=submission.name,
        active=submission.active,
        last_album_title=submission.last_album_title,
        last_album_year=submission.last_album_year
    )

    try:
        db.add(band)
        db.delete(submission)
        db.commit()
        return {"status": "approved", "band_id": band.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/admin/review/{submission_id}/reject", dependencies=[Depends(verify_admin)])
def reject_submission(submission_id: int, db: Session = Depends(get_db)):
    submission = db.query(BandSubmission).filter(BandSubmission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    db.delete(submission)
    db.commit()
    return {"status": "rejected"}
