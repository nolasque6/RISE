from dotenv import load_dotenv

from backend.app.routers import ai, calendar, documents
load_dotenv()

from fastapi import FastAPI
from backend.app.database import Base, engine
from backend.app.routers import users

Base.metadata.create_all(bind=engine)
app = FastAPI(title="RISE APP")

app.include_router(ai.router)
app.include_router(users.router)
# app.include_router(calendar.router)
app.include_router(documents.router)      

@app.get("/")
async def root():
    return {"message": "Welcome to the RISE APP!"}