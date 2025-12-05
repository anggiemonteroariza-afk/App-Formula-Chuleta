import streamlit as st
from datetime import datetime
import pandas as pd
from calculos import obtener_calculo_completo
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

    num_chuletas = st.number_input(
        "Cantidad de chuletas",
        min_value=1,
        step=1
    )

    submitted = st.form_submit_button("🔍 Calcular fórmula")

# ---------------------------------------------------------
# SOLO CALCULAR SI SE PRESIONA EL BOTÓN
# ---------------------------------------------------------
if submitted:

    agua_total, ingredientes = obtener_calculo_completo(num_chuletas)

    st.subheader("📊 Resultado de la fórmula")

    # Construir DataFrame para mostrarlo en Streamlit
    df = pd.DataFrame({
        "Ingrediente": [i["ingrediente"] for i in ingredientes],
        "Porcentaje (%)": [i["porcentaje"] for i in ingredientes],
        "Cantidad (kg)": [i["cantidad"] for i in ingredientes],
    })

    st.dataframe(df, use_container_width=True)

    st.markdown(f"💧 **Agua total:** {agua_total:.3f} kg")


    # ---------------------------------------------------------
    # GENERAR IMAGEN ORDENADA COMO TABLA
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
        label="📥 Descargar tabla en imagen",
        data=imagen_tabla,
        file_name=f"formula_chuleta_{fecha}.png",
        mime="image/png"
    )
