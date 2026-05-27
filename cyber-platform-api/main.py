from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core.queue_tasks import run_headers_scan_task
from core.celery_app import celery_instance

app = FastAPI(title="Cybersecurity API - Async Edition")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScanRequest(BaseModel):
    url: str

@app.post("/api/v1/scan/headers")
def dispatch_headers_scan(request: ScanRequest):
    task = run_headers_scan_task.delay(request.url)
    
    return {
        "status": "queued", 
        "message": "Scan has been added to the background queue.",
        "task_id": task.id
    }

@app.get("/api/v1/scan/status/{task_id}")
def get_scan_status(task_id: str):
    task_result = celery_instance.AsyncResult(task_id)
    
    if task_result.ready():
        return {
            "status": "success",
            "results": task_result.result
        }
    else:
        return {
            "status": "processing",
            "message": "The scan is currently running in the background..."
        }