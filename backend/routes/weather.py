from fastapi import APIRouter, HTTPException
import requests
import os

router = APIRouter()

WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "562be03eecf252f9ea302760628634ab")


@router.get("/weather/")
def get_weather(city: str):
    """Fetch real-time weather data for a given city"""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"

    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="City not found")

    data = response.json()

    return {
        "city": data["name"],
        "temperature": data["main"]["temp"],
        "weather": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"]
    }
