from fastapi import APIRouter
from app.schemas.calendar import EventCreate, EventResponse

router = APIRouter(prefix="/calendar", tags=["Calendar"])

@router.post("/events", response_model=EventResponse)
async def create_event(event: EventCreate):
    return {
        "id": 1,
        "title": event.title,
        "description": event.description,
        "date": event.date
    }