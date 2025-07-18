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
from fastapi.middleware.cors import CORSMiddleware
from app.routers.upload import router as upload_router
from app.routers.band_admin import router as admin_router

app = FastAPI()

app.include_router(upload_router)
app.include_router(admin_router)

Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="app/templates")

app.mount("/assets", StaticFiles(directory="app/dist/assets"), name="assets")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://isthisbandactive.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/band/{band_name}", response_model=schema.Band)
def get_band(band_name: str, db: Session = Depends(get_db)):
    band = crud.get_band_by_name(db, band_name)
    if not band:
        raise HTTPException(status_code=404, detail="Band not found")
    return band

# Final fallback: serve React app for all other frontend routes
@app.get("/{full_path:path}", response_class=FileResponse)
def serve_react_app(request: Request):
    return FileResponse("app/dist/index.html")

