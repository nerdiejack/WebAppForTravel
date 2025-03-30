from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, handler):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        return {"type": "string"}

class City(BaseModel):
    name: str
    country: str
    population: int
    description: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Paris",
                "country": "France",
                "population": 2148271,
                "description": "The City of Light"
            }
        }

class Restaurant(BaseModel):
    name: str
    city: str
    address: str
    rating: float

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Le Vegan",
                "city": "Paris",
                "address": "123 Rue de la Paix",
                "rating": 4.5
            }
        }

class HotelReservation(BaseModel):
    id: Optional[str] = None
    _id: Optional[str] = None
    hotel_name: str
    address: str
    city: str
    latitude: float
    longitude: float
    check_in: datetime
    check_out: datetime
    room_type: str
    price_per_night: float
    total_price: float
    guest_name: str
    number_of_guests: int
    special_requests: Optional[str] = None
    status: str = "confirmed"
    booking_reference: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "hotel_name": "Grand Hotel",
                "address": "456 Avenue des Champs-Élysées",
                "city": "Paris",
                "latitude": 48.8566,
                "longitude": 2.3522,
                "check_in": "2024-04-01T14:00:00",
                "check_out": "2024-04-05T11:00:00",
                "room_type": "Deluxe",
                "price_per_night": 200.0,
                "total_price": 800.0,
                "guest_name": "John Doe",
                "number_of_guests": 2,
                "special_requests": "High floor room"
            }
        }

class Photo(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    url: str
    caption: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    pin_id: PyObjectId

    class Config:
        validate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class PhotoPin(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    latitude: float
    longitude: float
    title: str
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    photos: List[PyObjectId] = []

    class Config:
        validate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class TravelEntry(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    title: str
    content: str
    date: datetime
    location: Optional[str] = None
    pin_id: Optional[PyObjectId] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        validate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class DiaryEntry(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    title: str
    content: str
    location: dict = Field(..., description="Location coordinates and name")
    images: List[str] = Field(default_factory=list, description="List of image URLs")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "title": "First Day in Paris",
                "content": "Visited the Eiffel Tower",
                "location": {
                    "name": "Paris",
                    "lat": 48.8566,
                    "lng": 2.3522
                },
                "images": []
            }
        }
