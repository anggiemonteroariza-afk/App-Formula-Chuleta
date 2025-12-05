import sys
import os
import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
import matplotlib.pyplot as plt

# --------------------------------------------------------------------
# AÑADE LA CARPETA utils AL PATH PARA IMPORTAR calculos.py
# --------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UTILS_DIR = os.path.join(BASE_DIR, "utils")

if UTILS_DIR not in sys.path:
    sys.path.append(UTILS_DIR)

from calculos import calcular_formula   # ahora sí funciona siempre


# --------------------------------------------------------------------
# CONFIGURACIÓN DE STREAMLIT
# --------------------------------------------------------------------
st.set_page_config(
    page_title="App Fórmula Chuleta",
    layout="centered"
)

st.title("📘 Calculadora de Fórmula de Chuleta Ahumada")


# --------------------------------------------------------------------
# FORMULARIO DE ENTRADA
# --------------------------------------------------------------------
with st.form("formulario"):

    fecha = st.date_input("📅 Fecha de producción", datetime.today())

    num_chuletas = st.number_input(
        "Cantidad de chuletas",
        min_value=1,
        step=1,
        value=1
    )

    submitted = st.form_submit_button("🔍 Calcular fórmula")


# --------------------------------------------------------------------
# SOLO CALCULAR CUANDO SE PRESIONA EL BOTÓN
# --------------------------------------------------------------------
if submitted:

    df, agua_base = calcular_formula(num_chuletas)

    st.subheader("📊 Resultado de la fórmula")

    st.dataframe(df, use_container_width=True)

    st.markdown(f"💧 **Agua base total:** {agua_base:.3f} kg")

    # ---------------------------------------------------------
    # FUNCIÓN PARA GENERAR IMAGEN ORDENADA COMO TABLA
    # ---------------------------------------------------------
    def generar_imagen_tabla(dataframe):

        fig, ax = plt.subplots(figsize=(8, 3 + len(dataframe) * 0.4))

        ax.axis("off")

        tabla = ax.table(
            cellText=dataframe.values,
            colLabels=dataframe.columns,
            cellLoc="center",
            loc="center"
        )

        tabla.auto_set_font_size(False)
        tabla.set_fontsize(9)
        tabla.scale(1, 1.3)

        buffer = BytesIO()
        plt.savefig(buffer, format="png", dpi=300, bbox_inches="tight")
        buffer.seek(0)

        return buffer

    # Generar imagen
    img_tabla = generar_imagen_tabla(df)

    st.download_button(
        label="📥 Descargar tabla como imagen",
        data=img_tabla,
        file_name=f"formula_chuleta_{fecha}.png",
        mime="image/png"
    )
