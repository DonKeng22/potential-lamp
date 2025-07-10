"""
Task processing and status endpoints
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.task_service import TaskService

router = APIRouter()


@router.get("/{task_id}")
async def get_task_status(task_id: str, db: Session = Depends(get_db)):
    """Get the status of a processing task"""
    
    task_service = TaskService(db)
    task = task_service.get_task(task_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return {
        "task_id": task.task_id,
        "status": task.status,
        "progress": task.progress,
        "result": task.result,
        "error_message": task.error_message,
        "created_at": task.created_at,
        "updated_at": task.updated_at
    }


@router.get("/")
async def list_tasks(
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[str] = None,
    task_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List processing tasks with optional filtering"""
    
    task_service = TaskService(db)
    tasks = task_service.get_tasks(
        skip=skip,
        limit=limit,
        status=status_filter,
        task_type=task_type
    )
    
    return {
        "tasks": tasks,
        "count": len(tasks)
    }


@router.delete("/{task_id}")
async def cancel_task(task_id: str, db: Session = Depends(get_db)):
    """Cancel a processing task"""
    
    task_service = TaskService(db)
    success = await task_service.cancel_task(task_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or cannot be cancelled"
        )
    
    return {"message": f"Task {task_id} cancelled successfully"}