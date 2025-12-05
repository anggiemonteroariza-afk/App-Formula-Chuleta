import streamlit as st
import pandas as pd
from utils.calculos import obtener_calculo_completo
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

# ---- CÁLCULO
