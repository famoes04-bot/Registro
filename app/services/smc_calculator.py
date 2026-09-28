class SMCCalculator:
    @staticmethod
    def calcular_niveis(
        pdh: float, pdl: float, pdc: float, pdo: float,
        max_h4: float, min_h4: float,
        max_atual: float, min_atual: float
    ) -> dict:
        """Efetua todos os cálculos matemáticos de níveis SMC."""
        eq_diario = (pdh + pdl) / 2.0
        eq_h4 = (max_h4 + min_h4) / 2.0
        eq_atual = (max_atual + min_atual) / 2.0

        # Lógica simples de determinação de Viés
        vies = "Neutro"
        if pdc > eq_diario:
            vies = "Bullish (Preço acima do EQ Diário)"
        elif pdc < eq_diario:
            vies = "Bearish (Preço abaixo do EQ Diário)"

        return {
            "diario_anterior": {
                "pdh": pdh,
                "pdl": pdl,
                "pdc": pdc,
                "pdo": pdo,
                "eq_diario": eq_diario
            },
            "h4_anterior": {
                "max_h4": max_h4,
                "min_h4": min_h4,
                "eq_h4": eq_h4
            },
            "dia_atual": {
                "max_atual": max_atual,
                "min_atual": min_atual,
                "eq_atual": eq_atual
            },
            "vies": vies
        }

