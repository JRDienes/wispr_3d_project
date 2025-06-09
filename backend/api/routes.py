from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
import os
from pathlib import Path
from fastapi.responses import FileResponse

app = FastAPI(title="WISPR 3D Visualization API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class WISPREvent(BaseModel):
    id: str
    timestamp: str
    description: str
    data_path: str
    preview_url: Optional[str] = None

# In-memory storage for events (replace with database in production)
events = []

@app.get("/")
async def root():
    return {"message": "Welcome to WISPR 3D Visualization API"}

@app.get("/events", response_model=List[WISPREvent])
async def get_events():
    return events

@app.get("/event/{event_id}", response_model=WISPREvent)
async def get_event(event_id: str):
    event = next((e for e in events if e["id"] == event_id), None)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@app.get("/event/{event_id}/data")
async def get_event_data(event_id: str):
    event = next((e for e in events if e["id"] == event_id), None)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    data_path = Path(event["data_path"])
    if not data_path.exists():
        raise HTTPException(status_code=404, detail="Event data not found")
    
    # Return the data file
    return FileResponse(data_path)

# Initialize events from data directory
def initialize_events():
    data_dir = Path("backend/data/wispr_data")
    if not data_dir.exists():
        return
    
    for file_path in data_dir.glob("*.fits"):
        event_id = file_path.stem
        timestamp = file_path.stem.split("_")[2]  # Extract timestamp from filename
        events.append({
            "id": event_id,
            "timestamp": timestamp,
            "description": f"WISPR observation at {timestamp}",
            "data_path": str(file_path),
            "preview_url": f"/previews/{event_id}.png"
        })

# Initialize events when the application starts
initialize_events() 