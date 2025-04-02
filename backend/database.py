import motor.motor_asyncio
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://db:27017/travel_db")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client.travel_db

# Ensure indexes are created
async def init_db():
    try:
        # Create indexes for various collections
        await db.cities.create_index("name", unique=True)
        await db.restaurants.create_index([("name", 1), ("city", 1)], unique=True)
        
        # Hotel booking indexes
        await db.hotels.create_index("booking_reference", unique=True, sparse=True)
        await db.hotels.create_index("city")
        await db.hotels.create_index("check_in")
        await db.hotels.create_index("status")
        await db.hotels.create_index([("latitude", 1), ("longitude", 1)])
        
        await db.diary.create_index("created_at")
        print("Database indexes created successfully")
    except Exception as e:
        print(f"Error creating database indexes: {e}")

# Export the init function
__all__ = ["db", "init_db"]
