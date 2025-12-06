import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import os

st.set_page_config(page_title="Formula Chuleta", layout="wide")

# Cargar base
@st.cache_data
def cargar_base():
    df = pd.read_csv("base_formula.csv", sep=";")
    df["% sobre agua"] = df["% sobre agua"].astype(float)
    return df

df = cargar_base()

st.title("🧪 App Fórmula Chuleta")

# --- Entrada de cantidad de agua ---
col1, col2 = st.columns(2)
with col1:
    agua_kg = st.number_input("Cantidad de agua (kg)", min_value=0.0, value=100.0, step=1.0)

# --- Cálculo de cantidades ---
df["Cantidad_editada_kg"] = df["% sobre agua"] * agua_kg

# Crear copia para mostrar
df_display = df.copy()
df_display["% sobre agua"] = df_display["% sobre agua"].astype(float)

# --- Mostrar tabla ---
st.dataframe(
    df_display[["Ingrediente", "% sobre agua", "Cantidad_editada_kg"]]
    .rename(columns={"Cantidad_editada_kg": "Cantidad (kg)"})
    .style.format({
        "% sobre agua": "{:.2f}",
        "Cantidad (kg)": "{:.3f}"
    })
)

# --- Generar imagen con numeración entera desde 0 ---
img_width = 800
img_height = 40 * len(df) + 60
img = Image.new("RGB", (img_width, img_height), "white")
draw = ImageDraw.Draw(img)

try:
    font = ImageFont.truetype("arial.ttf", 20)
except:
    font = ImageFont.load_default()

y = 20
for idx, row in df_display.iterrows():
    linea = f"{int(idx)}. {row['Ingrediente']} — {row['Cantidad_editada_kg']:.3f} kg"
    draw.text((20, y), linea, fill="black", font=font)
    y += 40

# Guardar imagen
output_path = "formula_generada.png"
img.save(output_path)

st.image(output_path, caption="Imagen generada", use_column_width=True)


