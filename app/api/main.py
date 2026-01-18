from fastapi import FastAPI
from prometheus_client import make_asgi_app, Gauge
from datetime import datetime

app = FastAPI(title="AutOPS API")

# 1. Definição de Métricas do Prometheus (Expor)
# Definimos globalmente para que possam ser importadas sem criar loops
CPU_USAGE = Gauge('autops_cpu_usage', 'Uso de CPU por Host', ['hostname'])
MEM_USAGE = Gauge('autops_memory_usage', 'Uso de Memória por Host', ['hostname'])
DISK_USAGE = Gauge('autops_disk_usage', 'Uso de Disco por Host', ['hostname'])

# 2. Função Unificada para atualizar o Prometheus
def update_prometheus_metrics(hostname, payload):
    if "cpu_percent" in payload:
        CPU_USAGE.labels(hostname=hostname).set(payload["cpu_percent"])
    if "memory_percent" in payload:
        MEM_USAGE.labels(hostname=hostname).set(payload["memory_percent"])
    if "disk_percent" in payload:
        DISK_USAGE.labels(hostname=hostname).set(payload["disk_percent"])

# 3. Importação tardia do router para evitar erro circular
from app.routers import ingest
app.include_router(ingest.router)

# 4. Rota de Monitoramento para o Prometheus (Scrape)
app.mount("/metrics", make_asgi_app())

@app.get("/health")
def health():
    return {
        "status": "UP",
        "time": datetime.utcnow().isoformat()
    }