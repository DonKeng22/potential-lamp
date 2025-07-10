"""
SQLAlchemy models for storing detection results and events.
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class DetectionResult(Base):
    __tablename__ = 'detection_results'
    id = Column(Integer, primary_key=True, index=True)
    video_path = Column(String, index=True)
    frame = Column(Integer)
    detections = Column(JSON)  # List of detected objects for this frame
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class EventResult(Base):
    __tablename__ = 'event_results'
    id = Column(Integer, primary_key=True, index=True)
    video_path = Column(String, index=True)
    event_type = Column(String)
    frame = Column(Integer)
    details = Column(JSON)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
