import streamlit as st
from datetime import datetime
import pandas as pd
from utils.calculos import obtener_calculo_completo, PORCENTAJES_BASE
from io import BytesIO
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# CONFIGURACIÓN DE PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="App Fórmula Chuleta",
    layout="centered"
)

st.title("📘 Fórmula de Chuleta")

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

# ---------------------------------------------------------
# PROCESAMIENTO
# ---------------------------------------------------------
if submitted:

    # 1️⃣ Obtener cálculos base
    agua_total, ingredientes = obtener_calculo_completo(num_chuletas)

    st.subheader("📊 Resultado de la fórmula")

    # Ordenar datos para tabla principal (ingredientes es dict nombre->kg)
    df = pd.DataFrame({
        "Ingrediente": ["Agua potable"] + list(ingredientes.keys()),
        "% sobre agua": ["-"] + list(PORCENTAJES_BASE.values()),
        "Cantidad (kg)": [agua_total] + list(ingredientes.values())
    })

    # Copia editable SOLO del agua
    df["Cantidad_editada_kg"] = df["Cantidad (kg)"]
    idx_agua = 0

    nuevo_agua = st.number_input(
        "💧 Editar agua manual (kg/L):",
        value=float(df.loc[idx_agua, "Cantidad (kg)"]),
        min_value=0.0
    )

    df.loc[idx_agua, "Cantidad_editada_kg"] = nuevo_agua

    # Guardamos esta versión para la imagen / visualización
    df_display = df.copy()

    # ---------------------------------------------------------
    # LIMPIAMOS/CONVERTIMOS LAS COLUMNAS QUE SE VAN A FORMATEAR
    # - Convertimos a numérico con errors='coerce' (saltará NaN donde estaba "-")
    # - Mantendremos el "-" en la visualización usando lambdas en style.format
    # ---------------------------------------------------------
    df_display["% sobre agua_numeric"] = pd.to_numeric(df_display["% sobre agua"], errors="coerce")
    df_display["Cantidad_editada_numeric"] = pd.to_numeric(df_display["Cantidad_editada_kg"], errors="coerce")

    # Mostrar tabla con formato seguro: dejar '-' si NaN en % y mostrar cantidades con 3 decimales
    display_df = df_display[["Ingrediente", "% sobre agua_numeric", "Cantidad_editada_numeric"]].copy()
    display_df = display_df.rename(columns={
        "% sobre agua_numeric": "% sobre agua",
        "Cantidad_editada_numeric": "Cantidad (kg)"
    })

    st.dataframe(
        display_df.style.format({
            "Cantidad (kg)": lambda x: f"{x:.3f}" if pd.notna(x) else "",
            "% sobre agua": lambda x: "-" if pd.isna(x) else f"{x:.2f}"
        })
    )

    st.markdown(f"💧 **Agua base total calculada:** {agua_total:.3f} kg")

    # ---------------------------------------------------------
    # GENERAR IMAGEN ORDENADA COMO TABLA (solo consecutivo + cantidad con 3 decimales)
    # ---------------------------------------------------------
    def generar_imagen_tabla(dataframe, fecha, num_chuletas, peso_chuletas):
        # dataframe debe tener la columna "Cantidad_editada_kg" original o numérica
        # Construimos df_img con consecutivo y cantidad redondeada a 3 decimales
      df_img = pd.DataFrame({
    "N°": range(0, len(dataframe)),   # inicia en 0
    "Cantidad (kg)": dataframe["Cantidad_editada_kg"].astype(float).round(3)
})
        fig, ax = plt.subplots(figsize=(8, 4 + len(df_img) * 0.35))
        ax.axis('off')

        # Encabezado superior
        encabezado = (
            f"Fecha: {fecha}\n"
            f"Cantidad de chuletas: {num_chuletas}\n"
            f"Peso total del lote: {peso_chuletas} kg"
        )

        ax.text(
            0.5, 1.05, encabezado,
            ha='center', va='top',
            fontsize=11, transform=ax.transAxes
        )

        tabla = ax.table(
            cellText=df_img.values,
            colLabels=df_img.columns,
            cellLoc='center',
            loc='center'
        )

        tabla.auto_set_font_size(False)
        tabla.set_fontsize(9)
        tabla.scale(1, 1.2)

        buf = BytesIO()
        plt.savefig(buf, format="png", dpi=300, bbox_inches="tight")
        buf.seek(0)
        return buf

    # Crear imagen final usando la vista con la edición del agua
    imagen_tabla = generar_imagen_tabla(
        dataframe=df_display,
        fecha=fecha,
        num_chuletas=num_chuletas,
        peso_chuletas=peso_chuletas
    )

    # Botón de descarga
    st.download_button(
        label="📥 Descargar tabla en imagen",
        data=imagen_tabla,
        file_name=f"formula_chuleta_{fecha}.png",
        mime="image/png"
    )

    st.success("Cálculo listo 🎉 Puedes editar el agua sin afectar los cálculos base.")


