from core.celery_app import celery_instance
from scanners.headers_analyzer import scan_security_headers

@celery_instance.task(bind=True)
def run_headers_scan_task(self, target_url: str):
    results = scan_security_headers(target_url)
    
    results["task_id"] = self.request.id
    return results