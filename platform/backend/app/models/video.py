"""
Database models for video processing and analysis
"""
import datetime
from sqlalchemy import Column, Integer, String, DateTime, JSON, Text, Boolean, Float
from app.core.database import Base


class Video(Base):
    """Video uploads and metadata"""
    __tablename__ = "videos"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    original_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer)
    content_type = Column(String)
    status = Column(String, default="uploaded")  # uploaded, processing, completed, failed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class ProcessingTask(Base):
    """Background processing tasks"""
    __tablename__ = "processing_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, unique=True, index=True, nullable=False)
    video_id = Column(Integer, nullable=True)
    task_type = Column(String, nullable=False)  # video_analysis, annotation, training
    status = Column(String, default="pending")  # pending, running, completed, failed
    progress = Column(Float, default=0.0)
    result = Column(JSON)
    error_message = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)


class Detection(Base):
    """Object detection results"""
    __tablename__ = "detections"
    
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, nullable=False)
    frame_number = Column(Integer, nullable=False)
    objects = Column(JSON)  # List of detected objects with bounding boxes and confidence
    timestamp = Column(Float)  # Frame timestamp in seconds
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Event(Base):
    """Game events detected in videos"""
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, nullable=False)
    event_type = Column(String, nullable=False)  # goal, card, corner, penalty
    frame_number = Column(Integer, nullable=False)
    timestamp = Column(Float)  # Event timestamp in seconds
    confidence = Column(Float)
    details = Column(JSON)  # Additional event details
    created_at = Column(DateTime, default=datetime.datetime.utcnow)


class Annotation(Base):
    """Manual annotations for training"""
    __tablename__ = "annotations"
    
    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(Integer, nullable=False)
    frame_number = Column(Integer, nullable=False)
    annotation_type = Column(String, nullable=False)  # object, event, field_boundary
    data = Column(JSON, nullable=False)  # Annotation data (bounding boxes, labels, etc.)
    annotator = Column(String)  # Who created the annotation
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)