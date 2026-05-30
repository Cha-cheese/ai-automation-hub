from collections import deque

queue = deque()

def add_job(job):
    queue.append(job)

def get_job():
    if queue:
        return queue.popleft()
    return None

from app.workers.queue import add_job

def calendar_agent(task):

    job = {
        "type": "calendar",
        "task": task
    }

    add_job(job)

    return {
        "status": "queued",
        "message": "Calendar event added to queue"
    }