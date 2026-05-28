from app.api.routes import app
from app.api.result import router

app.include_router(router)