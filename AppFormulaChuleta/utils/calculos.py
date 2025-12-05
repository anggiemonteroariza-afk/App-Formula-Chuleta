# utils/calculos.py

from utils.loader import calcular_agua, calcular_ingredientes

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


def obtener_calculo_completo(cantidad_chuletas: int, factor_agua: float = 3.0):
    agua = calcular_agua(cantidad_chuletas, factor_agua)
    ingredientes = calcular_ingredientes(agua, PORCENTAJES_BASE)
    return agua, PORCENTAJES_BASE, ingredientes


def calcular_formula(cantidad_chuletas: int):
    """
    Envuelve todo en una sola función para app.py
    """
    return obtener_calculo_completo(cantidad_chuletas)


def recalcular_con_agua_manual(agua_manual: float):
    ingredientes = calcular_ingredientes(agua_manual, PORCENTAJES_BASE)
    return ingredientes
