# models.py
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean
from sqlalchemy.sql import func
from db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(Integer, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    city = Column(String, nullable=True)
    subscribed = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    tg_id = Column(Integer, nullable=True)
    phone = Column(String, nullable=True)
    name = Column(String, nullable=True)
    city = Column(String, nullable=True)
    message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Broadcast(Base):
    __tablename__ = "broadcasts"
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
