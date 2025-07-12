from pydantic import BaseModel

class BandBase(BaseModel):
    name: str
    active: bool
    last_album_title: str
    last_album_year: int

class Band(BandBase):
    class Config:
        orm_mode = True