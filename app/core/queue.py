import asyncio
from collections import deque

JOB_QUEUE = deque()


async def worker():
    while True:
        if JOB_QUEUE:
            job = JOB_QUEUE.popleft()
            try:
                await job()
            except Exception:
                pass
        await asyncio.sleep(0.1)


def add_job(job):
    JOB_QUEUE.append(job)