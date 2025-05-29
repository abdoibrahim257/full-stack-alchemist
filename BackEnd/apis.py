from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import Depends, File, UploadFile
from pydub import AudioSegment
from fastapi.responses import FileResponse

from databases import *
import os
import requests
import time
import hashlib




app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class UserCreate(BaseModel):
    name: str
    age: int
        
class file_in(BaseModel):
    file : str
    

Base.metadata.create_all(bind=engine)

base_url = "https://api.assemblyai.com"
headers = {"authorization": "e6b18f7fa9a6481ca4cad0e90b489ea6"}

@app.get("/")
async def root():
    return {"message": "Hello World"}

# @app.post("/submit")
# async def insert_ussser(user_in: UserCreate, db: Session = Depends(get_db)):
#     userID = uuid.uuid4()
#     new_user = user(id=userID, name=user_in.name, age=user_in.age)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return {"message": "User created successfully", "user_id": str(userID)}


async def startTranscription(file_path: str):
    # Placeholder for transcription logic
    
    #uploading file to make audio publicly accessible
    with open(file_path, "rb") as f:
        response = requests.post(base_url + "/v2/upload", headers=headers, data=f)
        
    if response.status_code != 200:
        print(f"Error: {response.status_code}, Response: {response.text}")
        response.raise_for_status()
        
    upload_json = response.json()
    upload_url = upload_json["upload_url"]
    
    data = {
        "audio_url": upload_url,
        "speech_model": "slam-1"
    }
    
    response = requests.post(base_url + "/v2/transcript", headers=headers, json=data)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}, Response: {response.text}")
        response.raise_for_status()
        
    transcript_json = response.json()
    transcript_id = transcript_json["id"]
    polling_endpoint = f"{base_url}/v2/transcript/{transcript_id}"
    
    
    while True:
        transcript = requests.get(polling_endpoint, headers=headers).json()
        if transcript["status"] == "completed":
            # print(f" \nFull Transcript: \n\n{transcript['text']}")
            break
        elif transcript["status"] == "error":
            raise RuntimeError(f"Transcription failed: {transcript['error']}")
        else:
            time.sleep(2)
    
    
    srt_response = requests.get(f"{polling_endpoint}/srt?chars_per_caption=32", headers=headers)
            
    with open(f"srtFolder/transcript_{transcript_id}.srt", "w") as srt_file:
        srt_file.write(srt_response.text)
    
    return {
        "srt_file_name": f"srtFolder/transcript_{transcript_id}.srt",
        "transcript_text": transcript["text"],
        "language_code": transcript.get("language_code")
    }

# async def get_lang(file_path: str):

#     with open(file_path, "rb") as f:
#         response = requests.post(base_url + "/v2/upload", headers=headers, data=f)
        
#     if response.status_code != 200:
#         print(f"Error: {response.status_code}, Response: {response.text}")
#         response.raise_for_status()
            
#     upload_json = response.json()
#     upload_url = upload_json["upload_url"]

#     data = {
#         "audio_url": upload_url, 
#         "language_detection": True
#     }

#     url = base_url + "/v2/transcript"
#     response = requests.post(url, json=data, headers=headers)

#     transcript_id = response.json()['id']
#     polling_endpoint = base_url + "/v2/transcript/" + transcript_id

#     while True:
#         transcription_result = requests.get(polling_endpoint, headers=headers).json()

#         if transcription_result['status'] == 'completed':
#             return transcription_result['language_code']

#         elif transcription_result['status'] == 'error':
#             raise RuntimeError(f"Transcription failed: {transcription_result['error']}")

#         else:
#             time.sleep(3)

    



@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    
    os.makedirs("uploaded_files", exist_ok=True)
    
    file_path = f"uploaded_files/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(contents)
    
    
    audio_Obj = await startTranscription(file_path)
    
    # language = await get_lang(file_path)
    
    #save the transcription to the database
    
    # audioHash = get_file_hash(file_path)
    audioID = uuid.uuid4()
    
    new_transcript = transcript(
        id=audioID,
        filename=file.filename,
        transcriptTxt=audio_Obj["transcript_text"],
        language=audio_Obj["language_code"],
    )
    db.add(new_transcript)
    db.commit()
    db.refresh(new_transcript)
    
    return {
        "filename": file.filename,
        "transcription": audio_Obj["transcript_text"],
        "srt_file_name": audio_Obj["srt_file_name"],
        "language": audio_Obj["language_code"],
    }
    #save the transcription to the database
    
@app.get("/getSRT/{srt_file_name:path}")
async def get_srt_file(srt_file_name: str):
    file_path = srt_file_name
    if not os.path.exists(file_path):
        return {"error": "SRT file not found"}
    return FileResponse(
        path=file_path,
        media_type='text/plain',
        filename=os.path.basename(file_path)
    )
    
