import pandas as pd

# ------------------------------------------
# CONFIGURACIÓN
# ------------------------------------------
PESO_CHULETA = 0.160  # kg por chuleta


# ------------------------------------------
# FUNCIÓN PRINCIPAL DE CÁLCULO
# ------------------------------------------
def calcular_formula(num_chuletas):
    """
    Calcula los valores principales (tabla) para la fórmula de chuletas.
    Retorna:
      - DataFrame con ingredientes y cantidades
      - agua_total en litros
    """

    peso_total = num_chuletas * PESO_CHULETA

    ingredientes = {
        "Ingrediente": [
            "Agua",
            "Sal",
            "Azúcar",
            "Fosfatos",
            "Eritorbato",
            "Nitrito",
        ],
        "Porcentaje": [10, 2, 1, 0.3, 0.05, 0.015],  # base estándar
    }

    df = pd.DataFrame(ingredientes)
    df["Cantidad (kg)"] = (df["Porcentaje"] / 100) * peso_total

    agua_total = df.loc[df["Ingrediente"] == "Agua", "Cantidad (kg)"].iloc[0]

    return df, agua_total


# ------------------------------------------
# FUNCIÓN PARA LA IMAGEN
# ------------------------------------------
def obtener_calculo_completo(num_chuletas):
    """
    Devuelve datos más simples para armar la imagen.
    Retorna:
        - agua_total
        - lista de ingredientes con cantidades
    """

    df, agua_total = calcular_formula(num_chuletas)

    ingredientes = [
        {
            "ingrediente": row["Ingrediente"],
            "porcentaje": row["Porcentaje"],
            "cantidad": row["Cantidad (kg)"],
        }
        for _, row in df.iterrows()
    ]

    return agua_total, ingredientes
