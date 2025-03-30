from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

# Import database initialization
from database import init_db

# Import routes
from routes.city import router as city_router
from routes.restaurants import router as restaurants_router
from routes.map import router as map_router
from routes.hotels import router as hotels_router
from routes.booking_sync import router as booking_sync_router
from routes.diary import router as diary_router

app = FastAPI()

# Enable CORS for the development environment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Create uploads directory if it doesn't exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("uploads/thumbnails", exist_ok=True)

# Mount static files
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Include API routers
app.include_router(city_router, prefix="/api", tags=["Cities"])
app.include_router(restaurants_router, prefix="/api", tags=["Restaurants"])
app.include_router(map_router, prefix="/api", tags=["Map"])
app.include_router(hotels_router, tags=["Hotels"])
app.include_router(booking_sync_router, tags=["Booking Sync"])
app.include_router(diary_router, tags=["Diary"])

@app.on_event("startup")
async def startup_event():
    """Initialize the database on startup"""
    await init_db()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Travel API!"}
