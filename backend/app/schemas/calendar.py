from pydantic import BaseModel

class EventCreate(BaseModel):
    title: str
    description: str | None = None
    date: str

class EventResponse(BaseModel):
    id: int
    title: str
    description: str | None = None