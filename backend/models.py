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

class Restaurant(BaseModel):
    name: str
    city: str
    address: str
    rating: float

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
    status: str = "confirmed"  # confirmed, cancelled, completed
    booking_reference: Optional[str] = None

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
        validate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
