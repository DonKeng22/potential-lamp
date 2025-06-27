"""
Computer Vision Models Package

This package contains computer vision models for field hockey event detection
and player tracking using YOLOv8 and other CV techniques.
"""

from .main import FieldHockeyCV, create_cv_pipeline

__all__ = ["FieldHockeyCV", "create_cv_pipeline"] 