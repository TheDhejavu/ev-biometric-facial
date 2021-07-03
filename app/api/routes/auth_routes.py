from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from app.core.facial_recognition import FacialRecognition
from typing import List
from app.common.logger import logger
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
    if result == "unknown":
        raise HTTPException(
            status_code=401, detail="Invalid facial identity")

    return {"tmp_file_path": tmp_file_path, "result": result}


@router.post("/register/")
def register_faces(user_id: str = Form(...), files: List[UploadFile] = File(...)):
    try:
        cwd = os.getcwd()
        for image in files:

            directory = os.path.join(cwd, "dataset", user_id)
            os.makedirs(directory, exist_ok=True)

            ext = image.filename.split('.')[-1]
            tmp_file_path = f"{directory}/{str(uuid.uuid4())}.{ext}"
            with open(tmp_file_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
        return {
            "filenames": [file.filename for file in files],
            "message": "registered successfully"
        }
    except Exception:
        raise HTTPException(
            status_code=500, detail="Failed to register facial images")
