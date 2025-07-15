from sqlalchemy.orm import Session
from backend.app.database import SessionLocal, engine, Base
from app.models import Band

# Recreate tables (optional but useful during development)
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

bands = [
    Band(name="Napalm Death", active=True, last_album_title="Throes of Joy in the Jaws of Defeatism", last_album_year=2020),
    Band(name="Bolt Thrower", active=False, last_album_title="Those Once Loyal", last_album_year=2005),
    Band(name="Pig Destroyer", active=True, last_album_title="Head Cage", last_album_year=2018),
    Band(name="Nasum", active=False, last_album_title="Shift", last_album_year=2004),
    Band(name="Terrorizer", active=False, last_album_title="Caustic Attack", last_album_year=2018),
    Band(name="Wormrot", active=True, last_album_title="Hiss", last_album_year=2022),
    Band(name="Full of Hell", active=True, last_album_title="Coagulated Bliss", last_album_year=2024),
    Band(name="Gridlink", active=True, last_album_title="Coronet Juniper", last_album_year=2023),
    Band(name="Brutal Truth", active=False, last_album_title="End Time", last_album_year=2011),
    Band(name="Agoraphobic Nosebleed", active=False, last_album_title="Arc EP", last_album_year=2016),
]

def seed_data():
    db: Session = SessionLocal()
    db.add_all(bands)
    db.commit()
    db.close()
    print("✅ Seeded band data.")

if __name__ == "__main__":
    seed_data()
