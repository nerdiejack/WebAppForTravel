from fastapi import APIRouter, HTTPException, UploadFile, File
from models import DiaryEntry
from database import db
from datetime import datetime
from typing import List
from bson import ObjectId
import os
import uuid

router = APIRouter(prefix="/api")

@router.post("/diary/entries/", response_model=DiaryEntry)
async def create_diary_entry(entry: DiaryEntry):
    entry_dict = entry.dict(exclude={'_id'})
    entry_dict["created_at"] = datetime.utcnow()
    entry_dict["updated_at"] = datetime.utcnow()
    
    result = await db.diary_entries.insert_one(entry_dict)
    created_entry = await db.diary_entries.find_one({"_id": result.inserted_id})
    created_entry["_id"] = str(created_entry["_id"])
    return created_entry

@router.put("/diary/entries/{entry_id}", response_model=DiaryEntry)
async def update_diary_entry(entry_id: str, entry: DiaryEntry):
    try:
        # Exclude _id from update and set updated_at
        update_data = entry.dict(exclude={'_id'})
        update_data["updated_at"] = datetime.utcnow()
        
        # Update the entry
        result = await db.diary_entries.update_one(
            {"_id": ObjectId(entry_id)},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Diary entry not found")
        
        # Get and return the updated entry
        updated_entry = await db.diary_entries.find_one({"_id": ObjectId(entry_id)})
        if updated_entry:
            updated_entry["_id"] = str(updated_entry["_id"])
            return updated_entry
            
        raise HTTPException(status_code=404, detail="Diary entry not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/diary/entries/", response_model=List[DiaryEntry])
async def get_diary_entries():
    entries = []
    cursor = db.diary_entries.find()
    async for entry in cursor:
        entry["_id"] = str(entry["_id"])
        entries.append(entry)
    return entries

@router.get("/diary/entries/{entry_id}", response_model=DiaryEntry)
async def get_diary_entry(entry_id: str):
    try:
        entry = await db.diary_entries.find_one({"_id": ObjectId(entry_id)})
        if entry:
            entry["_id"] = str(entry["_id"])
            return entry
        raise HTTPException(status_code=404, detail="Diary entry not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/diary/entries/{entry_id}")
async def delete_diary_entry(entry_id: str):
    try:
        result = await db.diary_entries.delete_one({"_id": ObjectId(entry_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Diary entry not found")
        return {"message": "Diary entry deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/diary/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Create uploads directory if it doesn't exist
        os.makedirs("uploads", exist_ok=True)
        
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = f"uploads/{unique_filename}"
        
        # Save file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Return the URL
        return {"url": f"/uploads/{unique_filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 