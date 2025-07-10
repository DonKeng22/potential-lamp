from fastapi import APIRouter, UploadFile, File
import shutil
from cv_models.tasks import process_video_for_detection

router = APIRouter()

@router.post("/upload-video")
async def upload_video(file: UploadFile = File(...)):
    video_path = f"data/raw_videos/{file.filename}"
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    task = process_video_for_detection.delay(video_path)
    return {"filename": file.filename, "task_id": task.id}

@router.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    task = process_video_for_detection.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'status': task.info.get('status', ''),
            'result': task.info.get('detections', '')
        }
    else:
        response = {
            'state': task.state,
            'status': str(task.info),
        }
    return response
