from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.database import SessionLocal
from app.models import BandSubmission
from app import crud
import csv
from io import StringIO

router = APIRouter()

@router.post("/submit-form/")
def submit_form(...):
    ...

@router.post("/submit-csv/")
async def submit_csv(file: UploadFile = File(...)):
    contents = await file.read()
    decoded = contents.decode("utf-8")
    reader = csv.DictReader(StringIO(decoded))

    db = SessionLocal()
    added = 0

    try:
        for row in reader:
            name = row.get("name")
            if not name:
                continue

            last_album_year = row.get("last_album_year")
            try:
                last_album_year = int(last_album_year) if last_album_year else None
            except ValueError:
                last_album_year = None

            submission = BandSubmission(
                name=name,
                active=row.get("active", "true").lower() == "true",
                last_album_title=row.get("last_album_title"),
                last_album_year=last_album_year,
            )

            db.add(submission)
            added += 1

        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()

    return {"status": "success", "message": f"{added} submissions received for review."}





