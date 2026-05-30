import time
from app.workers.queue import get_job
from app.agents.calendar_agent import create_event

def worker_loop():

    while True:
        job = get_job()

        if job:
            if job["type"] == "calendar":
                create_event(job["task"])

        time.sleep(2)