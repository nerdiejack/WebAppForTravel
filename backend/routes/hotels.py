from fastapi import APIRouter, HTTPException
from models import HotelReservation
from database import db
from datetime import datetime
from typing import List
from bson import ObjectId
from bson.errors import InvalidId

router = APIRouter(prefix="/api")

@router.post("/hotels/", response_model=HotelReservation)
async def create_hotel_reservation(reservation: HotelReservation):
    reservation_dict = reservation.dict(exclude={'_id'})
    # Convert datetime objects to strings for MongoDB
    reservation_dict["check_in"] = reservation_dict["check_in"].isoformat()
    reservation_dict["check_out"] = reservation_dict["check_out"].isoformat()
    
    result = await db.hotels.insert_one(reservation_dict)
    created_reservation = await db.hotels.find_one({"_id": result.inserted_id})
    # Convert string dates back to datetime for response
    created_reservation["check_in"] = datetime.fromisoformat(created_reservation["check_in"])
    created_reservation["check_out"] = datetime.fromisoformat(created_reservation["check_out"])
    # Convert ObjectId to string
    created_reservation["_id"] = str(created_reservation["_id"])
    return created_reservation

@router.get("/hotels/", response_model=List[HotelReservation])
async def get_hotel_reservations():
    hotels = []
    cursor = db.hotels.find()
    async for hotel in cursor:
        # Convert string dates back to datetime
        hotel["check_in"] = datetime.fromisoformat(hotel["check_in"])
        hotel["check_out"] = datetime.fromisoformat(hotel["check_out"])
        # Convert ObjectId to string and set both id and _id
        str_id = str(hotel["_id"])
        hotel["_id"] = str_id
        hotel["id"] = str_id
        hotels.append(hotel)
    return hotels

@router.get("/hotels/{city}", response_model=List[HotelReservation])
async def get_hotels_by_city(city: str):
    hotels = []
    cursor = db.hotels.find({"city": city})
    async for hotel in cursor:
        # Convert string dates back to datetime
        hotel["check_in"] = datetime.fromisoformat(hotel["check_in"])
        hotel["check_out"] = datetime.fromisoformat(hotel["check_out"])
        # Convert ObjectId to string
        hotel["_id"] = str(hotel["_id"])
        hotels.append(hotel)
    return hotels

@router.put("/hotels/{hotel_id}", response_model=HotelReservation)
async def update_hotel_reservation(hotel_id: str, reservation: HotelReservation):
    reservation_dict = reservation.dict(exclude={'_id'})
    # Convert datetime objects to strings for MongoDB
    reservation_dict["check_in"] = reservation_dict["check_in"].isoformat()
    reservation_dict["check_out"] = reservation_dict["check_out"].isoformat()
    
    result = await db.hotels.update_one(
        {"_id": ObjectId(hotel_id)},
        {"$set": reservation_dict}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Hotel reservation not found")
    
    updated_reservation = await db.hotels.find_one({"_id": ObjectId(hotel_id)})
    # Convert string dates back to datetime for response
    updated_reservation["check_in"] = datetime.fromisoformat(updated_reservation["check_in"])
    updated_reservation["check_out"] = datetime.fromisoformat(updated_reservation["check_out"])
    # Convert ObjectId to string
    updated_reservation["_id"] = str(updated_reservation["_id"])
    return updated_reservation

@router.delete("/hotels/{hotel_id}")
async def delete_hotel_reservation(hotel_id: str):
    try:
        # Validate the hotel_id format
        if not hotel_id or not ObjectId.is_valid(hotel_id):
            raise HTTPException(status_code=400, detail="Invalid hotel ID format")

        result = await db.hotels.delete_one({"_id": ObjectId(hotel_id)})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Hotel reservation not found")
        
        return {"message": "Hotel reservation deleted successfully", "id": hotel_id}
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid hotel ID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 