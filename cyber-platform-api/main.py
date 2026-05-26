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

# ENDPOINT 1: Dispatch the job to the queue
@app.post("/api/v1/scan/headers")
def dispatch_headers_scan(request: ScanRequest):
    # .delay() pushes the job to Redis instead of running it right now
    task = run_headers_scan_task.delay(request.url)
    
    # The server responds instantly!
    return {
        "status": "queued", 
        "message": "Scan has been added to the background queue.",
        "task_id": task.id
    }

# ENDPOINT 2: Check the status of the job
@app.get("/api/v1/scan/status/{task_id}")
def get_scan_status(task_id: str):
    # Ask Celery for the state of this specific task
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