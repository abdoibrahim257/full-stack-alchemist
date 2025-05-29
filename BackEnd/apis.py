from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import Depends

from databases import *
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class UserCreate(BaseModel):
    name: str
    age: int

class UserOut(BaseModel):
    id: uuid.UUID
    name: str
    age: int

    class Config:
        from_attributes = True
        
        
Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/submit")
async def insert_ussser(user_in: UserCreate, db: Session = Depends(get_db)):
    userID = uuid.uuid4()
    new_user = user(id=userID, name=user_in.name, age=user_in.age)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully", "user_id": str(userID)}