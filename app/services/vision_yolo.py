import cv2
import numpy as np
from ultralytics import YOLO
import os

class YOLOVisionService:
    def __init__(self, model_path: str = "app/weights/modelo_smc.pt"):
        # Se não encontrar o modelo personalizado, carrega o yolov8n padrão para testes
        if os.path.exists(model_path):
            self.model = YOLO(model_path)
            print(f"[YOLO] Modelo personalizado carregado de: {model_path}")
        else:
            self.model = YOLO("yolov8n.pt")
            print("[YOLO] Modelo 'modelo_smc.pt' não encontrado em app/weights/. Usando yolov8n padrão.")

    def detectar_padroes(self, image_bytes: bytes) -> list:
        """Recebe os bytes da imagem, decodifica com OpenCV e aplica o YOLOv8."""
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if image is None:
            raise ValueError("Não foi possível decodificar a imagem fornecida.")

        # Executa a inferência na imagem
        results = self.model(image)
        padroes = []

        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                label = self.model.names[class_id]
                conf = float(box.conf[0])
                cords = box.xyxy[0].tolist()

                padroes.append({
                    "padrao": label,
                    "confianca": round(conf, 4),
                    "box": [round(c, 2) for c in cords]
                })

        return padroes

