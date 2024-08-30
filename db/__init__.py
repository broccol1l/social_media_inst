from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# connecting postgresql with fastapi

URL_DATABASE = 'postgresql://postgres:ramzik2006@localhost:5432/instagram'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()