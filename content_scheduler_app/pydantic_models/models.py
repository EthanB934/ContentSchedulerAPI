from pydantic import BaseModel
import datetime
from typing import Optional

class UserCreate(BaseModel):
    """
    The user creation model.
        Describes:
            (i.) the username for the user
            (ii.) the password for the user
            (iii.) the email for the user
            (iv.) the time that the user was registered to the site
            (v.) if the user is a site-admin
    """
    username: str
    password: str
    email: str
    # At the moment, the created_at field is not required
    # This will be updated to be required in the future
    # The datetime will be sent from the client
    created_at: Optional[datetime.datetime] = None
    is_admin: bool

class UserResponse(BaseModel):
    """
    The user response model.
        Describes:
            (i.) the unique id for the user
            (ii.) the username for the user
            (iii.) the email for the user
            (iv.) if the user is a site-admin
            (v.) the time that the user was registered to the site
    """
    id: int
    username: str
    email: str
    is_admin: bool
    created_at: datetime.datetime