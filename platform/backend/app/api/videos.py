"""
Video upload and processing endpoints
"""
import os
import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import settings
from app.models.video import Video, ProcessingTask
from app.services.video_service import VideoService
from app.services.task_service import TaskService

router = APIRouter()


@router.post("/upload")
async def upload_video(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload a video file for processing"""
    
    # Validate file
    if not file.content_type or not file.content_type.startswith('video/'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only video files are allowed"
        )
    
    # Read the entire file to enforce upload size limits since
    # UploadFile doesn't expose a reliable ``size`` attribute.
    content = await file.read()
    if len(content) > settings.max_file_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds maximum allowed size of {settings.max_file_size} bytes",
        )
    file.file.seek(0)

    video_service = VideoService(db)
    video = await video_service.save_uploaded_file(file)
    
    return {
        "id": video.id,
        "filename": video.filename,
        "status": video.status,
        "message": "Video uploaded successfully"
    }


@router.get("/")
async def list_videos(
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List uploaded videos with optional filtering"""
    
    video_service = VideoService(db)
    videos = video_service.get_videos(skip=skip, limit=limit, status=status_filter)
    
    return {
        "videos": videos,
        "count": len(videos)
    }


@router.get("/{video_id}")
async def get_video(video_id: int, db: Session = Depends(get_db)):
    """Get video details by ID"""
    
    video_service = VideoService(db)
    video = video_service.get_video(video_id)
    
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found"
        )
    
    return video


@router.post("/{video_id}/process")
async def process_video(
    video_id: int,
    process_type: str = "analysis",
    db: Session = Depends(get_db)
):
    """Start processing a video"""
    
    video_service = VideoService(db)
    video = video_service.get_video(video_id)
    
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found"
        )
    
    task_service = TaskService(db)
    task = await task_service.create_processing_task(
        video_id=video_id,
        task_type=process_type
    )
    
    return {
        "task_id": task.task_id,
        "status": task.status,
        "message": f"Processing started for video {video_id}"
    }


@router.get("/{video_id}/detections")
async def get_video_detections(
    video_id: int,
    frame_start: Optional[int] = None,
    frame_end: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get detection results for a video.

    The optional ``frame_start`` and ``frame_end`` query parameters can be
    used to limit the returned detections to a specific inclusive range of
    frame numbers. Only detections with ``frame_number`` greater than or
    equal to ``frame_start`` and less than or equal to ``frame_end`` are
    included in the response.
    """
    
    video_service = VideoService(db)
    detections = video_service.get_detections(
        video_id=video_id,
        frame_start=frame_start,
        frame_end=frame_end
    )
    
    return {
        "video_id": video_id,
        "detections": detections
    }


@router.get("/{video_id}/events")
async def get_video_events(
    video_id: int,
    event_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get detected events for a video"""
    
    video_service = VideoService(db)
    events = video_service.get_events(
        video_id=video_id,
        event_type=event_type
    )
    
    return {
        "video_id": video_id,
        "events": events
    }
