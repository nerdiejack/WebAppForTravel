from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://db:27017/travel_db")
client = AsyncIOMotorClient(MONGO_URI)
db = client.travel_db
