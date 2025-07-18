from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import BandSubmission
from io import StringIO
import csv

router = APIRouter()

@router.post("/submit-form/")
def submit_form(
    name: str = Form(...),
    active: bool = Form(...),
    last_album_title: str = Form(None),
    last_album_year: int = Form(None),
    db: Session = Depends(get_db)
):
    submission = BandSubmission(
        name=name,
        active=active,
        last_album_title=last_album_title,
        last_album_year=last_album_year
    )

    try:
        db.add(submission)
        db.commit()
        db.refresh(submission)
        return {"status": "success", "message": f"Band '{name}' submitted for review."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/submit-csv/")
async def submit_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    decoded = contents.decode("utf-8")
    reader = csv.DictReader(StringIO(decoded))

    added = 0

    try:
        for row in reader:
            name = row.get("name")
            if not name:
                continue

            try:
                year = int(row["last_album_year"]) if row.get("last_album_year") else None
            except ValueError:
                year = None

            submission = BandSubmission(
                name=name,
                active=row.get("active", "true").lower() == "true",
                last_album_title=row.get("last_album_title"),
                last_album_year=year
            )

            db.add(submission)
            added += 1

        db.commit()
        return {"status": "success", "message": f"{added} submissions received for review."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
