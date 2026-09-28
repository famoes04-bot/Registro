from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from app.services.smc_calculator import SMCCalculator
from app.services.vision_yolo import YOLOVisionService

app = FastAPI(
    title="SMC / ICT Trading Analyzer API",
    description="API para análise de setups SMC combinando cálculos matemáticos com visão por computadores (YOLOv8).",
    version="1.0.0"
)

# Inicializa o serviço de visão
vision_service = YOLOVisionService()

@app.get("/")
def read_root():
    return {"message": "API de Análise SMC a funcionar com sucesso!"}

@app.post("/analisar-setup/")
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
    # 1. Validar Ficheiro
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="O ficheiro enviado precisa de ser uma imagem.")

    image_bytes = await file.read()

    # 2. Passo 1: Processar Visão Computacional (YOLOv8)
    try:
        padroes_detectados = vision_service.detectar_padroes(image_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar imagem: {str(e)}")

    # 3. Passo 2: Calcular Níveis Numéricos Exatos
    niveis = SMCCalculator.calcular_niveis(
        pdh=pdh, pdl=pdl, pdc=pdc, pdo=pdo,
        max_h4=max_h4, min_h4=min_h4,
        max_atual=max_atual, min_atual=min_atual
    )

    # 4. Passo 3: Cruzar e Retornar Dados
    return {
        "status": "sucesso",
        "filename": file.filename,
        "niveis_calculados": niveis,
        "detecoes_visuais": padroes_detectados,
        "vies_sugerido": niveis["vies"]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

