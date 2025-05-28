from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text


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
        
        
class test(Base):
    __tablename__ = 'test'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    is_active = Column(Boolean, default=True)
        
