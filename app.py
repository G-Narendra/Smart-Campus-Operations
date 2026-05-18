import os
import sys
import streamlit as st
from dotenv import load_dotenv

base_dir = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(base_dir, '.env'))
sys.path.append(base_dir)

from src.agents.campus_agent import run_campus_agent
from src.core.database import SessionLocal, Booking, Maintenance, Room, Dining, Shuttle

# Define custom page config
st.set_page_config(
    page_title="UAEU Smart Campus Agent",
    page_icon="🎓",
    layout="wide"
)

def fetch_recent_bookings():
    db = SessionLocal()
    bookings = db.query(Booking).order_by(Booking.id.desc()).limit(5).all()
    db.close()
    return bookings

def fetch_recent_tickets():
    db = SessionLocal()
    tickets = db.query(Maintenance).order_by(Maintenance.id.desc()).limit(5).all()
    db.close()
    return tickets

def fetch_status():
    db = SessionLocal()
    room_count = db.query(Room).count()
    shuttle_count = db.query(Shuttle).count()
    dining_count = db.query(Dining).count()
    db.close()
    return room_count, shuttle_count, dining_count

st.title("🎓 UAEU Smart Campus Agent")
st.caption("Powered by LangGraph, Gemini 2.5 Flash, and local FastAPI/SQLite APIs")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Welcome to the UAEU Campus Operations Center! I can help you book rooms in CIT, check dining menus, track shuttles, or report maintenance issues. How can I help?"}
    ]

# Layout: Chat on the left, Dashboard on the right
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("💬 Agent Chat")
    chat_container = st.container(height=500)
    
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Chat Input
    prompt = st.chat_input("E.g., Book a room for 150 people with a projector...")
    
    # Preset queries
    cols = st.columns(3)
    if cols[0].button("Check CIT Menu"):
        prompt = "What's on the menu at the CIT coffee shop today?"
    if cols[1].button("Report Broken AC"):
        prompt = "Report that the AC is broken in the Data Science Lab. My email is narendra@uaeu.ac.ae."
    if cols[2].button("Male Shuttle"):
        prompt = "When is the next male hostel shuttle to CIT?"

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.chat_message("assistant"):
                with st.spinner("Agent is reasoning and using tools..."):
                    response = run_campus_agent(prompt)
                    st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun() # Refresh dashboard on the right

with col2:
    st.subheader("📊 System Dashboard")
    rooms, shuttles, dining = fetch_status()
    st.info(f"**Systems Online:**\n- {rooms} Rooms tracked\n- {shuttles} Shuttle Routes\n- {dining} Dining Halls")
    
    st.markdown("### 📝 Recent Bookings")
    bookings = fetch_recent_bookings()
    if not bookings:
        st.write("No bookings yet.")
    for b in bookings:
        st.success(f"Room {b.room_id} | {b.start_time.strftime('%H:%M')} | {b.user_email}")
        
    st.markdown("### 🛠️ Maintenance Tickets")
    tickets = fetch_recent_tickets()
    if not tickets:
        st.write("No tickets yet.")
    for t in tickets:
        st.error(f"#{t.id} - {t.location}: {t.issue}")
