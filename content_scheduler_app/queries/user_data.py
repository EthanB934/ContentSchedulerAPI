"""
This module is responsible for the manipulation of user data, whether creating, reading, updating
or deleting that data. HTTP requests handled by FastAPI's routing system, where endpoints end in
*user, should be redirected here and handled. The data received will then be used to manipulate the
users table in the PostGreSQL database.
"""

import os
import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from fastapi import HTTPException
from ..pydantic_models import UserCreate, UserResponse

# 1. Loads any environment variables as global variables to be used within the scope of this module
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not defined!")

# 2. The database connection string has been retrieved and stored. 
# A database engine can now be created
engine = create_engine(DATABASE_URL, echo=True)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def login_user(form_data) -> UserResponse:
    """
    Authenticate a user based on the provided form data.
    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing username and password
    Returns:
        UserResponse: The authenticated user object (without password)
    Raises:
        HTTPException: If authentication fails
    """

    with engine.connect() as conn:
        query = conn.execute(
            text("SELECT id, username, password, email, created_at, is_admin FROM content_scheduler.user WHERE username = :username"),
            {"username": form_data.username}
        )
        result = query.fetchone()
        if result and pwd_context.verify(form_data.password, result.password):
            return UserResponse(
                id=result.id,
                username=result.username,
                email=result.email,
                created_at=result.created_at,
                is_admin=result.is_admin
            )
        else:
            raise HTTPException(status_code=401, detail="Invalid username or password.")

def get_users():
    """
    Retrieve a list of all users from the PostGreSQL database.
    Returns:
        List[dict]: List of user objects (excluding passwords)
    """
    with engine.connect() as conn:
        query = conn.execute(
            text("SELECT id, username, email, created_at, is_admin FROM content_scheduler.user")
        )
        result = query.fetchall()
        users = [dict(row._mapping) for row in result]
        return users

def get_user_by_id(user_id: int) -> UserResponse:
    """
    Retrieve a user by their ID from the database.
    Args:
        user_id (int): The ID of the user to retrieve
    Returns:
        UserResponse: The user object (without password)
    """
    with engine.connect() as conn:
        query = conn.execute(
            text("SELECT id, username, email, created_at, is_admin FROM content_scheduler.user WHERE id = :id"),
            {"id": user_id}
        )
        result = query.fetchone()
        if result:
            return UserResponse(
                id=result.id,
                username=result.username,
                email=result.email,
                created_at=result.created_at,
                is_admin=result.is_admin
            )
        else:
            raise HTTPException(status_code=404, detail="User not found.")

def create_user(request: UserCreate) -> UserResponse:
    """
    Create a new user in the database. Hashes the password before storing.
    Args:
        request (UserCreate): User creation data
    Returns:
        UserResponse: The created user (without password)
    Raises:
        HTTPException: If user already exists or DB error occurs
    """
    hashed_password = get_password_hash(request.password)
    with engine.connect() as conn:
        try:
            query = conn.execute(
                text(
                    """
                    INSERT INTO content_scheduler.user (username, password, email, created_at, is_admin)
                    VALUES (:username, :password, :email, :created_at, :is_admin)
                    RETURNING id, username, email, created_at, is_admin
                    """
                ),
                {
                    "username": request.username,
                    "password": hashed_password,
                    "email": request.email,
                    "created_at": request.created_at or datetime.datetime.now(),
                    "is_admin": request.is_admin
                }
            )
            result = query.fetchone()

            conn.commit()
            
            if result:
                return UserResponse(
                    id=result.id,
                    username=result.username,
                    email=result.email,
                    created_at=result.created_at,
                    is_admin=result.is_admin
                )
            else:
                raise HTTPException(status_code=500, detail="User creation failed.")
        except IntegrityError as e:
            raise HTTPException(status_code=400, detail="User with this email or username already exists.")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
def update_user_in_db(user_id: int, request: UserCreate):
    """
    Update an existing user in the database.
    Args:
        user_id (int): The ID of the user to update
        request (UserCreate): The new data for the user
    Returns:
        UserResponse: The updated user (without password)
    """
    with engine.connect() as conn:
            query = conn.execute(
                text(
                    """
                    UPDATE content_scheduler.user
                    SET username = :username,
                        email = :email,
                        is_admin = :is_admin
                    WHERE id = :id
                    RETURNING id, username, email, created_at, is_admin
                    """
                ),
                {
                    "id": user_id,
                    "username": request.username,
                    "email": request.email,
                    "is_admin": request.is_admin
                }
            )
            result = query.fetchone()
            conn.commit()

            if result:
                return UserResponse(
                    id=result.id,
                    username=result.username,
                    email=result.email,
                    created_at=result.created_at,
                    is_admin=result.is_admin
                )
            else:
                raise HTTPException(status_code=404, detail="User not found.")
            
def delete_user_from_db(user_id: int):
    """
    Delete a user from the database.
    Args:
        user_id (int): The ID of the user to delete
    Raises:
        HTTPException: If user not found or DB error occurs
    """

    with engine.connect() as conn:
        try:
            query = conn.execute(
                text("DELETE FROM content_scheduler.user WHERE id = :id"),
                {"id": user_id}
            )
            if query.rowcount == 0:
                raise HTTPException(status_code=404, detail="User not found.")
            conn.commit()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))