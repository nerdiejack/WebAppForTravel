from fastapi import APIRouter, HTTPException
from database import db
from models import Restaurant

router = APIRouter()

restaurants_collection = db["restaurants"]


@router.post("/restaurant/")
def add_restaurant(restaurant: Restaurant):
    """Add a new vegan restaurant to the database"""
    if restaurants_collection.find_one({"name": restaurant.name, "city": restaurant.city}):
        raise HTTPException(status_code=400, detail="Restaurant already exists")

    restaurants_collection.insert_one(restaurant.dict())
    return {"message": "Restaurant added successfully"}


@router.get("/restaurants/{city}")
def get_restaurants(city: str):
    """Get vegan restaurants in a city"""
    restaurants = list(restaurants_collection.find({"city": city}, {"_id": 0}))
    if not restaurants:
        raise HTTPException(status_code=404, detail="No restaurants found")
    return restaurants
