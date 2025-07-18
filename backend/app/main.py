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
from app.routers import upload, admin



app = FastAPI()
app.include_router(upload.router)
app.include_router(admin.router)
Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="app/templates")


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

