import streamlit as st
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import io
import datetime

st.set_page_config(page_title="Fórmula Chuleta", layout="wide")

st.title("🧪 Calculadora de Fórmula de Chuletas")

# ---------------------------
# INGREDIENTES ORIGINALES (16)
# ---------------------------
ingredientes = [
    {"ingrediente": "Carne de cerdo", "porcentaje": 0.57},
    {"ingrediente": "Hielo", "porcentaje": 0.18},
    {"ingrediente": "Almidón de maíz", "porcentaje": 0.05},
    {"ingrediente": "Harina de trigo", "porcentaje": 0.03},
    {"ingrediente": "Sal", "porcentaje": 0.015},
    {"ingrediente": "Fosfatos", "porcentaje": 0.003},
    {"ingrediente": "Azúcar", "porcentaje": 0.005},
    {"ingrediente": "Ajo", "porcentaje": 0.004},
    {"ingrediente": "Cebolla", "porcentaje": 0.004},
    {"ingrediente": "Pimienta", "porcentaje": 0.001},
    {"ingrediente": "Comino", "porcentaje": 0.001},
    {"ingrediente": "Color caramelo", "porcentaje": 0.002},
    {"ingrediente": "Conservante", "porcentaje": 0.001},
    {"ingrediente": "Saborizante", "porcentaje": 0.002},
    {"ingrediente": "Estabilizante", "porcentaje": 0.002},
    {"ingrediente": "Agua", "porcentaje": 0.1}  # Se puede editar PERO NO afecta cálculos
]

# ---------------------------
# ENTRADAS
# ---------------------------
col1, col2, col3 = st.columns(3)

with col1:
    fecha = st.date_input("Fecha del proceso", datetime.date.today())

with col2:
    cantidad_chuletas = st.number_input("Cantidad de chuletas", min_value=1, value=1)

with col3:
    peso_chuleta = st.number_input("Peso por chuleta (kg)", min_value=0.01, value=0.15)

peso_total = cantidad_chuletas * peso_chuleta

st.markdown(f"### 🟦 Peso total: **{peso_total:.3f} kg**")

# --------------------------------
# PERMITIR EDITAR SOLO EL AGUA
# --------------------------------
for ingr in ingredientes:
    if ingr["ingrediente"] == "Agua":
        nuevo = st.number_input("Editar agua (%)", value=float(ingr["porcentaje"]), format="%.3f")
        ingr["porcentaje"] = nuevo  # Solo cambia lo visual, NO afecta cálculos

# ---------------------------
# CÁLCULOS DE FORMULACIÓN
# ---------------------------
df = pd.DataFrame({
    "Ingrediente": [i["ingrediente"] for i in ingredientes],
    "Porcentaje (%)": [i["porcentaje"] for i in ingredientes]
})

df["Cantidad (kg)"] = df["Porcentaje (%)"] * peso_total
df["Cantidad (kg)"] = df["Cantidad (kg)"].round(3)

st.subheader("📋 Fórmula calculada")
st.dataframe(df, use_container_width=True)

# ---------------------------
# GENERAR IMAGEN
# ---------------------------
if st.button("Generar imagen de fórmula"):
    img = Image.new("RGB", (900, 1300), color="white")
    draw = ImageDraw.Draw(img)

    try:
        font_title = ImageFont.truetype("arial.ttf", 40)
        font_text = ImageFont.truetype("arial.ttf", 30)
    except:
        font_title = ImageFont.load_default()
        font_text = ImageFont.load_default()

    # Título
    draw.text((50, 30), "FÓRMULA DE CHULETAS", fill="black", font=font_title)

    # Datos generales
    draw.text((50, 120), f"Fecha: {fecha}", fill="black", font=font_text)
    draw.text((50, 170), f"Cantidad de chuletas: {cantidad_chuletas}", fill="black", font=font_text)
    draw.text((50, 220), f"Peso unitario: {peso_chuleta:.3f} kg", fill="black", font=font_text)
    draw.text((50, 270), f"Peso total: {peso_total:.3f} kg", fill="black", font=font_text)

    # Tabla de ingredientes
    draw.text((50, 340), "No.     Cantidad (kg)", fill="black", font=font_text)

    y = 390
    for idx, row in df.iterrows():
        numero = int(idx)  # 🔥 AHORA SIEMPRE ENTERO DESDE 0
        cantidad = f"{row['Cantidad (kg)']:.3f}"

        draw.text((50, y), f"{numero}", fill="black", font=font_text)
        draw.text((200, y), cantidad, fill="black", font=font_text)

        y += 40

    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    st.image(img, caption="Fórmula generada")

    st.download_button(
        label="Descargar imagen",
        data=buffer,
        file_name="formula_chuletas.png",
        mime="image/png"
    )
