from prometheus_client import Gauge

HOST_METRICS = {}

def update_prometheus_metrics(hostname: str, payload: dict):
    if hostname not in HOST_METRICS:
        HOST_METRICS[hostname] = {}

    for key, val in payload.items():
        if isinstance(val, (int, float)):
            metric_name = f"autoops_{key}"
            if metric_name not in HOST_METRICS[hostname]:
                HOST_METRICS[hostname][metric_name] = Gauge(
                    metric_name,
                    f"{key} metric",
                    ["hostname"]
                )
            HOST_METRICS[hostname][metric_name].labels(
                hostname=hostname
            ).set(val)
