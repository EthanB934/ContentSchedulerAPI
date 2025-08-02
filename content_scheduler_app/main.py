from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from .models import User, Platform, Interaction, PostStatus
from datetime import datetime

# Initializes and instance of FastAPI, variable inherits FastAPI properties and methods
content_scheduler = FastAPI(title="Content Scheduler", version="0.1.0")

# Defines a new route in the API. The route is the string passed to .get()
@content_scheduler.get("/")
# Defines asynchronous function to invoke at API root route "/"
async def root():
    """
        This is the home route of the content scheduler app.
    """
    return {"message": "Social Media Scheduler API is running!"}

@content_scheduler.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}
