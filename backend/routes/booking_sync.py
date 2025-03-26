from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from models import HotelReservation
from database import db
import os
import requests
from datetime import datetime
from typing import List, Optional
import json
import re
import email
from email import policy
from email.parser import BytesParser

router = APIRouter()

BOOKING_API_URL = "https://distribution-xml.booking.com/2.0/json"
# These should be stored in environment variables
BOOKING_USERNAME = os.getenv("BOOKING_USERNAME")
BOOKING_PASSWORD = os.getenv("BOOKING_PASSWORD")

def get_booking_auth():
    return (BOOKING_USERNAME, BOOKING_PASSWORD)

@router.post("/sync-booking-reservations")
async def sync_booking_reservations():
    try:
        # Get reservations from Booking.com
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        # Example endpoint for reservations (you'll need to adjust based on Booking.com's actual API)
        response = requests.get(
            f"{BOOKING_API_URL}/reservations",
            auth=get_booking_auth(),
            headers=headers
        )
        
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to fetch Booking.com reservations")
            
        bookings = response.json()
        
        # Transform and save each booking
        for booking in bookings:
            hotel_reservation = {
                "hotel_name": booking["hotel_name"],
                "address": booking["hotel_address"],
                "city": booking["city"],
                "latitude": float(booking["latitude"]),
                "longitude": float(booking["longitude"]),
                "check_in": datetime.fromisoformat(booking["checkin"]),
                "check_out": datetime.fromisoformat(booking["checkout"]),
                "room_type": booking["room_type"],
                "price_per_night": float(booking["price_per_night"]),
                "total_price": float(booking["total_price"]),
                "guest_name": booking["guest_name"],
                "number_of_guests": int(booking["number_of_guests"]),
                "special_requests": booking.get("special_requests", ""),
                "status": "confirmed",
                "booking_reference": booking["booking_id"]  # Store Booking.com reference
            }
            
            # Check if booking already exists
            existing = await db["hotels"].find_one({"booking_reference": booking["booking_id"]})
            if existing:
                await db["hotels"].update_one(
                    {"booking_reference": booking["booking_id"]},
                    {"$set": hotel_reservation}
                )
            else:
                await db["hotels"].insert_one(hotel_reservation)
                
        return {"message": "Successfully synced Booking.com reservations"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/booking-status")
async def check_booking_connection():
    try:
        response = requests.get(
            f"{BOOKING_API_URL}/hotels",
            auth=get_booking_auth(),
            headers={"Accept": "application/json"}
        )
        return {
            "status": "connected" if response.status_code == 200 else "error",
            "message": "Successfully connected to Booking.com API" if response.status_code == 200 else "Failed to connect"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@router.post("/import-booking-email")
async def import_booking_email(email_file: UploadFile = File(...)):
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

        # Save to database
        if hotel_reservation["booking_reference"]:
            existing = await db["hotels"].find_one({"booking_reference": hotel_reservation["booking_reference"]})
            if existing:
                await db["hotels"].update_one(
                    {"booking_reference": hotel_reservation["booking_reference"]},
                    {"$set": hotel_reservation}
                )
            else:
                await db["hotels"].insert_one(hotel_reservation)
        else:
            await db["hotels"].insert_one(hotel_reservation)

        return {"message": "Successfully imported booking from email"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/manual-booking")
async def add_manual_booking(
    hotel_name: str = Form(...),
    address: str = Form(...),
    city: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    check_in: str = Form(...),
    check_out: str = Form(...),
    room_type: str = Form(...),
    price_per_night: float = Form(...),
    guest_name: str = Form(...),
    number_of_guests: int = Form(...),
    booking_reference: Optional[str] = Form(None),
    special_requests: Optional[str] = Form("")
):
    try:
        hotel_reservation = {
            "hotel_name": hotel_name,
            "address": address,
            "city": city,
            "latitude": latitude,
            "longitude": longitude,
            "check_in": datetime.strptime(check_in, "%Y-%m-%d"),
            "check_out": datetime.strptime(check_out, "%Y-%m-%d"),
            "room_type": room_type,
            "price_per_night": price_per_night,
            "total_price": price_per_night * (datetime.strptime(check_out, "%Y-%m-%d") - datetime.strptime(check_in, "%Y-%m-%d")).days,
            "guest_name": guest_name,
            "number_of_guests": number_of_guests,
            "special_requests": special_requests,
            "status": "confirmed",
            "booking_reference": booking_reference or f"MANUAL-{datetime.now().timestamp()}"
        }

        # Save to database
        if booking_reference:
            existing = await db["hotels"].find_one({"booking_reference": booking_reference})
            if existing:
                await db["hotels"].update_one(
                    {"booking_reference": booking_reference},
                    {"$set": hotel_reservation}
                )
            else:
                await db["hotels"].insert_one(hotel_reservation)
        else:
            await db["hotels"].insert_one(hotel_reservation)

        return {"message": "Successfully added manual booking"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 