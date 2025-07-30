from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Boolean, ForeignKey, Enum 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, nullable=False)
    username = Column(String(155), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(155), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, server_default=f'{func.current_timestamp}')
    is_admin = Column(Boolean, default=False)

class Format(Base):
    __tablename__ = "format"
    id = Column(BigInteger, primary_key=True, nullable=False)
    medium = Column(String(55))

class ScheduledTime(Base):
    __tablename__ = "scheduled_time"
    id = Column(BigInteger, primary_key=True, nullable=False)
    when = Column(DateTime, nullable=False, server_default=f'{func.current_timestamp}')

class Platform(Base):
    __tablename__ = "platform"
    id = Column(BigInteger, primary_key=True, nullable=False)
    platform = Column(String(55))

class Interaction(Base):
    __tablename__ = "interaction"
    id = Column(BigInteger, primary_key=True, nullable=False)
    interaction = Column(String(100))

class Media(Base):
    __tablename__ = "media"
    id = Column(BigInteger, primary_key=True, nullable=False)
    filepath = Column(String(255))
    caption = Column(String(255))
    uploaded_at = Column(DateTime, nullable=False, server_default=f'{func.current_timestamp}')
    scheduled_time_id = Column(BigInteger, ForeignKey("scheduled_time.id"), nullable=False)
    platform_id = Column(BigInteger, ForeignKey("platform.id"), nullable=False)
    user_id = Column(BigInteger, ForeignKey("user.id"), nullable=False)

class PostStatus(enum.Enum):
    SCHEDULED = 1
    SUBMITTED = 2
    PENDING = 3
    POSTED= 4
    CANCELLED = 5
    FAILED = 6


class MediaPlatform(Base):
    __tablename__ = "media_platform"

    id = Column(BigInteger, primary_key=True, nullable=False)
    status = Column(Enum(PostStatus))
    media_id = Column(BigInteger, ForeignKey("media.id"), nullable=False)
    platform_id = Column(BigInteger, ForeignKey("platform.id"), nullable=False)

class MediaInteraction(Base):
    __tablename__ = "media_interaction"

    id = Column(BigInteger, primary_key=True, nullable=False)
    interaction_id = Column(BigInteger, ForeignKey("interaction.id"), nullable=False)
    media_platform_id = Column(BigInteger, ForeignKey("media_platform"), nullable=False)
    media_id = Column(BigInteger, ForeignKey("media.id"), nullable=False)
