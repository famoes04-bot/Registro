from typing import List
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.config import settings
from app.services.smc_calculator import SMCCalculator
from app.services.vision_yolo import YOLOVisionService
from app.database import engine, Base, get_db, TradeRegistro
from app.models.schemas import TradeCreateSchema, TradeResponseSchema

# Criar tabelas na base de dados automaticamente
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API SMC / ICT Trading Analyzer com Visão Computacional (YOLOv8) e Diário de Trades."
)

# Configuração do Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializa o serviço de visão computacional
vision_service = YOLOVisionService()

@app.get("/")
def read_root():
    return {"message": f"{settings.APP_NAME} v{settings.APP_VERSION} a funcionar com sucesso!"}

# --- ENDPOINT DE ANÁLISE COMPLETA ---

@app.post("/analisar-setup/", summary="Analisar setup de trade combinando imagem e níveis matemáticos")
async def analisar_setup(
    file: UploadFile = File(..., description="Foto/Print do gráfico M1 ou M5"),
    # Dia Anterior
    pdh: float = Form(..., description="Previous Day High"),
    pdl: float = Form(..., description="Previous Day Low"),
    pdc: float = Form(..., description="Previous Day Close"),
    pdo: float = Form(..., description="Previous Day Open"),
    # Última Vela H4
    max_h4: float = Form(..., description="Máxima H4 anterior"),
    min_h4: float = Form(..., description="Mínima H4 anterior"),
    # Dia Atual
    max_atual: float = Form(..., description="Máxima do dia atual"),
    min_atual: float = Form(..., description="Mínima do dia atual")
):
    """Processa o gráfico via YOLOv8 e calcula os níveis numéricos exatos de SMC/ICT."""
    
    # 1. Validar Tipo do Ficheiro
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="O ficheiro enviado precisa de ser uma imagem válida.")

    image_bytes = await file.read()

    # 2. Processar Visão Computacional com Tratamento de Erros
    try:
        padroes_detectados = vision_service.detectar_padroes(image_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar imagem: {str(e)}")

    # 3. Calcular Níveis Numéricos Exatos
    niveis = SMCCalculator.calcular_niveis(
        pdh=pdh, pdl=pdl, pdc=pdc, pdo=pdo,
        max_h4=max_h4, min_h4=min_h4,
        max_atual=max_atual, min_atual=min_atual
    )

    # 4. Cruzar e Retornar Dados
    return {
        "status": "sucesso",
        "filename": file.filename,
        "niveis_calculados": niveis,
        "detecoes_visuais": padroes_detectados,
        "vies_sugerido": niveis.get("vies")
    }

# --- ENDPOINTS: REGISTO DE IDEIAS E TRADES ---

@app.post("/trades/", response_model=TradeResponseSchema, summary="Registar nova ideia ou operação")
def guardar_trade(trade_data: TradeCreateSchema, db: Session = Depends(get_db)):
    """Salva uma nova ideia de trade com Preço de Entrada, SL, TP e notas no histórico."""
    
    # Calcular Risco:Recompensa automaticamente
    rr = None
    distancia_sl = abs(trade_data.preco_entrada - trade_data.stop_loss)
    distancia_tp = abs(trade_data.take_profit - trade_data.preco_entrada)
    if distancia_sl > 0:
        rr = round(distancia_tp / distancia_sl, 2)

    novo_trade = TradeRegistro(
        par_moeda=trade_data.par_moeda,
        tipo_ordem=trade_data.tipo_ordem.upper(),
        preco_entrada=trade_data.preco_entrada,
        stop_loss=trade_data.stop_loss,
        take_profit=trade_data.take_profit,
        risco_recompensa=rr,
        vies_diario=trade_data.vies_diario,
        eq_diario=trade_data.eq_diario,
        ideia_nota=trade_data.ideia_nota
    )
    
    db.add(novo_trade)
    db.commit()
    db.refresh(novo_trade)
    return novo_trade

@app.get("/trades/", response_model=List[TradeResponseSchema], summary="Listar todas as ideias e trades gravados")
def listar_trades(db: Session = Depends(get_db)):
    """Retorna o histórico completo de trades e ideias gravadas por ordem cronológica inversa."""
    return db.query(TradeRegistro).order_by(TradeRegistro.data_criacao.desc()).all()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
