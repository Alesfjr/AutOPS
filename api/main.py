from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime, timezone

app= FastAPI(title="AutOPS API")

LAST_METRICS = {}

class Metrics(BaseModel):
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    load_average_percent: float

@app.get("/health")
def health():
    return {

        "status": "UP",
        "time" : datetime.now(timezone.utc).isoformat()
    }
@app.post("/metrics")
def receive_metrics(metrics: Metrics):
    global LAST_METRICS
    LAST_METRICS = metrics.dict()
    return{
        "message":"Metrics received"
    }

@app.get("/metrics")
def metrics():
    return LAST_METRICS