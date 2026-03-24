import streamlit as st
from telegram_builder import build_from_template, split_message, send_to_telegram
from templates import TEMPLATES
import os

BOT_TOKEN = st.secrets.get("BOT_TOKEN") or os.getenv("BOT_TOKEN")
CHAT_ID = st.secrets.get("CHAT_ID") or os.getenv("CHAT_ID")

def builder_ui():

    st.title("📨 Generador de Reportes")

    template_name = st.selectbox(
        "Tipo de reporte",
        list(TEMPLATES.keys())
    )

    st.subheader("Datos generales")

    titulo = st.text_input("Título")
    fecha = st.text_input("Fecha")
    menciones = st.text_input("Menciones")

    st.subheader("Líneas de discusión")
    lineas = st.text_area("Una por línea", key="builder_lineas").split("\n")

    st.subheader("Citas")
    citas = st.text_area("Una por línea", key="builder_citas").split("\n")

    st.subheader("Autores")

    autores_raw = st.text_area(
        "Formato: nombre | url | descripción",
        key="builder_autores"
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

    data = {
        "titulo": titulo,
        "fecha": fecha,
        "menciones": menciones,
        "lineas": [l for l in lineas if l.strip()],
        "citas": [c for c in citas if c.strip()],
        "autores": autores
    }

    if st.button("👁️ Previsualizar"):
        resultado = build_from_template(template_name, data, TEMPLATES)
        st.markdown("### Preview (como Telegram)")
        st.markdown(resultado, unsafe_allow_html=True)

    if st.button("🚀 Enviar a Telegram"):
        resultado = build_from_template(template_name, data, TEMPLATES)
        partes = split_message(resultado)

        for parte in partes:
            send_to_telegram(parte, BOT_TOKEN, CHAT_ID)

        st.success("✅ Enviado correctamente")
