# utils/calculos.py

# Porcentajes reales de tu fórmula (16 ingredientes)
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

FACTOR_AGUA = 3.0  # litros/kg de chuleta


def calcular_agua(cantidad_chuletas: int, factor_agua: float = FACTOR_AGUA) -> float:
    """
    Devuelve la cantidad de agua en kg/L.
    """
    return cantidad_chuletas * factor_agua


def calcular_ingredientes(agua_kg: float, porcentajes: dict) -> dict:
    """
    Calcula los ingredientes en kg según % sobre el agua.
    """
    resultados = {}
    for nombre, porcentaje in porcentajes.items():
        resultados[nombre] = agua_kg * (porcentaje / 100)
    return resultados


def obtener_calculo_completo(cantidad_chuletas: int):
    """
    Devuelve:
    - agua_base (kg)
    - porcentajes (dict)
    - ingredientes calculados en kg (dict)
    """
    agua = calcular_agua(cantidad_chuletas)
    ingredientes = calcular_ingredientes(agua, PORCENTAJES_BASE)
    return agua, PORCENTAJES_BASE, ingredientes


