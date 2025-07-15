import csv
from io import StringIO

from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app import schema, crud
from app.database import SessionLocal, engine, Base
from app.models import BandSubmission
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="app/templates")

app = FastAPI()

# Serve static files (JS, CSS, etc.)
app.mount("/assets", StaticFiles(directory="app/dist/assets"), name="assets")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Serve index.html at root
@app.get("/")
def serve_index():
    return FileResponse("app/dist/index.html")

@app.get("/band/{band_name}", response_model=schema.Band)
def get_band(band_name: str, db: Session = Depends(get_db)):
    band = crud.get_band_by_name(db, band_name)
    if not band:
        raise HTTPException(status_code=404, detail="Band not found")
    return band

@app.get("/submit", response_class=HTMLResponse)
def show_submission_form(request: Request):
    return templates.TemplateResponse("submit_form.html", {"request": request})

@app.post("/submit-csv/")
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





