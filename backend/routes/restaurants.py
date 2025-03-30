from fastapi import APIRouter, HTTPException
from database import db
from models import Restaurant

router = APIRouter()

@router.post("/restaurant/")
async def add_restaurant(restaurant: Restaurant):
    """Add a new vegan restaurant to the database"""
    existing = await db.restaurants.find_one({"name": restaurant.name, "city": restaurant.city})
    if existing:
        raise HTTPException(status_code=400, detail="Restaurant already exists")

    await db.restaurants.insert_one(restaurant.dict())
    return {"message": "Restaurant added successfully"}

@router.get("/restaurants/{city}")
async def get_restaurants(city: str):
    """Get vegan restaurants in a city"""
    cursor = db.restaurants.find({"city": city}, {"_id": 0})
    restaurants = []
    async for restaurant in cursor:
        restaurants.append(restaurant)
    if not restaurants:
        raise HTTPException(status_code=404, detail="No restaurants found")
    return restaurants
