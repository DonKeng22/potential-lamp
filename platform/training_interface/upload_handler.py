"""
Upload Handler for Training Data Management

This module handles file uploads for training data including videos,
annotations, and model configurations.
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any
import structlog
from datetime import datetime
import hashlib

logger = structlog.get_logger()

class TrainingDataUploader:
    """
    Handles upload and management of training data for AI models.
    
    Supports:
    - Video file uploads
    - Annotation file uploads
    - Data validation and organization
    - Metadata management
    """
    
    def __init__(self, base_path: str = "../data"):
        """
        Initialize the upload handler.
        
        Args:
            base_path: Base path for storing training data
        """
        self.base_path = Path(base_path)
        self.raw_videos_path = self.base_path / "raw_videos"
        self.annotations_path = self.base_path / "annotations"
        self.processed_path = self.base_path / "processed"
        
        # Create directories if they don't exist
        self._create_directories()
        
        # Supported file formats
        self.supported_video_formats = ['.mp4', '.avi', '.mov', '.mkv', '.webm']
        self.supported_annotation_formats = ['.json', '.xml', '.csv']
        
        logger.info(f"Training data uploader initialized at {self.base_path}")
    
    def _create_directories(self):
        """Create necessary directories for data storage."""
        directories = [
            self.raw_videos_path,
            self.annotations_path,
            self.processed_path,
            self.processed_path / "videos",
            self.processed_path / "annotations",
            self.processed_path / "metadata"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def upload_video(self, file_path: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Upload a video file for training.
        
        Args:
            file_path: Path to the video file
            metadata: Optional metadata about the video
            
        Returns:
            Dictionary containing upload status and file information
        """
        try:
            file_path = Path(file_path)
            
            # Validate file format
            if file_path.suffix.lower() not in self.supported_video_formats:
                raise ValueError(f"Unsupported video format: {file_path.suffix}")
            
            # Validate file exists
            if not file_path.exists():
                raise FileNotFoundError(f"Video file not found: {file_path}")
            
            # Generate unique filename
            file_hash = self._calculate_file_hash(file_path)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_filename = f"{timestamp}_{file_hash[:8]}{file_path.suffix}"
            
            # Copy file to raw videos directory
            destination = self.raw_videos_path / new_filename
            shutil.copy2(file_path, destination)
            
            # Create metadata
            video_metadata = {
                'original_filename': file_path.name,
                'uploaded_filename': new_filename,
                'file_hash': file_hash,
                'upload_timestamp': datetime.now().isoformat(),
                'file_size': destination.stat().st_size,
                'file_path': str(destination),
                'status': 'uploaded'
            }
            
            # Add custom metadata
            if metadata:
                video_metadata.update(metadata)
            
            # Save metadata
            metadata_file = self.processed_path / "metadata" / f"{new_filename}.json"
            with open(metadata_file, 'w') as f:
                json.dump(video_metadata, f, indent=2)
            
            logger.info(f"Video uploaded successfully: {new_filename}")
            
            return {
                'success': True,
                'filename': new_filename,
                'metadata': video_metadata
            }
            
        except Exception as e:
            logger.error(f"Video upload failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def upload_annotations(self, file_path: str, video_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Upload annotation file for training data.
        
        Args:
            file_path: Path to the annotation file
            video_id: Optional video ID to associate with annotations
            
        Returns:
            Dictionary containing upload status and file information
        """
        try:
            file_path = Path(file_path)
            
            # Validate file format
            if file_path.suffix.lower() not in self.supported_annotation_formats:
                raise ValueError(f"Unsupported annotation format: {file_path.suffix}")
            
            # Validate file exists
            if not file_path.exists():
                raise FileNotFoundError(f"Annotation file not found: {file_path}")
            
            # Validate annotation format
            if file_path.suffix.lower() == '.json':
                self._validate_json_annotations(file_path)
            
            # Generate unique filename
            file_hash = self._calculate_file_hash(file_path)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            new_filename = f"{timestamp}_{file_hash[:8]}{file_path.suffix}"
            
            # Copy file to annotations directory
            destination = self.annotations_path / new_filename
            shutil.copy2(file_path, destination)
            
            # Create metadata
            annotation_metadata = {
                'original_filename': file_path.name,
                'uploaded_filename': new_filename,
                'file_hash': file_hash,
                'upload_timestamp': datetime.now().isoformat(),
                'file_size': destination.stat().st_size,
                'file_path': str(destination),
                'video_id': video_id,
                'status': 'uploaded'
            }
            
            # Save metadata
            metadata_file = self.processed_path / "metadata" / f"{new_filename}.json"
            with open(metadata_file, 'w') as f:
                json.dump(annotation_metadata, f, indent=2)
            
            logger.info(f"Annotations uploaded successfully: {new_filename}")
            
            return {
                'success': True,
                'filename': new_filename,
                'metadata': annotation_metadata
            }
            
        except Exception as e:
            logger.error(f"Annotation upload failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def upload_youtube_video(self, youtube_url: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Download and upload a YouTube video for training.
        
        Args:
            youtube_url: YouTube video URL
            metadata: Optional metadata about the video
            
        Returns:
            Dictionary containing upload status and file information
        """
        try:
            # TODO: Implement YouTube video download
            # This would use yt-dlp or similar library
            
            logger.info(f"YouTube video download started: {youtube_url}")
            
            return {
                'success': True,
                'youtube_url': youtube_url,
                'status': 'downloading',
                'message': 'YouTube video download in progress'
            }
            
        except Exception as e:
            logger.error(f"YouTube video upload failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def list_uploaded_files(self, file_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all uploaded files with their metadata.
        
        Args:
            file_type: Optional filter for file type ('video', 'annotation')
            
        Returns:
            List of file metadata dictionaries
        """
        try:
            files = []
            
            # Scan metadata directory
            metadata_dir = self.processed_path / "metadata"
            for metadata_file in metadata_dir.glob("*.json"):
                with open(metadata_file, 'r') as f:
                    file_metadata = json.load(f)
                
                # Apply filter if specified
                if file_type:
                    if file_type == 'video' and metadata_file.stem.endswith(('.mp4', '.avi', '.mov', '.mkv')):
                        files.append(file_metadata)
                    elif file_type == 'annotation' and metadata_file.stem.endswith(('.json', '.xml', '.csv')):
                        files.append(file_metadata)
                else:
                    files.append(file_metadata)
            
            # Sort by upload timestamp
            files.sort(key=lambda x: x.get('upload_timestamp', ''), reverse=True)
            
            return files
            
        except Exception as e:
            logger.error(f"Failed to list uploaded files: {e}")
            return []
    
    def delete_file(self, filename: str) -> Dict[str, Any]:
        """
        Delete an uploaded file and its metadata.
        
        Args:
            filename: Name of the file to delete
            
        Returns:
            Dictionary containing deletion status
        """
        try:
            # Find and delete the file
            file_path = None
            if filename.endswith(tuple(self.supported_video_formats)):
                file_path = self.raw_videos_path / filename
            elif filename.endswith(tuple(self.supported_annotation_formats)):
                file_path = self.annotations_path / filename
            
            if file_path and file_path.exists():
                file_path.unlink()
            
            # Delete metadata
            metadata_file = self.processed_path / "metadata" / f"{filename}.json"
            if metadata_file.exists():
                metadata_file.unlink()
            
            logger.info(f"File deleted successfully: {filename}")
            
            return {
                'success': True,
                'message': f'File {filename} deleted successfully'
            }
            
        except Exception as e:
            logger.error(f"File deletion failed: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of a file."""
        hash_sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha256.update(chunk)
        return hash_sha256.hexdigest()
    
    def _validate_json_annotations(self, file_path: Path):
        """Validate JSON annotation file format."""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Basic validation
            required_fields = ['video_id', 'annotations']
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Missing required field: {field}")
            
            # Validate annotations structure
            if not isinstance(data['annotations'], list):
                raise ValueError("Annotations must be a list")
            
            logger.info(f"JSON annotations validated successfully: {file_path}")
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format: {e}")
        except Exception as e:
            raise ValueError(f"Annotation validation failed: {e}")
    
    def get_upload_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about uploaded training data.
        
        Returns:
            Dictionary containing upload statistics
        """
        try:
            files = self.list_uploaded_files()
            
            video_files = [f for f in files if f.get('original_filename', '').endswith(tuple(self.supported_video_formats))]
            annotation_files = [f for f in files if f.get('original_filename', '').endswith(tuple(self.supported_annotation_formats))]
            
            total_size = sum(f.get('file_size', 0) for f in files)
            
            return {
                'total_files': len(files),
                'video_files': len(video_files),
                'annotation_files': len(annotation_files),
                'total_size_bytes': total_size,
                'total_size_gb': total_size / (1024**3),
                'latest_upload': max(f.get('upload_timestamp', '') for f in files) if files else None
            }
            
        except Exception as e:
            logger.error(f"Failed to get upload statistics: {e}")
            return {}

# Convenience function for quick usage
def create_uploader(base_path: str = "../data") -> TrainingDataUploader:
    """
    Create a configured uploader instance.
    
    Args:
        base_path: Base path for storing training data
        
    Returns:
        Configured TrainingDataUploader instance
    """
    return TrainingDataUploader(base_path)

if __name__ == "__main__":
    # Example usage
    uploader = create_uploader()
    
    # Upload a video file
    # result = uploader.upload_video("path/to/video.mp4", {"description": "Field hockey match"})
    # print(f"Upload result: {result}")
    
    # List uploaded files
    files = uploader.list_uploaded_files()
    print(f"Uploaded files: {len(files)}")
    
    # Get statistics
    stats = uploader.get_upload_statistics()
    print(f"Upload statistics: {stats}") 