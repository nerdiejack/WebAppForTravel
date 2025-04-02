from fastapi import APIRouter, HTTPException, UploadFile, File
from models import HotelReservation
from database import db
from datetime import datetime
from typing import List
from bson import ObjectId
from bson.errors import InvalidId
import email
from email import policy
from email.parser import BytesParser
import re

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

@router.post("/hotels/import", response_model=HotelReservation)
async def import_hotel_booking(email_file: UploadFile = File(...)):
    try:
        content = await email_file.read()
        email_message = BytesParser(policy=policy.default).parsebytes(content)
        
        # Extract booking details from email body
        body = ""
        if email_message.is_multipart():
            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = email_message.get_payload(decode=True).decode()

        # Extract information using regex patterns
        patterns = {
            "hotel_name": r"Hotel:\s*(.+?)(?:\n|$)",
            "address": r"Address:\s*(.+?)(?:\n|$)",
            "city": r"City:\s*(.+?)(?:\n|$)",
            "check_in": r"Check-in:\s*(.+?)(?:\n|$)",
            "check_out": r"Check-out:\s*(.+?)(?:\n|$)",
            "price": r"Price:\s*(\d+\.?\d*)",
            "booking_id": r"Booking reference:\s*(\w+)",
            "guest_name": r"Guest name:\s*(.+?)(?:\n|$)",
        }
        
        booking_data = {}
        for key, pattern in patterns.items():
            match = re.search(pattern, body)
            if match:
                booking_data[key] = match.group(1).strip()

        if not booking_data:
            raise HTTPException(status_code=400, detail="Could not extract booking information from email")

        # Create hotel reservation object
        hotel_reservation = {
            "hotel_name": booking_data.get("hotel_name", ""),
            "address": booking_data.get("address", ""),
            "city": booking_data.get("city", ""),
            "latitude": 0,  # These will need to be updated manually or via geocoding
            "longitude": 0,
            "check_in": datetime.strptime(booking_data["check_in"], "%Y-%m-%d"),
            "check_out": datetime.strptime(booking_data["check_out"], "%Y-%m-%d"),
            "room_type": "Standard",  # Default value
            "price_per_night": float(booking_data.get("price", 0)),
            "total_price": float(booking_data.get("price", 0)),
            "guest_name": booking_data.get("guest_name", ""),
            "number_of_guests": 1,  # Default value
            "special_requests": "",
            "status": "confirmed",
            "booking_reference": booking_data.get("booking_id", "")
        }

        # Validate required fields
        required_fields = ["hotel_name", "address", "city", "check_in", "check_out", "price", "guest_name"]
        missing_fields = [field for field in required_fields if not hotel_reservation.get(field)]
        if missing_fields:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required fields: {', '.join(missing_fields)}"
            )

        # Save to database
        if hotel_reservation["booking_reference"]:
            existing = await db.hotels.find_one({"booking_reference": hotel_reservation["booking_reference"]})
            if existing:
                await db.hotels.update_one(
                    {"booking_reference": hotel_reservation["booking_reference"]},
                    {"$set": hotel_reservation}
                )
            else:
                result = await db.hotels.insert_one(hotel_reservation)
                hotel_reservation["_id"] = str(result.inserted_id)
        else:
            result = await db.hotels.insert_one(hotel_reservation)
            hotel_reservation["_id"] = str(result.inserted_id)

        return hotel_reservation

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid date format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error importing booking: {str(e)}") 