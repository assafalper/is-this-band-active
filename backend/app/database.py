import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
  engine = create_engine(DATABASE_URL)
else:
    raise Exception('missing DATABASE URL')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
