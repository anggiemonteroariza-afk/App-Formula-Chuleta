import streamlit as st
from datetime import datetime
import pandas as pd
from utils.calculos import obtener_calculo_completo
from io import BytesIO
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="App Fórmula Chuleta",
    layout="centered"
)

st.title("📘 Calculadora de Fórmula de Chuleta")


# ---------------------------------------------------------
# FORMULARIO DE ENTRADA
# ---------------------------------------------------------
with st.form("formulario"):
    fecha = st.date_input("📅 Fecha de producción", datetime.today())

    col1, col2 = st.columns(2)

    with col1:
        num_chuletas = st.number_input(
            "Cantidad de chuletas",
            min_value=1,
            step=1
        )

    with col2:
        peso_chuletas = st.number_input(
            "Peso total del lote (kg)",
            min_value=0.0,
            step=0.1
        )

    submitted = st.form_submit_button("🔍 Calcular fórmula")

# ---------------------------------------------------------
# SOLO CALCULAMOS CUANDO EL USUARIO PRESIONA EL BOTÓN
# ---------------------------------------------------------
if submitted:

    # Cálculo principal (usa % sobre agua)
    agua_total, ingredientes = obtener_calculo_completo(num_chuletas)

    # Crear DataFrame final
    df = pd.DataFrame({
        "Ingrediente": ["Agua potable"] + list(ingredientes.keys()),
        "% sobre agua": [0.0] + list(ingredientes.values()),
        "Cantidad (kg)": [agua_total] + [agua_total * (p / 100) for p in ingredientes.values()]
    })

    st.subheader("📊 Resultado de la fórmula")

    st.dataframe(df, use_container_width=True)

    st.markdown(f"💧 **Agua total calculada:** {agua_total:.3f} kg")

    # ---------------------------------------------------------
    # GENERAR IMAGEN COMO TABLA
    # ---------------------------------------------------------
    def generar_imagen_tabla(dataframe):
        fig, ax = plt.subplots(figsize=(8, 3 + len(dataframe) * 0.4))

        ax.axis('off')
        tabla = ax.table(
            cellText=dataframe.values,
            colLabels=dataframe.columns,
            cellLoc='center',
            loc='center'
        )

        tabla.auto_set_font_size(False)
        tabla.set_fontsize(9)
        tabla.scale(1, 1.3)

        buf = BytesIO()
        plt.savefig(buf, format="png", dpi=300, bbox_inches="tight")
        buf.seek(0)
        return buf

    imagen_tabla = generar_imagen_tabla(df)

    st.download_button(
        label="📥 Descargar tabla como imagen",
        data=imagen_tabla,
        file_name=f"formula_chuleta_{fecha}.png",
        mime="image/png"
    )
