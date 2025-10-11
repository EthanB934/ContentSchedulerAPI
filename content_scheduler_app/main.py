from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from datetime import datetime
from typing import List
from pydantic import BaseModel
from .pydantic_models import UserCreate, UserResponse
from .queries import get_users, create_user, get_user_by_id, update_user_in_db, delete_user_from_db

content_scheduler = FastAPI(title="Content Scheduler", version="0.1.0")

def get_token():
    print("Token endpoint called")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
    return oauth2_scheme

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


def fake_decode_token(token):
    print(type(token))
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )


async def get_current_user(token: Annotated[str, Depends(get_token)]):
    user = fake_decode_token(token)
    return user

@content_scheduler.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

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