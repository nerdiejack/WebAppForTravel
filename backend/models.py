from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from bson import ObjectId
from pydantic import validator

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
    hotel_name: str = Field(..., min_length=1, description="Name of the hotel")
    address: str = Field(..., min_length=1, description="Full address of the hotel")
    city: str = Field(..., min_length=1, description="City where the hotel is located")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude coordinate of the hotel")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude coordinate of the hotel")
    check_in: datetime = Field(..., description="Check-in date and time")
    check_out: datetime = Field(..., description="Check-out date and time")
    room_type: str = Field(..., min_length=1, description="Type of room booked")
    price_per_night: float = Field(..., ge=0, description="Price per night in USD")
    total_price: float = Field(..., ge=0, description="Total price for the entire stay")
    guest_name: str = Field(..., min_length=1, description="Name of the guest")
    number_of_guests: int = Field(..., ge=1, description="Number of guests staying")
    special_requests: Optional[str] = Field(None, description="Any special requests for the stay")
    status: str = Field("confirmed", pattern="^(confirmed|cancelled|completed)$", description="Status of the booking")
    booking_reference: Optional[str] = Field(None, description="External booking reference number")

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
                "special_requests": "High floor room",
                "status": "confirmed",
                "booking_reference": "BK123456"
            }
        }

    @validator('check_out')
    def check_out_after_check_in(cls, v, values):
        if 'check_in' in values and v <= values['check_in']:
            raise ValueError('Check-out date must be after check-in date')
        return v

    @validator('total_price')
    def validate_total_price(cls, v, values):
        if 'price_per_night' in values and 'check_in' in values and 'check_out' in values:
            nights = (values['check_out'] - values['check_in']).days
            expected_total = values['price_per_night'] * nights
            if abs(v - expected_total) > 0.01:  # Allow for small floating-point differences
                raise ValueError('Total price does not match price per night * number of nights')
        return v

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
