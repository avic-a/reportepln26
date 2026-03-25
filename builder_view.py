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

    # =========================
    # LÍNEAS
    # =========================
    st.subheader("Líneas de discusión")
    lineas = st.text_area("Esta sección permite incluir lineas en fragmentos del texto el formato es: Texto [texto con url] - https://fb.com. Hacer intro cada que haya una nueva linea", key="builder_lineas").split("\n")

    # =========================
    # CITAS
    # =========================
    st.subheader("Texto en lista y con Vínculo")

    citas_titulo = st.text_input(
        "Título de sección",
        value="Citas clave"
    )
    
    citas_desc = st.text_area(
        "Descripción (opcional)",
        key="citas_desc"
    )
    num_citas = st.number_input("Número de elementos", 1, 10, 3)

    citas = []

    for i in range(num_citas):
        col1, col2 = st.columns([2, 3])

        with col1:
            texto = st.text_input(f"Texto con vínculo {i+1}", key=f"builder_cita_texto_{i}")

        with col2:
            url = st.text_input(f"URL {i+1}", key=f"builder_cita_url_{i}")

        if texto:
            citas.append({
                "text": texto,
                "url": url
            })

    # =========================
    # AUTORES
    # =========================
    st.subheader("Texto en lista con Vínculo y descripción")
    
    autores_titulo = st.text_input(
        "Título de sección",
        value="Autores"
    )
    
    autores_desc = st.text_area(
        "Descripción (opcional)",
        key="autores_desc"
    )
    num_autores = st.number_input(
        "Número de elementos",
        1, 15, 3,
        key="builder_num_autores"
    )

    autores = []

    for i in range(num_autores):
        col1, col2, col3 = st.columns([2, 3, 4])

        with col1:
            nombre = st.text_input(f"Texto con vínculo {i+1}", key=f"builder_autor_nombre_{i}")

        with col2:
            url = st.text_input(f"URL {i+1}", key=f"builder_autor_url_{i}")

        with col3:
            desc = st.text_input(f"Descripción {i+1}", key=f"builder_autor_desc_{i}")

        if nombre:
            autores.append({
                "name": nombre,
                "url": url,
                "desc": desc
            })

    # =========================
    # DATA FINAL
    # =========================
    data = {
        "titulo": titulo,
        "fecha": fecha,
        "menciones": menciones,
        "lineas": [l for l in lineas if l.strip()],
        "citas": citas,
        "autores": autores,
        "citas_titulo": f"<b>{citas_titulo}</b>" if citas_titulo else "",
        "citas_desc": citas_desc.strip(),
        "autores_titulo": f"<b>{autores_titulo}</b>" if autores_titulo else "",
        "autores_desc": autores_desc.strip()
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
            res = send_to_telegram(parte, BOT_TOKEN, CHAT_ID)
            # 👇 NUEVO: Validar si Telegram aceptó el mensaje
            if not res.get("ok"):
                st.error(f"Error de Telegram: {res.get('description')}")
                st.stop() # Detiene la ejecución si hay error

        st.success("✅ Enviado correctamente")
