from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "AI Automation Hub running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/automate")
def automate(req: dict):
    return {"result": "ok"}