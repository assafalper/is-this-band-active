from sqlalchemy.orm import Session
from backend.app import models

def get_band_by_name(db: Session, name: str):
    return db.query(models.Band).filter(models.Band.name.ilike(name)).first()

