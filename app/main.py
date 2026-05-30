from fastapi import FastAPI
from app.api.routes import router
from fastapi.responses import FileResponse

app = FastAPI(title="AI Automation Hub")

app.include_router(router)


@app.get("/")
def home():
    return FileResponse("app/frontend/index.html")