import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.database import init_db, SessionLocal, Room, Dining, Shuttle

def populate_db():
    init_db()
    db = SessionLocal()

    # Clear existing to prevent duplicates during testing
    db.query(Room).delete()
    db.query(Dining).delete()
    db.query(Shuttle).delete()

    # --- ADD UAEU CIT ROOMS ---
    rooms = [
        Room(name="Robotics and AI Lab", building="CIT (E1)", capacity=30, facilities="High-End GPUs, Robotics Kits, Projector"),
        Room(name="Data Science Lab", building="CIT (E1)", capacity=40, facilities="Workstations, Smartboard"),
        Room(name="Immersive Learning Lab", building="CIT (E1)", capacity=20, facilities="VR Headsets, Tracking Cameras"),
        Room(name="Auditorium 1", building="CIT (E1)", capacity=150, facilities="Video Conference, Surround Sound, Stage"),
        Room(name="Lecture Hall 3", building="CIT (E1)", capacity=105, facilities="Projector, Microphones"),
        Room(name="Study Room A", building="Library", capacity=6, facilities="Whiteboard, Screen Share"),
        Room(name="Study Room B", building="Library", capacity=8, facilities="Whiteboard")
    ]
    db.add_all(rooms)

    # --- ADD DINING SERVICES ---
    dining = [
        Dining(name="Crescent Cafeteria", location="Crescent Building", menu_today="Chicken Machboos, Salad, Lentil Soup", status="Open until 8:00 PM"),
        Dining(name="CIT Coffee Shop", location="CIT (E1) Ground Floor", menu_today="Sandwiches, Lattes, Muffins", status="Open until 5:00 PM"),
        Dining(name="Student Center Food Court", location="Student Center", menu_today="Pizza, Shawarma, Sushi", status="Open until 10:00 PM")
    ]
    db.add_all(dining)

    # --- ADD SHUTTLE SCHEDULES ---
    shuttles = [
        Shuttle(route="Male Hostel to CIT (E1)", next_departures="07:30, 08:00, 08:30, 09:00"),
        Shuttle(route="Female Hostel to Crescent Building", next_departures="07:15, 07:45, 08:15"),
        Shuttle(route="Campus Loop (CIT -> Library -> Student Center)", next_departures="Every 15 minutes")
    ]
    db.add_all(shuttles)

    db.commit()
    db.close()
    print("UAEU Campus Database successfully initialized with real-world simulated data!")

if __name__ == "__main__":
    populate_db()
