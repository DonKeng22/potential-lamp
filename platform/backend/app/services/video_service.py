"""
Video processing service
"""
import os
import uuid
from typing import List, Optional
from fastapi import UploadFile
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.video import Video, Detection, Event


class VideoService:
    """Service for handling video operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def save_uploaded_file(self, file: UploadFile) -> Video:
        """Save uploaded video file and create database record"""
        
        # Ensure upload directory exists
        os.makedirs(settings.upload_dir, exist_ok=True)
        
        # Generate unique filename
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(settings.upload_dir, unique_filename)
        
        # Save file to disk
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Create database record
        video = Video(
            filename=unique_filename,
            original_name=file.filename,
            file_path=file_path,
            file_size=len(content),
            content_type=file.content_type,
            status="uploaded"
        )
        
        self.db.add(video)
        self.db.commit()
        self.db.refresh(video)
        
        return video
    
    def get_video(self, video_id: int) -> Optional[Video]:
        """Get video by ID"""
        return self.db.query(Video).filter(Video.id == video_id).first()
    
    def get_videos(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None
    ) -> List[Video]:
        """Get list of videos with optional filtering"""
        
        query = self.db.query(Video)
        
        if status:
            query = query.filter(Video.status == status)
        
        return query.offset(skip).limit(limit).all()
    
    def update_video_status(self, video_id: int, status: str) -> Optional[Video]:
        """Update video processing status"""
        
        video = self.get_video(video_id)
        if video:
            video.status = status
            self.db.commit()
            self.db.refresh(video)
        
        return video
    
    def get_detections(
        self,
        video_id: int,
        frame_start: Optional[int] = None,
        frame_end: Optional[int] = None
    ) -> List[Detection]:
        """Get detection results for a video"""
        
        query = self.db.query(Detection).filter(Detection.video_id == video_id)
        
        if frame_start is not None:
            query = query.filter(Detection.frame_number >= frame_start)
        
        if frame_end is not None:
            query = query.filter(Detection.frame_number <= frame_end)
        
        return query.order_by(Detection.frame_number).all()
    
    def get_events(
        self,
        video_id: int,
        event_type: Optional[str] = None
    ) -> List[Event]:
        """Get detected events for a video"""
        
        query = self.db.query(Event).filter(Event.video_id == video_id)
        
        if event_type:
            query = query.filter(Event.event_type == event_type)
        
        return query.order_by(Event.timestamp).all()
    
    def add_detection(self, video_id: int, frame_number: int, objects: dict, timestamp: float) -> Detection:
        """Add detection result to database"""
        
        detection = Detection(
            video_id=video_id,
            frame_number=frame_number,
            objects=objects,
            timestamp=timestamp
        )
        
        self.db.add(detection)
        self.db.commit()
        self.db.refresh(detection)
        
        return detection
    
    def add_event(
        self,
        video_id: int,
        event_type: str,
        frame_number: int,
        timestamp: float,
        confidence: float,
        details: dict
    ) -> Event:
        """Add detected event to database"""
        
        event = Event(
            video_id=video_id,
            event_type=event_type,
            frame_number=frame_number,
            timestamp=timestamp,
            confidence=confidence,
            details=details
        )
        
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        
        return event