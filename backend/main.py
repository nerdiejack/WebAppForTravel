from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import weather, city, restaurants, map

app = FastAPI()

# Enable CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (change this in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include API routers
app.include_router(weather.router, prefix="/api", tags=["Weather"])
app.include_router(city.router, prefix="/api", tags=["Cities"])
app.include_router(restaurants.router, prefix="/api", tags=["Restaurants"])
app.include_router(map.router, prefix="/api", tags=["Map"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Travel API!"}
