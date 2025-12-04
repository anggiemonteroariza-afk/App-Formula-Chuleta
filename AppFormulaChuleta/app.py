import streamlit as st
from utils.calculos import (
    obtener_calculo_completo,
    recalcular_con_agua_manual,
)

st.set_page_config(page_title="Cálculo de Inyección – Chuleta Ahumada", layout="centered")

st.title("💧 Cálculo de Inyección para Chuleta Ahumada")

st.markdown("Calculadora completa según tu fórmula real de 16 ingredientes.")

# -------------------------------------------------------
# 1. Entrada de datos
# -------------------------------------------------------
st.subheader("🔢 Datos de entrada")

col1, col2 = st.columns(2)

with col1:
    cantidad_chuletas = st.number_input(
        "Cantidad de chuletas a procesar",
        min_value=0,
        step=1,
        format="%d"
    )

with col2:
    peso_total = st.number_input(
        "Peso total de la chuleta (kg) – Solo control",
        min_value=0.0,
        step=0.1,
        format="%.2f"
    )

factor_agua = 3.0  # L por chuleta


# -------------------------------------------------------
# 2. Cálculo automático
# -------------------------------------------------------
if cantidad_chuletas > 0:
    agua_calculada, ingredientes_base = obtener_calculo_completo(
        cantidad_chuletas,
        factor_agua
    )

    st.subheader("💧 Agua calculada automáticamente")
    st.write(f"**{agua_calculada:.2f} L** (3 L por chuleta)")

    # -------------------------------------------------------
    # 3. Ajuste manual del agua
    # -------------------------------------------------------
    st.subheader("✏️ Ajustar agua manualmente (opcional)")

    agua_final = st.number_input(
        "Cantidad final de agua (L)",
        value=float(agua_calculada),
        min_value=0.0,
        step=0.1,
        format="%.2f"
    )

    if agua_final != agua_calculada:
        ingredientes = recalcular_con_agua_manual(agua_final)
        st.info("Se recalcularon los ingredientes con el agua editada manualmente.")
    else:
        ingredientes = ingredientes_base

    # -------------------------------------------------------
    # 4. Tabla de ingredientes
    # -------------------------------------------------------
    st.subheader("🧂 Ingredientes requeridos")

    tabla = {
        "Ingrediente": [],
        "Cantidad (g / ml)": []
    }

    for nombre, valor in ingredientes.items():
        tabla["Ingrediente"].append(nombre)
        tabla["Cantidad (g / ml)"].append(round(valor, 2))

    st.table(tabla)

else:
    st.warning("Ingresa la cantidad de chuletas para iniciar el cálculo.")
