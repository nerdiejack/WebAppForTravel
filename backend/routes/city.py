from fastapi import APIRouter, HTTPException
from database import db
from models import City

router = APIRouter()

@router.post("/city/")
async def add_city(city: City):
    """Add a new city to the database"""
    existing_city = await db.cities.find_one({"name": city.name})
    if existing_city:
        raise HTTPException(status_code=400, detail="City already exists")

    await db.cities.insert_one(city.dict())
    return {"message": "City added successfully"}

@router.get("/city/{name}")
async def get_city(name: str):
    """Get information about a specific city"""
    city = await db.cities.find_one({"name": name}, {"_id": 0})
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city
