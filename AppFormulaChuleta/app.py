import streamlit as st
from datetime import datetime
import pandas as pd
from utils.calculos import obtener_calculo_completo, recalcular_con_agua_manual, PORCENTAJES_BASE
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

    peso_chuletas = st.number_input(
        "Peso total del lote (kg)",
        min_value=0.0,
        step=0.1
    )

    submitted = st.form_submit_button("🔍 Calcular fórmula")

# Solo calculamos cuando el usuario presiona el botón
if submitted:

    # Cálculo de la fórmula
    agua_total, ingredientes = obtener_calculo_completo(num_chuletas)

    st.subheader("📊 Resultado de la fórmula")

    # Convertir dict a DataFrame ordenado
    df = pd.DataFrame({
        "Ingrediente": ["Agua potable"] + list(ingredientes.keys()),
        "% sobre agua": ["-"] + list(PORCENTAJES_BASE.values()),
        "Cantidad (kg)": [agua_total] + list(ingredientes.values())
    })

    # --- editable solo el agua ---
    df["Cantidad_editada_kg"] = df["Cantidad (kg)"]

    # índice del agua
    idx_agua = 0

    nuevo_agua = st.number_input(
        "💧 Editar agua manual (kg/L):",
        value=float(df.loc[idx_agua, "Cantidad (kg)"]),
        min_value=0.0
    )

    # Actualizar solo la vista
    df.loc[idx_agua, "Cantidad_editada_kg"] = nuevo_agua

    # ---------------------------------------------------------
    # PREPARAR TABLA PARA MOSTRAR SIN ERRORES
    # ---------------------------------------------------------
    df_display = df.copy()

    # Convertir columnas a numérico excepto los "-"
    df_display["% sobre agua"] = pd.to_numeric(df_display["% sobre agua"], errors="coerce")
    df_display["Cantidad_editada_kg"] = pd.to_numeric(df_display["Cantidad_editada_kg"], errors="coerce")

    # Mostrar tabla con formato seguro
    st.dataframe(
        df_display[["Ingrediente", "% sobre agua", "Cantidad_editada_kg"]]
        .rename(columns={"Cantidad_editada_kg": "Cantidad (kg)"})
        .style.format({
            "Cantidad (kg)": "{:.3f}",
            "% sobre agua": lambda x: "-" if pd.isna(x) else "{:.2f}".format(x)
        })
    )

    st.markdown(f"💧 **Agua base total calculada:** {agua_total:.3f} kg")

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

    imagen_tabla = generar_imagen_tabla(
        df_display[["Ingrediente", "% sobre agua", "Cantidad_editada_kg"]]
        .rename(columns={"Cantidad_editada_kg": "Cantidad (kg)"})
    )

    st.download_button(
        label="📥 Descargar tabla en imagen",
        data=imagen_tabla,
        file_name=f"formula_chuleta_{fecha}.png",
        mime="image/png"
    )

    st.success("Cálculo listo 🎉 Puedes editar el agua sin afectar los cálculos base.")
