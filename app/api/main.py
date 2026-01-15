from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI(title="AutOPS API")

class Metrics(BaseModel):
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    load_average_percent: float

LAST_METRICS = {}

@app.post("/metrics")
def receive_metrics(metrics: Metrics):
    global LAST_METRICS

    LAST_METRICS = {
        **metrics.dict(),
        "received_at": datetime.utcnow().isoformat()
    }

    return {"status": "received"}

@app.get("/health")
def health():
    return {
        "status": "UP",
        "time": datetime.utcnow().isoformat()
    }
