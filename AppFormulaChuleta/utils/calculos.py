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
    1. Calcula el agua base (en L); tratamos 1 L ~= 1 kg, por lo tanto lo devolvemos como kg.
    2. Calcula los ingredientes en KILOS usando los porcentajes sobre el agua.
    Devuelve: agua_kg (float), ingredientes_kilos (dict nombre->kg), porcentajes (dict)
    """
    # calcular_agua devuelve litros (porque factor_agua está en L/chuleta)
    agua_litros = calcular_agua(cantidad_chuletas, factor_agua)  # ej: 3 * n
    agua_kg = float(agua_litros)  # 1 L ≈ 1 kg, lo manejamos como kg

    # calcular_ingredientes espera agua en (kg o L) y devuelve cantidad en la misma unidad (kg)
    ingredientes_kilos = calcular_ingredientes(agua_kg, PORCENTAJES_BASE)  # ya retorna kg

    # asegurar redondeo razonable
    ingredientes_kilos = {k: round(v, 6) for k, v in ingredientes_kilos.items()}

    return agua_kg, ingredientes_kilos, PORCENTAJES_BASE


def recalcular_con_agua_manual(agua_manual_kg: float):
    """
    Recalcula los ingredientes a partir de un agua manual (kg).
    Devuelve dict nombre->kg y porcentajes.
    """
    ingredientes_kilos = calcular_ingredientes(agua_manual_kg, PORCENTAJES_BASE)
    ingredientes_kilos = {k: round(v, 6) for k, v in ingredientes_kilos.items()}
    return ingredientes_kilos, PORCENTAJES_BASE
