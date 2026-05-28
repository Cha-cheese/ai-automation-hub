from fastapi.staticfiles import StaticFiles
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")