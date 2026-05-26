from core.celery_app import celery_instance
from scanners.headers_analyzer import scan_security_headers

# The @celery_instance.task decorator tells Celery this function belongs in the queue
@celery_instance.task(bind=True)
def run_headers_scan_task(self, target_url: str):
    # Execute the scanner module we built earlier
    results = scan_security_headers(target_url)
    
    # Attach the unique task ID to the results so the frontend can track it
    results["task_id"] = self.request.id
    return results