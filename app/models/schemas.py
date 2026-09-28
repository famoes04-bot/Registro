from pydantic import BaseModel, Field
from typing import List, Optional

class NiveisDiarios(BaseModel):
    pdh: float = Field(..., description="Previous Day High")
    pdl: float = Field(..., description="Previous Day Low")
    pdc: float = Field(..., description="Previous Day Close")
    pdo: float = Field(..., description="Previous Day Open")
    eq_diario: float = Field(..., description="Equilibrium Diário (PDH + PDL) / 2")

class NiveisH4(BaseModel):
    max_h4: float = Field(..., description="Máxima da última vela H4")
    min_h4: float = Field(..., description="Mínima da última vela H4")
    eq_h4: float = Field(..., description="Equilibrium H4 (Max + Min) / 2")

class NiveisDiaAtual(BaseModel):
    max_atual: float = Field(..., description="Máxima do dia atual")
    min_atual: float = Field(..., description="Mínima do dia atual")
    eq_atual: float = Field(..., description="Equilibrium do dia atual (Max + Min) / 2")

class PadraoDetectado(BaseModel):
    padrao: str = Field(..., description="Nome do padrão (MSS, CHoCH, FVG, Sweep, OB)")
    confianca: float = Field(..., description="Grau de confiança da IA (0.0 a 1.0)")
    box: List[float] = Field(..., description="Coordenadas da caixa [x1, y1, x2, y2]")

class AnaliseResponse(BaseModel):
    status: str
    filename: str
    niveis_calculados: dict
    detecoes_visuais: List[PadraoDetectado]
    vies_sugerido: str

