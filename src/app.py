"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Competitive basketball team for interscholastic play",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["marcus@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Learn tennis skills and participate in matches",
        "schedule": "Wednesdays and Saturdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["alex@mergington.edu", "jordan@mergington.edu"]
    },
    "Art Studio": {
        "description": "Explore painting, drawing, and mixed media techniques",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["grace@mergington.edu"]
    },
    "Music Band": {
        "description": "Play instruments and perform in school concerts",
        "schedule": "Tuesdays and Thursdays, 3:00 PM - 4:30 PM",
        "max_participants": 25,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop critical thinking and public speaking skills",
        "schedule": "Mondays and Fridays, 3:30 PM - 4:30 PM",
        "max_participants": 14,
        "participants": ["sarah@mergington.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments and explore STEM topics",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["ava@mergington.edu", "ethan@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Normalize email for consistent comparison/storage
    normalized_email = email.strip().lower()

    # Validate student is not already signed up (case/whitespace insensitive)
    if any(p.strip().lower() == normalized_email for p in activity["participants"]):
        raise HTTPException(status_code=400, detail="Student is already signed up for this activity")

    # Add student (store normalized email)
    activity["participants"].append(normalized_email)
    return {"message": f"Signed up {normalized_email} for {activity_name}"}


@app.delete("/activities/{activity_name}/signup")
def unregister_for_activity(activity_name: str, email: str):
    """Unregister a student from an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]
    normalized_email = email.strip().lower()

    # Find and remove the participant (case/whitespace insensitive)
    for i, p in enumerate(activity["participants"]):
        if p.strip().lower() == normalized_email:
            activity["participants"].pop(i)
            return {"message": f"Unregistered {normalized_email} from {activity_name}"}

    raise HTTPException(status_code=404, detail="Participant not found in this activity")
