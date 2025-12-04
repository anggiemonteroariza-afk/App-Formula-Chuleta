# utils/loader.py

def calcular_agua(cantidad_chuletas: int, factor_agua: float = 3.0) -> float:
    """
    Calcula los litros de agua requeridos según la cantidad de chuletas.
    factor_agua = litros por chuleta (por defecto 3 L).
    """
    if cantidad_chuletas < 0:
        raise ValueError("La cantidad de chuletas no puede ser negativa.")
    return cantidad_chuletas * factor_agua


def calcular_ingredientes(agua_litros: float, porcentajes: dict) -> dict:
    """
    Calcula la cantidad de ingredientes en gramos/ml según el % definido
    sobre la cantidad de agua.

    porcentajes = diccionario con valores en % ej:
        {"sal": 3.2, "azucar": 2.1, "fosfato": 0.3}
    """
    ingredientes = {}
    for nombre, porcentaje in porcentajes.items():
        ingredientes[nombre] = agua_litros * (porcentaje / 100)
    return ingredientes
