from sqlalchemy import Column, Integer, String, Boolean
from backend.app.database import Base

class Band(Base):
    __tablename__ = "bands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    active = Column(Boolean, default=True)
    last_album_title = Column(String)
    last_album_year = Column(Integer)