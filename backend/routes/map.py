import time
import os
import pandas as pd
from fastapi import APIRouter, HTTPException
from geopy.geocoders import Nominatim
from opencage.geocoder import OpenCageGeocode
from database import db

router = APIRouter()

# Initialize geocoders
geolocator = Nominatim(user_agent="geoapi", timeout=10)  # OpenStreetMap
OPENCAGE_API_KEY = os.getenv("OPENCAGE_API_KEY", "0b3d0ca596734914880b9a980d0b8e15")
geocoder = OpenCageGeocode(OPENCAGE_API_KEY) if OPENCAGE_API_KEY else None


def get_city_coordinates(city_name):
    """Fetch GPS coordinates with retries and fallback to OpenCage API."""

    # Check if the coordinates already exist in the database
    city_data = db["cities"].find_one({"name": city_name}, {"latitude": 1, "longitude": 1, "_id": 0})
    if city_data and "latitude" in city_data and "longitude" in city_data:
        print(f"Using cached coordinates for {city_name}: {city_data}")
        return city_data["latitude"], city_data["longitude"]

    # Try fetching coordinates using Nominatim
    for _ in range(3):  # Retry up to 3 times
        try:
            location = geolocator.geocode(city_name, timeout=10)
            if location:
                print(f"Nominatim API Success: {city_name} → {location.latitude}, {location.longitude}")
                return location.latitude, location.longitude
        except Exception as e:
            print(f"Nominatim API Failed for {city_name}: {e}")
            time.sleep(2)  # Wait before retrying

    # Fallback to OpenCage if available
    if geocoder:
        try:
            result = geocoder.geocode(city_name)
            if result:
                print(
                    f"OpenCage API Success: {city_name} → {result[0]['geometry']['lat']}, {result[0]['geometry']['lng']}")
                return result[0]['geometry']['lat'], result[0]['geometry']['lng']
        except Exception as e:
            print(f"OpenCage API Failed for {city_name}: {e}")

    return None, None  # No coordinates found


@router.get("/map/")
def get_map_data():
    """Return map data as JSON instead of HTML for React frontend."""

    # Retrieve all cities from MongoDB
    cities = list(db["cities"].find({}, {"_id": 0, "name": 1, "country": 1, "latitude": 1, "longitude": 1}))
    if not cities:
        raise HTTPException(status_code=404, detail="No cities found")

    # Fetch and update missing coordinates
    for city in cities:
        if "latitude" not in city or "longitude" not in city or city["latitude"] is None:
            lat, lon = get_city_coordinates(city["name"])
            if lat and lon:
                city["latitude"], city["longitude"] = lat, lon
                # Update MongoDB with the new coordinates
                db["cities"].update_one({"name": city["name"]}, {"$set": {"latitude": lat, "longitude": lon}})

    return {"cities": cities}
