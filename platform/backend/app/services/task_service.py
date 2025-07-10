"""
Task processing service
"""
import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.video import ProcessingTask
from app.services.celery_tasks import process_video_task


class TaskService:
    """Service for handling background tasks"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def create_processing_task(
        self,
        video_id: int,
        task_type: str
    ) -> ProcessingTask:
        """Create a new processing task"""
        
        task_id = str(uuid.uuid4())
        
        # Create database record
        task = ProcessingTask(
            task_id=task_id,
            video_id=video_id,
            task_type=task_type,
            status="pending"
        )
        
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        
        # Submit to Celery (for now, just a placeholder)
        # In a full implementation, this would dispatch to Celery workers
        try:
            # process_video_task.delay(task_id, video_id, task_type)
            self.update_task_status(task_id, "queued")
        except Exception as e:
            self.update_task_status(task_id, "failed", error_message=str(e))
        
        return task
    
    def get_task(self, task_id: str) -> Optional[ProcessingTask]:
        """Get task by ID"""
        return self.db.query(ProcessingTask).filter(ProcessingTask.task_id == task_id).first()
    
    def get_tasks(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        task_type: Optional[str] = None
    ) -> List[ProcessingTask]:
        """Get list of tasks with optional filtering"""
        
        query = self.db.query(ProcessingTask)
        
        if status:
            query = query.filter(ProcessingTask.status == status)
        
        if task_type:
            query = query.filter(ProcessingTask.task_type == task_type)
        
        return query.offset(skip).limit(limit).order_by(ProcessingTask.created_at.desc()).all()
    
    def update_task_status(
        self,
        task_id: str,
        status: str,
        progress: Optional[float] = None,
        result: Optional[dict] = None,
        error_message: Optional[str] = None
    ) -> Optional[ProcessingTask]:
        """Update task status and progress"""
        
        task = self.get_task(task_id)
        if task:
            task.status = status
            if progress is not None:
                task.progress = progress
            if result is not None:
                task.result = result
            if error_message is not None:
                task.error_message = error_message
            
            self.db.commit()
            self.db.refresh(task)
        
        return task
    
    async def cancel_task(self, task_id: str) -> bool:
        """Cancel a processing task"""
        
        task = self.get_task(task_id)
        if task and task.status in ["pending", "queued", "running"]:
            task.status = "cancelled"
            self.db.commit()
            
            # In a full implementation, also cancel the Celery task
            # celery_app.control.revoke(task_id, terminate=True)
            
            return True
        
        return False