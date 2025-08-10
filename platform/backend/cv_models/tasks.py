
from celery import Celery
from ultralytics import YOLO
import cv2
from cv_models.events import EventDetector
from data.models import DetectionResult, EventResult
from data.db import SessionLocal
import json
import time

# Initialize Celery
celery_app = Celery('video_processor', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

@celery_app.task
def process_video_for_detection(video_path: str):
    model = YOLO('yolov8n.pt')
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return {"status": "error", "message": "Could not open video"}

    results = []
    frame_idx = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        # YOLOv8 inference
        preds = model(frame)
        # Convert YOLO output to a serializable format (dummy structure for now)
        objects = []
        for pred in preds:
            # Each pred is a Results object; convert to dict
            for box in pred.boxes:
                cls = int(box.cls[0]) if hasattr(box, 'cls') else None
                conf = float(box.conf[0]) if hasattr(box, 'conf') else None
                xyxy = box.xyxy[0].tolist() if hasattr(box, 'xyxy') else None
                objects.append({
                    'class': model.names[cls] if cls is not None and hasattr(model, 'names') else str(cls),
                    'conf': conf,
                    'bbox': xyxy
                })
        det = {'frame': frame_idx, 'objects': objects}
        results.append(det)
        frame_idx += 1
    cap.release()

    # Store detections in DB
    db = SessionLocal()
    try:
        for det in results:
            db.add(DetectionResult(video_path=video_path, frame=det['frame'], detections=det['objects']))
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"DB error: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

    # Event detection
    event_detector = EventDetector()
    events = event_detector.detect_events(results)

    # Store events in DB
    db = SessionLocal()
    try:
        for event in events:
            db.add(EventResult(video_path=video_path, event_type=event['type'], frame=event['frame'], details=event['details']))
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"DB error (events): {e}")
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

    return {"status": "completed", "detections": results, "events": events}


@celery_app.task(bind=True)
def train_model(self, data_path: str):
    """Dummy long-running training task.

    Args:
        data_path: Location of the training data or identifier.

    This task simulates model training by sleeping and updating progress
    so the API can report intermediate states back to the client.
    """
    steps = 5
    for step in range(steps):
        self.update_state(state="PROGRESS", meta={"status": f"step {step + 1}/{steps}"})
        time.sleep(1)
    # In a real implementation this would return the path to the trained model
    return {"status": "completed", "model_path": f"{data_path}/model.pt"}

