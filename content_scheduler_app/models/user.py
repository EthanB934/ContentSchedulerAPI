from sqlalchemy import Column, Integer, BigInteger, String, DateTime, Boolean, ForeignKey, Enum 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

Base = declarative_base()

class User(Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True)
    username = Column(String(155), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    email = Column(String(155), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, server_default=func.current_timestamp)
    is_admin = Column(Boolean, default=False)