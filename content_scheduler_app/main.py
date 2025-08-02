from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from models import User, MediaPlatform, PostStatus

# app = FastAPI(title="Social Media Scheduler")

# @app.get("/", response_class=HTMLResponse)
# async def home():
#     return """
#         <h1> Social Media Scheduler </h1>
#         <p> Your portfolio is starting! <p>
#         """

# @app.get("/api/health")
# async def health_check():
#     return {"status": "healthy"}

user_one = User()

my_new_media = MediaPlatform(
    id = 1,
    status = PostStatus(1),
    media_id = 1,
    platform_id = 1
)

print(user_one.created_at)

# Define the Enum with either class or function-call syntax
# Assign the Enum as a value to a column on a table
# When creating that object that stores an Enum value
# Pass the value of the Enum to the created Enum, either class or by function
# When accessing that created object's enum property, you will receive the name of that Enum's value