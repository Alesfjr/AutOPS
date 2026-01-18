from sqlalchemy.orm import Session
from app.models.metrics import Event

def evaluate_thresholds(host_id: int, payload: dict, db: Session):
    """
        Analisa as métricas recebidas e decide se gera um evento de alerta.
        """
    rules= [{"metric": "cpu_percent", "threshold": 90, "type": "CPU_CRITICAL", "severity": "CRITICAL"},
        {"metric": "memory_percent", "threshold": 85, "type": "MEM_HIGH", "severity": "WARNING"},
        {"metric": "disk_percent", "threshold": 95, "type": "DISK_FULL", "severity": "CRITICAL"},]

    for rule in rules:
        metrics_name=rule["metric"]
        value=payload.get(metrics_name)

        if value and value > rule["threshold"]:
            # Cria o evento no banco de dados (MySQL)
            new_event = Event(
            host_id=host_id,
            event_type=rule["type"],
            severity=rule["severity"],
            description=f"Alerta: {metrics_name} em {value}% (Limite: {rule['threshold']}%)"
        )
        db.add(new_event)
