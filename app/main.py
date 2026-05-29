from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="AI Automation Hub")

app.include_router(router)