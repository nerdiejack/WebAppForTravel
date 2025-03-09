from fastapi import FastAPI
import os
from pymongo import MongoClient
from routes import weather, city, restaurants

app = FastAPI()

# Connect to MongoDB
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(mongo_uri)
db = client.travel_db

# Include routers
app.include_router(weather.router, prefix="/api", tags=["Weather"])
app.include_router(city.router, prefix="/api", tags=["Cities"])
app.include_router(restaurants.router, prefix="/api", tags=["Restaurants"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Travel API!"}
