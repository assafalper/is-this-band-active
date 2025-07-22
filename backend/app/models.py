import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime

from app.database import Base

class Band(Base):
    __tablename__ = "bands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    active = Column(Boolean, default=True)
    last_album_title = Column(String)
    last_album_year = Column(Integer)

class BandSubmission(Base):
    __tablename__ = "band_submissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    active = Column(Boolean, default=True)
    last_album_title = Column(String)
    last_album_year = Column(Integer)
    submitted_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    reviewed = Column(Boolean, default=False)
    approved = Column(Boolean, default=False)