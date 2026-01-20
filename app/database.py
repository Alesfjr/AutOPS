import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import OperationalError

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./autoops.db"
)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    pool_pre_ping=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# Dependency do FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Inicialização com retry (Docker/MySQL)
def init_db(retries: int = 10, delay: int = 2):
    from app.models.metrics import Host, Metrics, Event  # registra os models

    for attempt in range(retries):
        try:
            Base.metadata.create_all(bind=engine)
            print("✅ Banco inicializado com sucesso")
            return
        except OperationalError:
            print(f"⏳ Banco indisponível, tentativa {attempt+1}/{retries}")
            time.sleep(delay)

    raise RuntimeError("❌ Não foi possível conectar ao banco de dados")
