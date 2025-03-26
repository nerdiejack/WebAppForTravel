from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import city, restaurants, map, hotels, booking_sync

app = FastAPI()

# Enable CORS for the development environment
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include API routers without /api prefix
app.include_router(city.router, tags=["Cities"])
app.include_router(restaurants.router, tags=["Restaurants"])
app.include_router(map.router, tags=["Map"])
app.include_router(hotels.router, tags=["Hotels"])
app.include_router(booking_sync.router, tags=["Booking Sync"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Travel API!"}
