from turtle import title

from fastapi import FastAPI
from app.database import Base, engine
from app.routers import ai, users, calendar, documents

Base.metadata.create_all(bind=engine)
app = FastAPI(title="RISE APP")

app.include_router(ai.router)
app.include_router(users.router)
app.include_router(calendar.router)
app.include_router(documents.router)      

@app.get("/")
async def root():
    return {"message": "Welcome to the RISE APP!"}