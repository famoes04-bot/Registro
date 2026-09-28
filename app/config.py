import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    """
    Configurações globais da aplicação.
    As variáveis podem ser sobrescritas por um ficheiro .env ou variáveis do sistema.
    """
    # Informações da Aplicação
    APP_NAME: str = "SMC Trading Analyzer API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Servidor
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Configurações de Visão / YOLOv8
    MODEL_PATH: str = str(BASE_DIR / "app" / "weights" / "modelo_smc.pt")
    CONFIDENCE_THRESHOLD: float = 0.35  # Limiar mínimo de confiança para aceitar deteção (0.0 a 1.0)
    ALLOWED_IMAGE_TYPES: list[str] = ["image/jpeg", "image/png", "image/webp"]
    MAX_IMAGE_SIZE_MB: int = 10  # Tamanho máximo da imagem em Megabytes
    
    # Configurações de CORS (para ligar com o Frontend em React/Next.js/Flutter)
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8080",
        "*"
    ]

    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Instância global das configurações
settings = Settings()

