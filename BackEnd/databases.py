from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:!Abd0!0138415047@localhost:5432/SentiVue'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

class user(Base):
    __tablename__ = 'users'
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

class transcript(Base):
    __tablename__ = 'transcripts'
    
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    filename = Column(String, nullable=False)
    transcriptTxt = Column(String, nullable=False)
    sentiment_score = Column(Float, nullable=True)
    sentiment_label = Column(String, nullable=True)
    speaker_count = Column(Integer, default=1)
    duration = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)