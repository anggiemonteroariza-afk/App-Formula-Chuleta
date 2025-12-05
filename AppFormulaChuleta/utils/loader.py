# utils/loader.py

def calcular_agua(cantidad_chuletas: int, factor_agua: float = 3.0) -> float:
    """
    Calcula litros/kg de agua según cantidad de chuletas.
    """
    return cantidad_chuletas * factor_agua


def calcular_ingredientes(agua_kg: float, porcentajes: dict) -> dict:
    """
    Aplica % sobre agua y retorna cantidades en kg.
    """
    ingredientes = {}
    for nombre, porcentaje in porcentajes.items():
        ingredientes[nombre] = agua_kg * (porcentaje / 100)
    return ingredientes
