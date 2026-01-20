def evaluate_metrics(metrics: dict) -> dict:
    status = "OK"

    cpu = metrics.get("cpu_percent", 0)  # corrigido aqui

    if cpu > 90:
        status = "CRITICAL"
    elif cpu >= 75:
        status = "WARNING"

    return {
        "status": status,
        "cpu": cpu
    }
