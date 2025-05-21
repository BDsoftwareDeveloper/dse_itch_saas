from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
from app.db.config import settings

DATABASE_URL = settings.SQLALCHEMY_DATABASE_URI

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Default DB Session for public schema."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def get_tenant_db(schema_name: str) -> Session:
    """Context manager that sets PostgreSQL search_path per tenant."""
    db = SessionLocal()
    try:
        db.execute(f'SET search_path TO {schema_name}, public')
        yield db
    finally:
        db.close()
