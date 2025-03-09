from fastapi import APIRouter, HTTPException
from database import db
from models import City

router = APIRouter()

cities_collection = db["cities"]

@router.post("/city/")
def add_city(city: City):
    """Add a new city to the database"""
    if cities_collection.find_one({"name": city.name}):
        raise HTTPException(status_code=400, detail="City already exists")

    cities_collection.insert_one(city.dict())
    return {"message": "City added successfully"}

@router.get("/city/{name}")
def get_city(name: str):
    """Get information about a specific city"""
    city = cities_collection.find_one({"name": name}, {"_id": 0})
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    return city
