from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Column, DateTime, Float, Integer, String, Text

from app.database.connection import Base
# --- ESQUEMAS ANTERIORES PERMANECEM AQUI ---

# --- NOVOS ESQUEMAS PARA O REGISTO DE TRADES ---
class TradeCreateSchema(BaseModel):
    par_moeda: str = Field("EURUSD", description="Par de moedas ou ativo (ex: EURUSD, BTCUSD)")
    tipo_ordem: str = Field(..., description="Tipo de ordem: 'BUY' ou 'SELL'")
    preco_entrada: float = Field(..., description="Preço de Entrada (Entry Price)")
    stop_loss: float = Field(..., description="Preço do Stop Loss (SL)")
    take_profit: float = Field(..., description="Preço do Take Profit (TP)")
    vies_diario: Optional[str] = Field(None, description="Viés identificado (Bullish/Bearish)")
    eq_diario: Optional[float] = Field(None, description="Equilibrium Diário calculado")
    ideia_nota: Optional[str] = Field(None, description="Anotações sobre a ideia, POI ou gatilho da operação")

class TradeResponseSchema(TradeCreateSchema):
    id: int
    data_criacao: datetime
    risco_recompensa: Optional[float]
    estado: str

    class Config:
        from_attributes = True

# ==========================================
# MODELO SQLALCHEMY (Base de Dados)
# ==========================================
class TradeRegistro(Base):
    """
    Tabela na base de dados para registar entradas, TP, SL, ideias e notas de trade.
    """
    __tablename__ = "trades_registos"

    id = Column(Integer, primary_key=True, index=True)
    data_criacao = Column(DateTime, default=datetime.utcnow)

    par_moeda = Column(String(20), nullable=False, default="EURUSD")
    tipo_ordem = Column(String(10), nullable=False)  # 'BUY' ou 'SELL'

    # Valores do Trade
    preco_entrada = Column(Float, nullable=False)
    stop_loss = Column(Float, nullable=False)
    take_profit = Column(Float, nullable=False)
    risco_recompensa = Column(Float, nullable=True)  # Ex: 1:3 -> 3.0

    # Dados SMC do Setup
    vies_diario = Column(String(50), nullable=True)
    eq_diario = Column(Float, nullable=True)

    # Campo para anotar a Ideia / Razão da Entrada
    ideia_nota = Column(Text, nullable=True)

    # Estado da operação
    estado = Column(String(20), default="PENDENTE")  # 'PENDENTE', 'GANHO', 'PERDIDO', 'CANCELADO'


# ==========================================
# SCHEMAS PYDANTIC (Validação / API)
# ==========================================
class TradeCreateSchema(BaseModel):
    par_moeda: str = Field("EURUSD", description="Par de moedas ou ativo (ex: EURUSD, BTCUSD)")
    tipo_ordem: str = Field(..., description="Tipo de ordem: 'BUY' ou 'SELL'")
    preco_entrada: float = Field(..., description="Preço de Entrada (Entry Price)")
    stop_loss: float = Field(..., description="Preço do Stop Loss (SL)")
    take_profit: float = Field(..., description="Preço do Take Profit (TP)")
    vies_diario: Optional[str] = Field(None, description="Viés identificado (Bullish/Bearish)")
    eq_diario: Optional[float] = Field(None, description="Equilibrium Diário calculated")
    ideia_nota: Optional[str] = Field(None, description="Anotações sobre a ideia, POI ou gatilho da operação")


class TradeResponseSchema(TradeCreateSchema):
    id: int
    data_criacao: datetime
    risco_recompensa: Optional[float] = None
    estado: str = "PENDENTE"

    # Pydantic v2 (Substitui 'class Config: from_attributes = True')
    model_config = ConfigDict(from_attributes=True)
