from fastapi import FastAPI, HTTPException
from datetime import datetime
from typing import List
from .pydantic_models.models import UserCreate, UserResponse
from .queries.user_data import get_users, create_user

content_scheduler = FastAPI(title="Content Scheduler", version="0.1.0")

@content_scheduler.get("/", tags=["Root"])
async def root():
    """Home route of the content scheduler app."""
    return {"message": "Social Media Scheduler API is running!"}

@content_scheduler.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now()}

@content_scheduler.get("/users", response_model=List[UserResponse], tags=["Users"])
def get_all_users():
    """Retrieve all users from the database."""
    return get_users()

@content_scheduler.post("/users", response_model=UserResponse, status_code=201, tags=["Users"])
def create_user_in_database(request: UserCreate):
    """Create a new user in the database from the provided data."""
    return create_user(request)

@content_scheduler.put("/users/{user_id}", tags=["Users"])
def update_user_in_db(user_id: int, request: UserCreate):
    """Update an existing user in the database."""
    pass