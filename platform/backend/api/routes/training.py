from fastapi import APIRouter, HTTPException, Query, UploadFile, File, Response
from pydantic import BaseModel
from typing import List, Optional
from cv_models.tasks import train_model

router = APIRouter()

# --- Models ---
class VideoLinkRequest(BaseModel):
    video_link: str

class Annotation(BaseModel):
    id: int
    video: str
    events: int
    description: Optional[str] = None

class Insights(BaseModel):
    totalVideos: int
    totalEvents: int
    mostCommonEvent: str

# --- In-memory demo storage (replace with DB integration) ---
ANNOTATIONS = [
    Annotation(id=1, video="https://example.com/video1.mp4", events=12, description="Match 1"),
    Annotation(id=2, video="https://example.com/video2.mp4", events=8, description="Match 2"),
]

INSIGHTS = Insights(totalVideos=2, totalEvents=20, mostCommonEvent="goal")

# --- Endpoints ---
@router.post("/train/start")
def start_training(req: VideoLinkRequest):
    task = train_model.delay(req.video_link)
    return {"status": "started", "task_id": task.id}


@router.get("/train/status/{task_id}")
def get_training_status(task_id: str):
    task = train_model.AsyncResult(task_id)
    if task.state == 'PENDING':
        return {'state': task.state, 'status': 'Pending...'}
    elif task.state != 'FAILURE':
        return {
            'state': task.state,
            'status': task.info.get('status', ''),
            'result': task.info.get('model_path', '')
        }
    else:
        return {'state': task.state, 'status': str(task.info)}

@router.get("/train/annotations", response_model=List[Annotation])
def get_annotations(
    q: Optional[str] = Query(None, description="Search by video or description"),
    skip: int = 0,
    limit: int = 10
):
    # TODO: Fetch from DB
    filtered = ANNOTATIONS
    if q:
        filtered = [a for a in filtered if q.lower() in a.video.lower() or (a.description and q.lower() in a.description.lower())]
    return filtered[skip:skip+limit]
# Delete annotation by id
@router.delete("/train/annotations/{annotation_id}")
def delete_annotation(annotation_id: int):
    global ANNOTATIONS
    before = len(ANNOTATIONS)
    ANNOTATIONS = [a for a in ANNOTATIONS if a.id != annotation_id]
    if len(ANNOTATIONS) == before:
        raise HTTPException(status_code=404, detail="Annotation not found")
    return {"status": "deleted", "id": annotation_id}

# Edit annotation by id
class AnnotationEditRequest(BaseModel):
    video: Optional[str] = None
    events: Optional[int] = None
    description: Optional[str] = None

@router.put("/train/annotations/{annotation_id}", response_model=Annotation)
def edit_annotation(annotation_id: int, req: AnnotationEditRequest):
    for a in ANNOTATIONS:
        if a.id == annotation_id:
            if req.video is not None:
                a.video = req.video
            if req.events is not None:
                a.events = req.events
            if req.description is not None:
                a.description = req.description
            return a
    raise HTTPException(status_code=404, detail="Annotation not found")

# Upload annotation file (JSON)
@router.post("/train/annotations/upload")
async def upload_annotation_file(file: UploadFile = File(...)):
    content = await file.read()
    # TODO: Parse and store in DB
    return {"filename": file.filename, "size": len(content)}

# Download all annotations as JSON
@router.get("/train/annotations/download")
def download_annotations():
    import json
    data = [a.dict() for a in ANNOTATIONS]
    return Response(content=json.dumps(data), media_type="application/json")

@router.get("/train/insights", response_model=Insights)
def get_insights():
    # TODO: Compute from DB
    return INSIGHTS
