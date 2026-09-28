from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from datetime import datetime
from app.database.connection import Base

class TradeRegistro(Base):
    """
    Tabela na base de dados para registar entradas, TP, SL, ideias e notas de trade.
    """
    __tablename__ = "trades_registos"

    id = Column(Integer, primary_key=True, index=True)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    
    par_moeda = Column(String(20), nullable=False, default="EURUSD")
    tipo_ordem = Column(String(10), nullable=False) # 'BUY' ou 'SELL'
    
    # Valores do Trade
    preco_entrada = Column(Float, nullable=False)
    stop_loss = Column(Float, nullable=False)
    take_profit = Column(Float, nullable=False)
    risco_recompensa = Column(Float, nullable=True) # Ex: 1:3 -> 3.0
    
    # Dados SMC do Setup
    vies_diario = Column(String(50), nullable=True)
    eq_diario = Column(Float, nullable=True)
    
    # Campo para anotar a Ideia / Razão da Entrada
    ideia_nota = Column(Text, nullable=True)
    
    # Estado da operação
    estado = Column(String(20), default="PENDENTE") # 'PENDENTE', 'GANHO', 'PERDIDO', 'CANCELADO'

