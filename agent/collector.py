import time
import psutil
import requests
import os

from agent.logs import get_logger
from agent.services import evaluate_metrics

logger = get_logger(__name__)

API_URL = os.getenv("API_URL", "http://localhost:8000/metrics")


def collect_metrics() -> dict:
    load_1, load_5, load_15 = psutil.getloadavg()

    return {
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage("/").percent,
        "load_average_percent": load_1
    }


def send_metrics(data: dict):
    logger.info(f"Payload enviado: {data}")

    try:
        response = requests.post(API_URL, json=data, timeout=5)
        logger.info(f"Enviado para API | status={response.status_code}")
    except Exception as error:
        logger.error(f"Erro ao enviar metricas: {error}")


if __name__ == "__main__":
    logger.info("Agent iniciado")

    while True:
        metrics = collect_metrics()
        evaluated = evaluate_metrics(metrics)

        logger.info(f"Avaliação local: {evaluated}")
        logger.info(f"Métricas coletadas: {metrics}")
        send_metrics(metrics)

        time.sleep(5)
