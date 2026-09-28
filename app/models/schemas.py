from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

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
