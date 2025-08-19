from pydantic import BaseModel
import datetime
class UserCreate(BaseModel):
    id: int
    username: str
    password: str
    email: str
    created_at: None
    is_admin: bool

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_admin: bool
    created_at: datetime.datetime