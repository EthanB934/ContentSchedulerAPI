from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from models import User

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