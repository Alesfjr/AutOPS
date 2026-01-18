from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.metrics import MetricsTable, Host, Event
# Importamos a lógica de decisão
from app.api.serivces import evaluate_thresholds

router = APIRouter(prefix="/ingest")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/metrics")
def ingest_metrics(payload: dict, db: Session = Depends(get_db)):
    # 1. Identificar Host (Sensor não opina, a API identifica)
    h_name = payload.get("hostname", "unknown")
    host = db.query(Host).filter(Host.hostname == h_name).first()

    if not host:
        host = Host(hostname=h_name)
        db.add(host)
        db.flush()  # Gera o ID para as métricas

    # 2. EXPOR (Prometheus)
    # Import local para quebrar o ciclo de dependência com o main.py
    from app.api.main import update_prometheus_metrics
    update_prometheus_metrics(h_name, payload)

    # 3. ARMAZENAR (MySQL)
    for key, val in payload.items():
        if isinstance(val, (int, float)):
            db.add(MetricsTable(
                host_id=host.id,
                metric_name=key,
                metric_value=val
            ))

    # 4. DECIDIR (Cérebro)
    evaluate_thresholds(host.id, payload, db)

    db.commit()
    return {"status": "processed", "host_id": host.id}