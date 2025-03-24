from fastapi import APIRouter, UploadFile, File, Form
from . import photo_folder
from db.models import (get_all_meters, add_photo, get_photos_by_meter, get_last_photo_by_meter, get_reading)
import os
import uuid
import aiofiles
from datetime import datetime

router = APIRouter()
UPLOAD_FOLDER = photo_folder

@router.get("/list_meters/")
async def list_meters():
    meters = get_all_meters()
    return [{"meter_id": meter["meter_id"], "description": meter["description"], "location": meter["location"]} for meter in meters]


@router.post("/upload_photo/")
async def upload_photo(meter_uuid: str = Form(...), file: UploadFile = File(...)):
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    photo_uuid = str(uuid.uuid4())

    file_name = f"{meter_uuid}_{photo_uuid}.jpg"

    current_date = datetime.now()
    date_folder = current_date.strftime("%Y-%m-%d")
    folder_path = os.path.join(UPLOAD_FOLDER, date_folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


    file_path = os.path.join(folder_path, file_name)
    async with aiofiles.open(file_path, "wb") as buffer:
        while chunk := await file.read(4096):  
            await buffer.write(chunk)
        
    add_photo(photo_uuid, meter_uuid, file_path)
    return  {"message": "Photo added", "photo_path": file_path}

@router.get("/photos/{meter_uuid}")
async def list_photos(meter_uuid):
    photos = get_photos_by_meter(meter_uuid)
    return [{"photo_id": photo["photo_id"], "photo_path": photo["photo_path"], "date": photo["date"]} for photo in photos]

@router.get("/last_photo/{meter_uuid}")
async def last_photo(meter_uuid):
    photo = get_last_photo_by_meter(meter_uuid)
    return {"photo_id": photo["photo_id"], "photo_path": photo["photo_path"], "date": photo["date"]}

@router.get("/reading/{photo_id}")
async def get_photo_reading(photo_id: str):
    reading = get_reading(photo_id)
    if reading:
        return {
            "photo_id": reading["photo_id"],
            "meter_uuid": reading["meter_uuid"],
            "reading_value": reading["reading_value"],
            "date": reading["date"]
        }
    return {"error": "Reading not found"}