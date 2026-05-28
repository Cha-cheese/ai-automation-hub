from fastapi import FastAPI
from fastapi.responses import StreamingResponse
import asyncio

app = FastAPI()


@app.post("/stream")
async def stream(req: dict):

    async def event_stream():
        yield "data: starting...\n\n"

        await asyncio.sleep(1)
        yield "data: planning task...\n\n"

        await asyncio.sleep(1)
        yield "data: executing...\n\n"

        await asyncio.sleep(1)
        yield "data: finalizing...\n\n"

        yield "data: done\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


@app.post("/login")
def login():
    return {
        "token": "mock-jwt-token",
        "status": "logged_in"
    }