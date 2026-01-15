from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from app.database import Base
from datetime import datetime

class Metrics(Base):

    __tablename__ = 'metrics'

    id = Column(Integer, primary_key=True)
    host_id = Column(Integer, nullable=False)
    metric_name = Column(String(50), nullable=False)
    metric_value = Column(Float, nullable=False)
    collected_at = Column(DateTime, default=datetime.utcnow)

