import os
import sys
from datetime import datetime
from langchain_core.tools import tool

# Ensure the parent directory is in the path to import local modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.core.database import SessionLocal, Room, Dining, Shuttle, Booking, Maintenance

@tool
def search_rooms(capacity: int, required_facility: str = None) -> str:
    """Search for available rooms based on minimum capacity and optional required facility (e.g., 'Projector', 'Video Conference')."""
    db = SessionLocal()
    try:
        query = db.query(Room).filter(Room.capacity >= capacity)
        if required_facility:
            query = query.filter(Room.facilities.ilike(f"%{required_facility}%"))
        
        rooms = query.all()
        if not rooms:
            return f"No rooms found for {capacity}+ people with {required_facility}."
        
        results = []
        for r in rooms:
            results.append(f"- Room ID: {r.id} | {r.name} in {r.building} (Capacity: {r.capacity}, Facilities: {r.facilities})")
        return "Available Rooms:\n" + "\n".join(results)
    finally:
        db.close()

@tool
def book_room(room_id: int, user_email: str, start_time: str, end_time: str) -> str:
    """
    Book a room by its ID. 
    start_time and end_time must be in 'YYYY-MM-DD HH:MM' format.
    """
    db = SessionLocal()
    try:
        room = db.query(Room).filter(Room.id == room_id).first()
        if not room:
            return f"Error: Room ID {room_id} not found."
            
        try:
            start = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
            end = datetime.strptime(end_time, "%Y-%m-%d %H:%M")
        except ValueError:
            return "Error: Time format must be 'YYYY-MM-DD HH:MM'"
            
        booking = Booking(
            room_id=room_id,
            user_email=user_email,
            start_time=start,
            end_time=end,
            status="Confirmed"
        )
        db.add(booking)
        db.commit()
        return f"SUCCESS: Room '{room.name}' has been booked for {user_email} from {start_time} to {end_time}."
    finally:
        db.close()

@tool
def get_dining_menu(location: str) -> str:
    """Get the current menu and opening hours for a dining location. Valid locations: 'Crescent', 'CIT', 'Student Center'"""
    db = SessionLocal()
    try:
        dining = db.query(Dining).filter(Dining.name.ilike(f"%{location}%")).first()
        if not dining:
            return f"Error: No dining hall found matching '{location}'. Available are Crescent, CIT, Student Center."
        return f"Menu for {dining.name}: {dining.menu_today}. Hours: {dining.status}."
    finally:
        db.close()

@tool
def get_shuttle_schedule(route_keyword: str) -> str:
    """Get shuttle bus departure times. Keywords: 'Male', 'Female', 'Loop'"""
    db = SessionLocal()
    try:
        shuttle = db.query(Shuttle).filter(Shuttle.route.ilike(f"%{route_keyword}%")).first()
        if not shuttle:
            return "Error: Route not found. Try 'Male Hostel', 'Female Hostel', or 'Loop'."
        return f"Shuttle Route '{shuttle.route}': Next departures are {shuttle.next_departures}."
    finally:
        db.close()

@tool
def report_maintenance(location: str, issue: str, reported_by: str) -> str:
    """Report a facility maintenance issue (e.g., broken AC, lights out)."""
    db = SessionLocal()
    try:
        ticket = Maintenance(
            location=location,
            issue=issue,
            reported_by=reported_by
        )
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        return f"SUCCESS: Maintenance Ticket #{ticket.id} created for '{location}'. Issue: '{issue}'."
    finally:
        db.close()
