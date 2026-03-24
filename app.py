import streamlit as st
from telegram_builder import build_from_template, split_message, send_to_telegram
from templates import TEMPLATES
from config import BOT_TOKEN, CHAT_ID

st.set_page_config(page_title="Telegram Builder", layout="wide")

st.title("📨 Generador de Reportes")

# =========================
# SELECTOR DE TEMPLATE
# =========================
template_name = st.selectbox(
    "Tipo de reporte",
    list(TEMPLATES.keys())
)

# =========================
# INPUTS
# =========================
st.subheader("Datos generales")

titulo = st.text_input("Título")
fecha = st.text_input("Fecha")
menciones = st.text_input("Menciones")

# =========================
# LÍNEAS
# =========================
st.subheader("Líneas de discusión")
lineas = st.text_area("Una por línea").split("\n")

# =========================
# CITAS
# =========================
st.subheader("Citas")
citas = st.text_area("Una por línea").split("\n")

# =========================
# AUTORES
# =========================
st.subheader("Autores")

autores_raw = st.text_area(
    "Formato: nombre | url | descripción"
)

autores = []
for linea in autores_raw.split("\n"):
    if "|" in linea:
        nombre, url, desc = linea.split("|")
        autores.append({
            "name": nombre.strip(),
            "url": url.strip(),
            "desc": desc.strip()
        })

# =========================
# DATA FINAL
# =========================
data = {
    "titulo": titulo,
    "fecha": fecha,
    "menciones": menciones,
    "lineas": [l for l in lineas if l.strip()],
    "citas": [c for c in citas if c.strip()],
    "autores": autores
}

# =========================
# PREVIEW
# =========================
if st.button("👁️ Previsualizar"):
    resultado = build_from_template(template_name, data, TEMPLATES)

    st.markdown("### Preview (como Telegram)")
    st.markdown(resultado, unsafe_allow_html=True)

# =========================
# ENVIAR
# =========================
if st.button("🚀 Enviar a Telegram"):
    resultado = build_from_template(template_name, data, TEMPLATES)
    partes = split_message(resultado)

    for parte in partes:
        send_to_telegram(parte, BOT_TOKEN, CHAT_ID)

    st.success("✅ Enviado correctamente")
