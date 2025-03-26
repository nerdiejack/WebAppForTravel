from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

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
