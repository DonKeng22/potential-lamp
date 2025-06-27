"""
Streaming routes for video upload, live streaming, and video management.
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
import structlog
import os
import uuid
from datetime import datetime

from data.database import get_db
from data.config import settings

logger = structlog.get_logger()
router = APIRouter()

@router.post("/upload")
async def upload_video(
    file: UploadFile = File(...),
    title: str = Form(...),
    description: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Upload a video file for processing and streaming.
    
    Supports:
    - Direct file upload
    - YouTube link processing
    - Automatic HLS conversion
    """
    try:
        # Validate file format
        file_extension = os.path.splitext(file.filename)[1].lower()
        if file_extension not in settings.ALLOWED_VIDEO_FORMATS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format. Allowed: {settings.ALLOWED_VIDEO_FORMATS}"
            )
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        filename = f"{file_id}{file_extension}"
        file_path = os.path.join(settings.UPLOAD_DIR, filename)
        
        # Save uploaded file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        logger.info(f"Video uploaded successfully: {filename}")
        
        # TODO: Process video for HLS streaming
        # TODO: Extract metadata and create database record
        
        return {
            "message": "Video uploaded successfully",
            "file_id": file_id,
            "filename": filename,
            "title": title,
            "status": "processing"
        }
        
    except Exception as e:
        logger.error(f"Video upload failed: {e}")
        raise HTTPException(status_code=500, detail="Video upload failed")

@router.post("/youtube")
async def process_youtube_video(
    youtube_url: str = Form(...),
    title: str = Form(...),
    description: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Process a YouTube video for streaming.
    """
    try:
        # TODO: Download YouTube video
        # TODO: Process for HLS streaming
        # TODO: Create database record
        
        logger.info(f"YouTube video processing started: {youtube_url}")
        
        return {
            "message": "YouTube video processing started",
            "youtube_url": youtube_url,
            "title": title,
            "status": "processing"
        }
        
    except Exception as e:
        logger.error(f"YouTube video processing failed: {e}")
        raise HTTPException(status_code=500, detail="YouTube video processing failed")

@router.get("/list")
async def list_streams(
    page: int = 1,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    List available streams with pagination.
    """
    try:
        # TODO: Query database for streams
        # TODO: Implement pagination
        
        streams = [
            {
                "id": "sample-1",
                "title": "Sample Field Hockey Match",
                "description": "A sample field hockey match for testing",
                "status": "live",
                "created_at": datetime.now().isoformat(),
                "viewer_count": 150
            }
        ]
        
        return {
            "streams": streams,
            "page": page,
            "limit": limit,
            "total": len(streams)
        }
        
    except Exception as e:
        logger.error(f"Failed to list streams: {e}")
        raise HTTPException(status_code=500, detail="Failed to list streams")

@router.get("/{stream_id}")
async def get_stream(
    stream_id: str,
    db: Session = Depends(get_db)
):
    """
    Get stream details and HLS playlist.
    """
    try:
        # TODO: Query database for stream details
        # TODO: Return HLS playlist URL
        
        stream_info = {
            "id": stream_id,
            "title": "Sample Field Hockey Match",
            "description": "A sample field hockey match",
            "status": "live",
            "hls_url": f"/streams/{stream_id}/playlist.m3u8",
            "created_at": datetime.now().isoformat(),
            "viewer_count": 150
        }
        
        return stream_info
        
    except Exception as e:
        logger.error(f"Failed to get stream {stream_id}: {e}")
        raise HTTPException(status_code=404, detail="Stream not found")

@router.get("/{stream_id}/playlist.m3u8")
async def get_hls_playlist(
    stream_id: str,
    db: Session = Depends(get_db)
):
    """
    Get HLS playlist for streaming.
    """
    try:
        # TODO: Generate or retrieve HLS playlist
        # TODO: Return proper HLS content
        
        playlist_content = f"""#EXTM3U
#EXT-X-VERSION:3
#EXT-X-TARGETDURATION:6
#EXT-X-MEDIA-SEQUENCE:0
#EXTINF:6.0,
/streams/{stream_id}/segment_0.ts
#EXTINF:6.0,
/streams/{stream_id}/segment_1.ts
#EXT-X-ENDLIST"""
        
        return StreamingResponse(
            iter([playlist_content]),
            media_type="application/vnd.apple.mpegurl"
        )
        
    except Exception as e:
        logger.error(f"Failed to get HLS playlist for {stream_id}: {e}")
        raise HTTPException(status_code=404, detail="Playlist not found")

@router.delete("/{stream_id}")
async def delete_stream(
    stream_id: str,
    db: Session = Depends(get_db)
):
    """
    Delete a stream and associated files.
    """
    try:
        # TODO: Delete stream from database
        # TODO: Remove associated files
        
        logger.info(f"Stream deleted: {stream_id}")
        
        return {"message": "Stream deleted successfully"}
        
    except Exception as e:
        logger.error(f"Failed to delete stream {stream_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete stream") 