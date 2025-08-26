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

# 1. Loads any environment variables as global variables to be used within the scope of this module
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not defined!")

# 2. The database connection string has been retrieved and stored. 
# A database engine can now be created
engine = create_engine(DATABASE_URL, echo=True)

def get_users():
    """
        GET users will be for used for retrieving a list of all users from the PostGreSQL database.
    Returns:
        JSON Serialized List: Since we are querying the database for a list of items, 
        and because FastAPI handles the JSON serialization of data in the response body, the query
        will return a JSON serialized list of users objects from PostGreSQL's Result Object.
    """
    # Creates an open connection to the database
    with engine.connect() as conn:
        # Runs SQL expression in PSQL database
        query = conn.execute(
            text("SELECT * FROM content_scheduler.user" \
            "RETURNING id, username, email, created_at, is_admin"),)
        
        # Stores all found users 
        result = query.fetchall()

        # Initializes an empty Python list to contain serialized data.
        users = []

        # Iterates through Cursor Result objects to begin serialization.
        for row in result:
            # Serializes Cursor Row objects into Python dictionaries
            users.append(dict(row._mapping))

        # Return the serialized list of user data
        return users

def create_user(request, response):
    # Creates an open connection to the database
    with engine.begin() as conn:
        # Run SQL expression, to create new user
        query = conn.execute(
            text("INSERT INTO content_scheduler.user " \
            "VALUES (:id, :username, :password, :email, :created_at, :is_admin)"
            "RETURNING id, username, email, created_at, is_admin",),
            # Maps request body data to user properties in database
            [
                {
                    "id": request.id,
                    "username": request.username,
                    "password": request.password,
                    "email": request.email,
                    "created_at": datetime.datetime.now(),
                    "is_admin": request.is_admin
                }
            ]
        
        )

        # Fetches and stores the newly created user resource
        result = query.fetchone()

        # If result is not none
        if result:
            # Maps user data from database to pydantic model UserResponse as HTTP response
            return response(
                id = result.id,
                username = result.username,
                email = result.email,
                created_at = result.created_at,
                is_admin = result.is_admin
            )