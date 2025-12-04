import streamlit as st
import pandas as pd
from utils.calculos import obtener_calculo_completo, recalcular_con_agua_manual
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="Fórmula Chuleta", layout="centered")

st.title("🟢 Cálculo de Fórmula para Chuleta Ahumada")

# ---- ENTRADAS ----
st.subheader("Datos del lote")

col1, col2 = st.columns(2)

with col1:
    num_chuletas = st.number_input(
        "Cantidad de chuletas a procesar:",
        min_value=1,
        value=1
    )

with col2:
    peso_chuletas = st.number_input(
        "Peso total del lote (kg):",
        min_value=0.0,
        value=0.0
    )

# ---- CÁLCULOS ----
df, agua_base = calcular_formula(num_chuletas)

st.markdown("---")
st.subheader("Ingredientes y cantidades")

# Agregamos columna editable para el agua
df["Cantidad_editada_kg"] = df["Cantidad_base_kg"]

# Ubicar la fila del agua
agua_idx = df.index[df["Ingrediente"] == "Agua potable"][0]

nuevo_valor_agua = st.number_input(
    "Editar cantidad de agua (kg/L):",
    value=float(df.loc[agua_idx, "Cantidad_base_kg"]),
    min_value=0.0
)

# Actualizar solo la vista, NO los cálculos
df.loc[agua_idx, "Cantidad_editada_kg"] = nuevo_valor_agua

# Mostrar tabla final
st.dataframe(
    df[["Ingrediente", "% sobre agua", "Cantidad_editada_kg"]]
        .rename(columns={"Cantidad_editada_kg": "Cantidad (kg)"})
        .style.format({"Cantidad (kg)": "{:.3f}"})
)

st.markdown("---")

# ---- GENERAR IMAGEN ----
st.subheader("Descargar imagen del lote")

if st.button("Generar y descargar imagen"):
    # Crear imagen blanca
    img = Image.new("RGB", (900, 1400), "white")
    draw = ImageDraw.Draw(img)

    # Fuente
    try:
        font = ImageFont.truetype("arial.ttf", 28)
    except:
        font = ImageFont.load_default()

    y = 40
    draw.text((40, y), f"LOTE DE CHULETAS", font=font, fill="black")
    y += 50
    draw.text((40, y), f"Cantidad de chuletas: {num_chuletas}", font=font, fill="black")
    y += 40
    draw.text((40, y), f"Peso total ingresado: {peso_chuletas} kg", font=font, fill="black")
    y += 60

    draw.text((40, y), "Ingredientes (solo número y cantidad):", font=font, fill="black")
    y += 40

    # Ingredientes numerados sin nombre
    for i, row in df.iterrows():
        numero = i + 1
        cantidad = row["Cantidad_editada_kg"]
        txt = f"{numero}.  {cantidad:.3f} kg"
        draw.text((40, y), txt, font=font, fill="black")
        y += 35

    # Guardar en buffer
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    st.download_button(
        label="Descargar imagen",
        data=buffer,
        file_name="lote_chuletas.png",
        mime="image/png"
    )

st.markdown("---")
st.success("Cálculo completo. Puedes editar el agua sin afectar la fórmula y descargar la imagen del lote.")

