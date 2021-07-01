from fastapi import APIRouter, File, UploadFile, Form
from app.core.facial_recognition import FacialRecognition
from typing import List
import uuid
import shutil
import os
ft = FacialRecognition()

router = APIRouter()


@router.post("/verify")
def verify_face(image: UploadFile = File(...)):
    ext = image.filename.split('.')[-1]
    tmp_file_path = f"/tmp/{str(uuid.uuid4())}.{ext}"
    with open(tmp_file_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    result = ft.test_images(tmp_file_path)
    return {"tmp_file_path": tmp_file_path, "result": result}


@router.post("/register/")
def register_faces(user_id: str = Form(...), files: List[UploadFile] = File(...)):

    for image in files:
        os.makedirs(f"/dataset/{user_id}")
        ext = image.filename.split('.')[-1]
        tmp_file_path = f"/tmp/{str(uuid.uuid4())}.{ext}"
        with open(tmp_file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

    return {"filenames": [file.filename for file in files]}
