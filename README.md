# Cybersecurity Automation Platform (Async Edition)

A full-stack, decoupled web application that performs automated security audits on target URLs. This project demonstrates an enterprise-grade asynchronous architecture using a React frontend, a FastAPI gateway, and a Celery/Redis background worker queue.
<img width="1397" height="712" alt="image" src="https://github.com/user-attachments/assets/469f783d-a5d3-4e37-9ecd-bb04b9af8241" />

## Architecture

This application mimics how large-scale enterprise platforms handle heavy processing tasks without blocking the main web server:

1. **Frontend (React/Vite):** Provides a modern UI. It submits scan requests and uses a polling mechanism to fetch the status of background jobs.
2. **Web Gateway (FastAPI):** Instantly accepts requests, dispatches them to the message broker, and immediately returns a tracking `task_id` to the client.
3. **Message Broker (Redis):** Acts as the queue, holding pending scan jobs (Hosted via Upstash).
4. **Worker Engine (Celery):** Picks up jobs from the Redis queue and executes the heavy Python security scanning modules in the background.

## Features
* **Security Headers Analysis:** Automatically audits target URLs for critical missing security headers (HSTS, CSP, X-Frame-Options, etc.).
* **Asynchronous Processing:** Long-running scans are decoupled from the HTTP request cycle.
* **Real-time Status Polling:** The UI dynamically updates from "Processing" to "Completed" as the background worker finishes.
* **Actionable Reporting:** Results are returned with severity levels and specific remediation steps.

## How to Run Locally

Because this is a decoupled microservice architecture, you need to run three separate processes simultaneously. 

### Prerequisites
* Node.js & npm
* Python 3.8+
* A Redis Database URL (Local or Cloud/Upstash)

### 1. Start the FastAPI Web Server
Open Terminal 1:
```bash
cd cyber-platform-api
venv\Scripts\activate
uvicorn main:app --reload
```

### 2. Start the Celery Background Worker
Open Terminal 2:
```bash
cd cyber-platform-api
venv\Scripts\activate
# Note: --pool=solo is required for Windows environments
celery -A core.queue_tasks worker --loglevel=info --pool=solo
```

### 3. Start the React Frontend
Open Terminal 3:
```bash
cd cyber-demo-frontend
npm run dev
```

### Once all three are running, open your browser and navigate to http://localhost:5173
