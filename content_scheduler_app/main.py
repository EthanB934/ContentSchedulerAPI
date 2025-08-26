from fastapi import FastAPI, Depends, HTTPException
from datetime import datetime
from .pydantic_models import UserCreate, UserResponse
from .queries import get_users, create_user

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

@content_scheduler.get("/users")
def get_all_users():
    """
    This route in the API will query the database for all users   
    """
    return get_users()


@content_scheduler.post("/create-user")
def create_user_in_database(request: UserCreate):
    """
    This route in the API will create a user in the database from
    the provided data in the HTTP request. 
    Args:
        request (UserCreate): A Pydantic model to which the request
        body will be mapped

    Returns:
        JSON serialized data: the return of the encapsulated function
        is a JSON serialized body of data that will be mapped to the 
        UserResponse pydantic model.
    """
    return create_user(request, UserResponse)