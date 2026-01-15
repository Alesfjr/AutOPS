from fastapi import FastAPI, APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.metrics import Metrics

router = APIRouter(prefix="/ingest")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/metrics")
def ingest_metrics(playload: dict, db: Session = Depends(get_db)):
    metrics = Metrics(

        host_id=playload["host_id"],
        metric_name=playload["name"],
        metric_value=playload["value"]

    )
    db.add(metrics)
    db.commit()
    return {"status": "OK"}