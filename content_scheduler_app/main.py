from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from datetime import datetime
from typing import List
from pydantic import BaseModel
from .pydantic_models import UserCreate, UserResponse
from .queries import get_users, create_user, get_user_by_id, update_user_in_db, delete_user_from_db, login_user

content_scheduler = FastAPI(title="Content Scheduler", version="0.1.0")

# Declares the endpoint for token generation
# Is a dependency that can be used in path operations
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Path operation to authenticate users
# The dependency defines the security scheme
# Handles JSON requests for user authentication
# Does not handle Docs Form Data
content_scheduler.get("/authenticate", tags=["Authentication"])
async def authenticate(token: Annotated[str, Depends(oauth2_scheme)]):
    """Endpoint to authenticate users using OAuth2 token."""
    return {"token": token}


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

@content_scheduler.get("/users/{user_id}", tags=["Users"])
def get_user(user_id: int, request: UserCreate):
    """Update an existing user in the database."""
    return get_user_by_id(user_id)

@content_scheduler.put("/users/{user_id}", tags=["Users"])
def update_user(user_id: int, request: UserCreate):
    """Update an existing user in the database."""
    return update_user_in_db(user_id, request)

@content_scheduler.delete("/users/{user_id}", tags=["Users"])
def delete_user(user_id: int):
    """Delete a user from the database."""
    return delete_user_from_db(user_id)