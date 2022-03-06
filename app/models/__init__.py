from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings


_db_url = f"postgresql://{settings.postgres_user}:{settings.postgres_password}" \
          f"@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_database}"

engine = create_engine(_db_url)
Base = declarative_base()


def get_db():
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(e)
        db.close()
