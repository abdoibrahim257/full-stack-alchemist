from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

import os
from dotenv import load_dotenv

load_dotenv()


SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

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
    
    id = Column(UUID(as_uuid=True), primary_key=True)
    fileHash = Column(String(length=64), nullable=False, unique=True)
    filename = Column(String, nullable=False)
    transcriptTxt = Column(String, nullable=False)
    language = Column(String, nullable=True)