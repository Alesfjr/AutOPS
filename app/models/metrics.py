from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime
import socket
import psutil

def collect_metrics() -> dict:
    return {
        "hostname": socket.gethostname(), # ESSENCIAL
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage("/").percent
    }

class Host(Base):
    __tablename__ = 'hosts'
    id = Column(Integer, primary_key=True)
    hostname = Column(String(100), nullable=False)
    ip = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    metrics = relationship("Metrics", back_populates="host")

class MetricsTable(Base):
    __tablename__ = 'metrics'
    id = Column(Integer, primary_key=True)
    host_id = Column(Integer, ForeignKey('hosts.id'))
    metric_name = Column(String(50), nullable=False)
    metric_value = Column(Float, nullable=False)
    collected_at = Column(DateTime, default=datetime.utcnow)
    host = relationship("Host", back_populates="metrics")

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    host_id = Column(Integer, ForeignKey('hosts.id'))
    event_type = Column(String(50)) # ex: 'CPU_HIGH'
    severity = Column(String(20))   # ex: 'CRITICAL'
    description = Column(Text)
    started_at = Column(DateTime, default=datetime.utcnow)
    host = relationship("Host", back_populates="events")