FROM python:3.11-slim

# ต้องใช้ slim ไม่ใช่ full — ประหยัด RAM 200+ MB
WORKDIR /app

# ติดตั้ง dependencies ก่อน copy code (cache layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# ไม่ใช้ --reload ใน production
CMD ["uvicorn", "app.api.routes:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]