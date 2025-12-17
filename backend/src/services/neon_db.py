from sqlalchemy import create_engine, Column, String, Text, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

_engine = None
_SessionLocal = None

def get_engine():
    global _engine
    if _engine is None:
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL environment variable is not set.")
        _engine = create_engine(database_url)
    return _engine

def get_session_local():
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    return _SessionLocal

# Declare a Base for declarative models
Base = declarative_base()

# Define the ContentChunk model
class ContentChunk(Base):
    __tablename__ = "content_chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    text_content = Column(Text, nullable=False)
    source_url = Column(String, nullable=False)
    section_title = Column(String, nullable=True)
    document_id = Column(String, nullable=False)
    chunk_order = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<ContentChunk(id='{self.id}', document_id='{self.document_id}', section_title='{self.section_title}')>"

# Create tables (if they don't exist)
def create_db_and_tables():
    Base.metadata.create_all(get_engine())

# Dependency to get the DB session
def get_db():
    db = get_session_local()()
    try:
        yield db
    finally:
        db.close()

