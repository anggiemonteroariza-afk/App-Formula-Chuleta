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

    # Si se presionó, guardamos una marca en session_state para que la vista persista
    if submitted:
        st.session_state["calculated"] = True

# Mostrar si ya se calculó en este flujo (evita que editar inputs borre la tabla)
should_show = submitted or st.session_state.get("calculated", False)

# ---------------------------------------------------------
# PROCESAMIENTO (solo se muestra si se ha calculado)
# ---------------------------------------------------------
if should_show:

    # 1️⃣ Obtener cálculos base
    agua_total, ingredientes = obtener_calculo_completo(num_chuletas)

    st.subheader("📊 Resultado de la fórmula")

    # Ordenar datos para tabla principal
    df = pd.DataFrame({
        "Ingrediente": ["Agua potable"] + list(ingredientes.keys()),
        "% sobre agua": ["-"] + list(PORCENTAJES_BASE.values()),
        "Cantidad (kg)": [agua_total] + list(ingredientes.values())
    })

    # Copia editable SOLO del agua
    df["Cantidad_editada_kg"] = df["Cantidad (kg)"]
    idx_agua = 0

    # Inicializar valor de agua editada en session_state si no existe
    if "water_edit" not in st.session_state:
        st.session_state["water_edit"] = float(df.loc[idx_agua, "Cantidad (kg)"])

    # ---------------------------------------------------------
    # CAMBIO: input con key persistente; editarlo actualiza la vista
    # ---------------------------------------------------------
    nuevo_agua = st.number_input(
        "💧 Editar agua manual (kg/L):",
        value=st.session_state["water_edit"],
        min_value=0.0,
        step=0.001,
        format="%.3f",
        key="water_edit_input"
    )

    # Volcar el valor persistente en session_state para que permanezca entre reruns
    st.session_state["water_edit"] = float(nuevo_agua)

    # Actualizamos solo la vista (NO recalculamos ingredientes)
    df.loc[idx_agua, "Cantidad_editada_kg"] = st.session_state["water_edit"]

    # Guardamos esta versión para la imagen
    df_display = df.copy()

    # ---------------------------------------------------------
    # MOSTRAR TABLA: formatear sólo la columna de kilos (evita errores)
    # ---------------------------------------------------------
    # Aseguramos que la columna a formatear sea numérica para no romper styler
    df_display["Cantidad_editada_kg"] = pd.to_numeric(df_display["Cantidad_editada_kg"], errors="coerce").fillna(0)

    st.dataframe(
        df_display[["Ingrediente", "% sobre agua", "Cantidad_editada_kg"]]
        .rename(columns={"Cantidad_editada_kg": "Cantidad (kg)"})
        .style.format({"Cantidad (kg)": "{:.3f}"})
    )

    st.markdown(f"💧 **Agua base total calculada:** {agua_total:.3f} kg")

    # ---------------------------------------------------------
    # GENERAR IMAGEN ORDENADA COMO TABLA
    # ---------------------------------------------------------
    def generar_imagen_tabla(dataframe, fecha, num_chuletas, peso_chuletas):

        # Numeración inicia en 0 y se guarda como texto sin decimales
        df_img = pd.DataFrame({
            "N°": [str(i) for i in range(0, len(dataframe))],
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

    # Crear imagen final
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
