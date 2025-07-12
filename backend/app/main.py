from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app import models, schema, crud
from backend.app.database import SessionLocal, engine, Base
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()

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

@app.get("/band/{band_name}", response_model=schema.Band)
def get_band(band_name: str, db: Session = Depends(get_db)):
    band = crud.get_band_by_name(db, band_name)
    if not band:
        raise HTTPException(status_code=404, detail="Band not found")
    return band

@app.post("/band", )
def create_band(band: schema.Band):
    return band
