# utils/calculos.py

from utils.loader import calcular_agua, calcular_ingredientes

# Porcentajes reales de tu fórmula (16 ingredientes sobre agua)
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
    """
    1. Calcula el agua base con la fórmula original.
    2. Luego calcula los ingredientes según % sobre agua.
    3. Devuelve valores en KILOS.
    """
    agua = calcular_agua(cantidad_chuletas, factor_agua)

    ingredientes_gramos = calcular_ingredientes(agua, PORCENTAJES_BASE)

    # Convertimos todo a kilos para la app
    ingredientes_kilos = {k: round(v / 1000, 4) for k, v in ingredientes_gramos.items()}

    agua_kilos = round(agua / 1000, 4)

    return agua_kilos, ingredientes_kilos


def recalcular_con_agua_manual(agua_manual_kilos: float):
    """
    Si el usuario ingresa un valor de agua manual en KILOS:
    - Recalcula los ingredientes con ese valor.
    - No toca la cantidad de chuletas.
    - Devuelve todo en kilos.
    """
    # Convertimos a gramos para usar el cargador original
    agua_gramos = agua_manual_kilos * 1000

    ingredientes_gramos = calcular_ingredientes(agua_gramos, PORCENTAJES_BASE)

    ingredientes_kilos = {k: round(v / 1000, 4) for k, v in ingredientes_gramos.items()}

    return ingredientes_kilos
