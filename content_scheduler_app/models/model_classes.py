"""
This module will store all database models so that 
I am not importing much of the same classes from sqlalchemy.
These models are being packaged in the __init__.py of this directory
to be distributed to other modules that will perform queries on the database
"""
# SQLalchemy gives the means to create tables 
# With datatypes and an in-line declarative base
# For the database models to inherit
from sqlalchemy import Column, BigInteger, String, DateTime, Boolean, ForeignKey, Enum 
from sqlalchemy.ext.declarative import declarative_base
import enum

# Initializes an instance of the Base class that for models' inheritance
Base = declarative_base()

class User(Base):
    """ 
    The user table.
    
        Describes:
            (i.) the unique username for the user
            (ii.) the user's obfuscated password
            (iii.) the unique email of the user
            (iv.) the time that the user was registered to the site
            (v.) if the user is a site-admin
    """

    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, nullable=False)
    username = Column(String(155), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(155), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=True)
    is_admin = Column(Boolean, default=False)

class Format(Base):
    """
    The format table. 
    
        Describes:
            (i.) a medium (i.e. video, picture)
    """
    # Might update to contain file extensions instead
    __tablename__ = "format"
    id = Column(BigInteger, primary_key=True, nullable=False)
    format = Column(String(55))

class ScheduledTime(Base):
    """
    The scheduled time table. 
    
        Describes: 
            (i.) the time that a medium is expected to deploy
    """

    __tablename__ = "scheduled_time"
    id = Column(BigInteger, primary_key=True, nullable=False)
    when = Column(DateTime, nullable=True)

class Platform(Base):
    """
    The platform table.
    
        Describes:
            (i.) to which platform a medium may be deployed
    """

    __tablename__ = "platform"
    id = Column(BigInteger, primary_key=True, nullable=False)
    platform = Column(String(55))

class Interaction(Base):
    """
    The interaction table. 
    
        Describes:
            (i.) which reaction was received on a medium after deployment
    """

    __tablename__ = "interaction"
    id = Column(BigInteger, primary_key=True, nullable=False)
    interaction = Column(String(100))

class Medium(Base):
    """
    The medium table.
        Describes:
            (i.) where the medium will be saved
            (ii.) when the medium was uploaded to the site
            (iii.) when the medium is/was deployed to a platform
            (iv.) what type of medium it is
            (v.) which user owns it
    """

    __tablename__ = "medium"
    id = Column(BigInteger, primary_key=True, nullable=False)
    filepath = Column(String(255))
    caption = Column(String(255))
    uploaded_at = Column(DateTime, nullable=True)
    scheduled_time_id = Column(BigInteger, ForeignKey("scheduled_time.id"), nullable=False)
    format_id = Column(BigInteger, ForeignKey("format.id"), nullable=False)
    user_id = Column(BigInteger, ForeignKey("user.id"), nullable=False)

class PostStatus(enum.Enum):
    """
    The medium post status enumerator.

        Describes:
            What the current status of any created medium is.
            1. The medium is scheduled for deployment (waiting to deploy)
            2. The medium has been submitted to the platform for deployment
            3. The medium is being reviewed by platform, pending
            4. The medium has successfully been deployed to the platform
            5. The medium's deployment has been cancelled by site-user
            6. The medium's deployment has been refused by the platform
            7. The medium's deployment has failed due to network error or site error
    """
    SCHEDULED = 1
    SUBMITTED = 2
    PENDING = 3
    POSTED= 4
    CANCELLED = 5
    REJECTED = 6
    FAILED =  7

class MediaPlatform(Base):
    """
    The media platform table, a relationship table between medium and platform

        Describes:
            (i.) the status of the medium on a particular platform using PostStatus Enum
            (ii.) which medium
            (iii.) which platform
    """

    __tablename__ = "media_platform"

    id = Column(BigInteger, primary_key=True, nullable=False)
    status = Column(Enum(PostStatus))
    media_id = Column(BigInteger, ForeignKey("media.id"), nullable=False)
    platform_id = Column(BigInteger, ForeignKey("platform.id"), nullable=False)

class MediaInteraction(Base):
    """
    The media interaction table, a relational table.

        Describes:

            (i.) which type of reaction the medium received
            (ii.) which media and which platform relationship
    """
    __tablename__ = "media_interaction"

    id = Column(BigInteger, primary_key=True, nullable=False)
    interaction_id = Column(BigInteger, ForeignKey("interaction.id"), nullable=False)
    media_platform_id = Column(BigInteger, ForeignKey("media_platform.id"), nullable=False)
