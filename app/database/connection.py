from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import settings

# Cria o ficheiro SQLite local chamado 'smc_trades.db' na raiz do projeto
SQLALCHEMY_DATABASE_URL = getattr(settings, "DATABASE_URL", "sqlite:///./smc_trades.db")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Injeta a sessão da base de dados nas rotas da FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

