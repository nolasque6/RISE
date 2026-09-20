from fastapi import APIRouter, FastAPI
from app.routers import ai, users, calendar, documents

app = FastAPI()

app.include_router(ai.router)
app.include_router(users.router)
app.include_router(calendar.router)
app.include_router(documents.router)      

@app.get("/")
async def root():
    return {"message": "Welcome to the RISE APP!"}