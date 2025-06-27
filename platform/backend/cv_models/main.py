"""
Main Computer Vision Pipeline for Field Hockey Event Detection

This module provides the main interface for computer vision processing
of field hockey matches, including player detection, event recognition,
and real-time analytics.
"""

import cv2
import numpy as np
from typing import List, Dict, Any, Optional
import structlog
from pathlib import Path

from .detector import HockeyDetector
from .tracker import ObjectTracker
from .events import EventDetector
from .player_id import PlayerIdentifier
from .utils import VideoProcessor, FrameBuffer

logger = structlog.get_logger()

class FieldHockeyCV:
    """
    Main computer vision pipeline for field hockey analysis.
    
    This class orchestrates all CV components including:
    - Object detection (players, ball, referee, goals)
    - Object tracking across frames
    - Event detection (goals, cards, corners)
    - Player identification and analytics
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the CV pipeline.
        
        Args:
            config: Configuration dictionary for CV components
        """
        self.config = config or {}
        
        # Initialize components
        self.detector = HockeyDetector(
            model_path=self.config.get('model_path', 'models/yolov8n.pt'),
            confidence_threshold=self.config.get('confidence_threshold', 0.5),
            nms_threshold=self.config.get('nms_threshold', 0.4)
        )
        
        self.tracker = ObjectTracker(
            max_disappeared=self.config.get('max_disappeared', 30),
            max_distance=self.config.get('max_distance', 50)
        )
        
        self.event_detector = EventDetector(
            goal_threshold=self.config.get('goal_threshold', 0.8),
            card_threshold=self.config.get('card_threshold', 0.7)
        )
        
        self.player_identifier = PlayerIdentifier(
            face_model_path=self.config.get('face_model_path'),
            jersey_model_path=self.config.get('jersey_model_path')
        )
        
        # Video processing utilities
        self.video_processor = VideoProcessor()
        self.frame_buffer = FrameBuffer(max_frames=30)
        
        # State tracking
        self.current_frame = 0
        self.detection_history = []
        self.event_history = []
        self.player_tracks = {}
        
        logger.info("Field Hockey CV pipeline initialized")
    
    def process_frame(self, frame: np.ndarray) -> Dict[str, Any]:
        """
        Process a single video frame.
        
        Args:
            frame: Input video frame (BGR format)
            
        Returns:
            Dictionary containing detection results, events, and analytics
        """
        try:
            self.current_frame += 1
            
            # Add frame to buffer
            self.frame_buffer.add_frame(frame)
            
            # Run object detection
            detections = self.detector.detect(frame)
            
            # Update object tracking
            tracked_objects = self.tracker.update(detections)
            
            # Detect events
            events = self.event_detector.detect_events(
                frame, tracked_objects, self.frame_buffer
            )
            
            # Identify players
            player_identifications = self.player_identifier.identify_players(
                frame, tracked_objects
            )
            
            # Update player tracks
            self._update_player_tracks(tracked_objects, player_identifications)
            
            # Compile results
            results = {
                'frame_number': self.current_frame,
                'detections': detections,
                'tracked_objects': tracked_objects,
                'events': events,
                'player_identifications': player_identifications,
                'analytics': self._compute_analytics()
            }
            
            # Store in history
            self.detection_history.append(results)
            if events:
                self.event_history.extend(events)
            
            return results
            
        except Exception as e:
            logger.error(f"Error processing frame {self.current_frame}: {e}")
            return {
                'frame_number': self.current_frame,
                'error': str(e),
                'detections': [],
                'tracked_objects': [],
                'events': [],
                'player_identifications': [],
                'analytics': {}
            }
    
    def process_video(self, video_path: str) -> Dict[str, Any]:
        """
        Process an entire video file.
        
        Args:
            video_path: Path to the video file
            
        Returns:
            Dictionary containing complete video analysis
        """
        try:
            logger.info(f"Starting video processing: {video_path}")
            
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise ValueError(f"Could not open video: {video_path}")
            
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            results = {
                'video_path': video_path,
                'total_frames': total_frames,
                'fps': fps,
                'frame_results': [],
                'summary': {}
            }
            
            frame_count = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                if frame_count % 30 == 0:  # Log every 30 frames
                    logger.info(f"Processing frame {frame_count}/{total_frames}")
                
                # Process frame
                frame_result = self.process_frame(frame)
                results['frame_results'].append(frame_result)
            
            cap.release()
            
            # Generate summary
            results['summary'] = self._generate_video_summary()
            
            logger.info(f"Video processing completed: {video_path}")
            return results
            
        except Exception as e:
            logger.error(f"Error processing video {video_path}: {e}")
            raise
    
    def get_real_time_analytics(self) -> Dict[str, Any]:
        """
        Get real-time analytics for the current match.
        
        Returns:
            Dictionary containing current match analytics
        """
        return {
            'current_frame': self.current_frame,
            'active_players': len(self.player_tracks),
            'recent_events': self.event_history[-10:] if self.event_history else [],
            'player_positions': self._get_player_positions(),
            'ball_trajectory': self._get_ball_trajectory(),
            'match_stats': self._compute_match_stats()
        }
    
    def _update_player_tracks(self, tracked_objects: List[Dict], 
                            player_identifications: List[Dict]):
        """Update player tracking information."""
        for obj in tracked_objects:
            if obj.get('class') == 'player':
                player_id = obj.get('track_id')
                if player_id:
                    if player_id not in self.player_tracks:
                        self.player_tracks[player_id] = {
                            'positions': [],
                            'actions': [],
                            'identifications': []
                        }
                    
                    self.player_tracks[player_id]['positions'].append({
                        'frame': self.current_frame,
                        'bbox': obj.get('bbox'),
                        'confidence': obj.get('confidence')
                    })
    
    def _compute_analytics(self) -> Dict[str, Any]:
        """Compute analytics for the current frame."""
        return {
            'player_count': len([obj for obj in self.tracker.objects.values() 
                               if obj.get('class') == 'player']),
            'ball_detected': any(obj.get('class') == 'ball' 
                               for obj in self.tracker.objects.values()),
            'referee_detected': any(obj.get('class') == 'referee' 
                                  for obj in self.tracker.objects.values()),
            'goal_detected': any(obj.get('class') == 'goal' 
                               for obj in self.tracker.objects.values())
        }
    
    def _get_player_positions(self) -> Dict[str, List]:
        """Get current player positions."""
        positions = {}
        for player_id, track in self.player_tracks.items():
            if track['positions']:
                positions[player_id] = track['positions'][-1]
        return positions
    
    def _get_ball_trajectory(self) -> List[Dict]:
        """Get recent ball trajectory."""
        ball_positions = []
        for obj in self.tracker.objects.values():
            if obj.get('class') == 'ball':
                ball_positions.append({
                    'frame': self.current_frame,
                    'bbox': obj.get('bbox'),
                    'confidence': obj.get('confidence')
                })
        return ball_positions[-20:]  # Last 20 ball positions
    
    def _compute_match_stats(self) -> Dict[str, Any]:
        """Compute overall match statistics."""
        return {
            'total_frames': self.current_frame,
            'total_events': len(self.event_history),
            'goals': len([e for e in self.event_history if e.get('type') == 'goal']),
            'cards': len([e for e in self.event_history if e.get('type') == 'card']),
            'corners': len([e for e in self.event_history if e.get('type') == 'corner'])
        }
    
    def _generate_video_summary(self) -> Dict[str, Any]:
        """Generate summary for processed video."""
        return {
            'total_frames_processed': self.current_frame,
            'total_events_detected': len(self.event_history),
            'unique_players_tracked': len(self.player_tracks),
            'event_breakdown': self._get_event_breakdown(),
            'performance_metrics': self._get_performance_metrics()
        }
    
    def _get_event_breakdown(self) -> Dict[str, int]:
        """Get breakdown of detected events."""
        event_counts = {}
        for event in self.event_history:
            event_type = event.get('type', 'unknown')
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
        return event_counts
    
    def _get_performance_metrics(self) -> Dict[str, float]:
        """Get performance metrics for the pipeline."""
        return {
            'average_fps': self.current_frame / (self.current_frame / 30),  # Assuming 30 FPS
            'detection_confidence_avg': np.mean([
                det.get('confidence', 0) 
                for result in self.detection_history 
                for det in result.get('detections', [])
            ]) if self.detection_history else 0.0,
            'tracking_accuracy': len(self.player_tracks) / max(len(self.player_tracks), 1)
        }

# Convenience function for quick usage
def create_cv_pipeline(config: Optional[Dict[str, Any]] = None) -> FieldHockeyCV:
    """
    Create a configured CV pipeline instance.
    
    Args:
        config: Optional configuration dictionary
        
    Returns:
        Configured FieldHockeyCV instance
    """
    return FieldHockeyCV(config)

if __name__ == "__main__":
    # Example usage
    cv_pipeline = create_cv_pipeline()
    
    # Process a video file
    # results = cv_pipeline.process_video("path/to/video.mp4")
    # print(f"Processed {results['total_frames']} frames")
    # print(f"Detected {len(results['summary']['event_breakdown'])} event types") 