# utils/calculos.py

# Porcentajes reales de tu fórmula (% sobre el agua)
PORCENTAJES_BASE = {
    "Sal nitral": 0.80,
    "Carragenina": 0.50,
    "Tripolifosfato": 3.19,
    "Bensopro (EMBAC)": 0.36,
    "Proteína Supra": 1.00,
    "Almidón de trigo": 1.82,
    "Goma xantana": 0.04,
    "Excelpro": 0.83,
    "Jamón California": 0.89,
    "Humo P-50": 0.05,
    "Eritorbato de sodio": 1.00,
    "Sal común": 1.82,
    "Saborizante tocineta": 0.53,
    "Adobo tocino": 0.18,
    "Fibragel MT": 1.00,
    "Pirofosfato": 1.50
}

# ---------------------------------------------------------
#  CÁLCULO PRINCIPAL USADO POR LA APP
# ---------------------------------------------------------

def obtener_calculo_completo(cantidad_chuletas: int, factor_a
