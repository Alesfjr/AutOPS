import time
import  psutil
import requests

from agent.logs import ger_logger
from agent.services import evaluate_metrics

logger=ger_logger(__name__)

API_URL= "https://api:8000/metrics"

def collect_metrics() -> dict:
    return {
        "cpu": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("/").percent,
        "load_average":psutil.getloadavg()
    }

def send_metrics(data: dict):

    try:
        response =requests.post(url=API_URL, json=data, timeout=5)
        logger.info(f"Enviado para API | status={response.status_code}")
    except Exception as error:
        logger.error(f"Erro ao enviar metricas :{error}")

if __name__ == "__main__":
    logger.info("Agent iniciado ")

    while True:
        metrics = collect_metrics()
        evaluted=evaluate_metrics(metrics)

        logger.info(evaluted)
        send_metrics(metrics)

        time.sleep(5)

