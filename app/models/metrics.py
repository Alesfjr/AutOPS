from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import socket
import psutil

# Função para coletar métricas do host
def collect_metrics() -> dict:
    return {
        "hostname": socket.gethostname(),  # ESSENCIAL
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage("/").percent
    }

# Modelo Host
class Host(Base):
    __tablename__ = "hosts"

    id = Column(Integer, primary_key=True, index=True)
    hostname = Column(String(50), unique=True, index=True)
    ip = Column(String(15))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relacionamento com eventos e métricas
    events = relationship("Event", back_populates="host", cascade="all, delete-orphan")
    metrics = relationship("Metrics", back_populates="host", cascade="all, delete-orphan")


# Modelo Metrics
class Metrics(Base):
    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True, index=True)
    host_id = Column(Integer, ForeignKey('hosts.id'))
    metric_name = Column(String(50), nullable=False)
    metric_value = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    host = relationship("Host", back_populates="metrics")

# Modelo Event
class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    host_id = Column(Integer, ForeignKey('hosts.id'))
    event_type = Column(String(50))
    severity = Column(String(20))
    description = Column(Text)
    started_at = Column(DateTime, default=datetime.utcnow)

    host = relationship("Host", back_populates="events")
