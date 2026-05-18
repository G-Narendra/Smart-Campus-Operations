import os
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime

# Setup DB path relative to this file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "data", "campus.db")

# Create data dir if not exists
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

engine = create_engine(f"sqlite:///{DB_PATH}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)      # e.g., "Lecture Hall 1"
    building = Column(String, index=True)  # e.g., "CIT (E1)"
    capacity = Column(Integer)
    facilities = Column(String)            # e.g., "Video Conference, Projector"

class Dining(Base):
    __tablename__ = "dining"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)      # e.g., "Crescent Cafeteria"
    location = Column(String)
    menu_today = Column(String)
    status = Column(String)                # e.g., "Open until 8PM"

class Shuttle(Base):
    __tablename__ = "shuttles"
    id = Column(Integer, primary_key=True, index=True)
    route = Column(String, index=True)     # e.g., "Hostel to CIT E1"
    next_departures = Column(String)       # e.g., "08:00, 08:30, 09:00"

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    user_email = Column(String, index=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    status = Column(String, default="Confirmed")
    
    room = relationship("Room")

class Maintenance(Base):
    __tablename__ = "maintenance_tickets"
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String)
    issue = Column(String)
    reported_by = Column(String)
    reported_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="Open")

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
