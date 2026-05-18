import os
import sys
from dotenv import load_dotenv

# Ensure local imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env'))

from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, SystemMessage

from src.tools.campus_api import (
    search_rooms, 
    book_room, 
    get_dining_menu, 
    get_shuttle_schedule, 
    report_maintenance
)

# Initialize Gemini
# The API key is automatically picked up from the GEMINI_API_KEY env var
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

# Define the tools the agent has access to
tools = [
    search_rooms,
    book_room,
    get_dining_menu,
    get_shuttle_schedule,
    report_maintenance
]

system_prompt = """You are the Smart Campus Operations Agent for the United Arab Emirates University (UAEU).
Your goal is to assist students and faculty by booking rooms, finding food, getting shuttle schedules, and reporting maintenance issues.
Always use your tools to find accurate, real-time information.
If the user wants to book a room, FIRST use `search_rooms` to find an available room that meets their capacity/facility needs, THEN use `book_room` using the ID of the room you found.
If the user doesn't provide an email for booking/maintenance, ask for it, or use a default like 'student@uaeu.ac.ae' if they imply they want it done immediately.
Be extremely helpful, polite, and format your final answers clearly.
"""

# Create the LangGraph agent
campus_agent_executor = create_react_agent(llm, tools, prompt=system_prompt)

def run_campus_agent(user_query: str) -> str:
    """Run the agent on a user query and return the final string response."""
    response = campus_agent_executor.invoke({"messages": [HumanMessage(content=user_query)]})
    return response["messages"][-1].content

if __name__ == "__main__":
    # Test locally
    query = "Is there a room for 100 people with a projector? If so, book it for me (admin@uaeu.ac.ae) tomorrow from 10:00 to 12:00."
    print("User:", query)
    print("Agent:", run_campus_agent(query))
