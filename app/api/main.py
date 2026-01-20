from fastapi import FastAPI
from prometheus_client import make_asgi_app, Gauge
from datetime import datetime
from app.database import init_db

from app.database import Base, engine
from app.models.metrics import Host

app = FastAPI(title="AutOPS API")

# Métricas Prometheus
CPU_USAGE = Gauge(
    "autops_cpu_usage",
    "Uso de CPU por Host",
    ["hostname"]
)

MEM_USAGE = Gauge(
    "autops_memory_usage",
    "Uso de Memória por Host",
    ["hostname"]
)

DISK_USAGE = Gauge(
    "autops_disk_usage",
    "Uso de Disco por Host",
    ["hostname"]
)

@app.on_event("startup")
def startup():
    init_db()

LOAD_USAGE = Gauge(
    "autops_load_average",
    "Load Average por Host",
    ["hostname"]
)

def update_prometheus_metrics(hostname: str, payload: dict):
    if "cpu_percent" in payload:
        CPU_USAGE.labels(hostname=hostname).set(payload["cpu_percent"])
    if "memory_percent" in payload:
        MEM_USAGE.labels(hostname=hostname).set(payload["memory_percent"])
    if "disk_percent" in payload:
        DISK_USAGE.labels(hostname=hostname).set(payload["disk_percent"])
    if "load_average_percent" in payload:
        LOAD_USAGE.labels(hostname=hostname).set(payload["load_average_percent"])


# Router
from app.routers import ingest

app.include_router(ingest.router)

# Endpoint Prometheus
app.mount("/metrics", make_asgi_app())

@app.get("/health")
def health():
    return {
        "status": "UP",
        "time": datetime.utcnow().isoformat()
    }
