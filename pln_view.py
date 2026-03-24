import requests
import streamlit as st
import os

BOT_TOKEN = st.secrets.get("BOT_TOKEN") or os.getenv("BOT_TOKEN")
CHAT_ID = st.secrets.get("CHAT_ID") or os.getenv("CHAT_ID")

def pln_ui():
    # todo tu código original

    st.title("Generador de Reporte PLN")

    # ======================
    # HEADER
    # ======================

    fecha = st.text_input("Fecha del reporte")

    # ======================
    # FUENTES
    # ======================
    url_api = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    st.subheader("Fuentes")

    fuentes = {}

    for red in ["Facebook", "Portales", "Twitter", "Tiktok"]:
        col1, col2 = st.columns(2)
        with col1:
            p = st.text_input(f"% {red}", key=f"p_{red}")
        with col2:
            m = st.text_input(f"Menciones {red}", key=f"m_{red}")
        fuentes[red] = (p, m)

    st.subheader("Menciones principales")

    def input_menciones(nombre):
        data = []
        for i in range(3):
            st.write(f"{nombre} {i+1}")
            medio = st.text_input("Medio", key=f"{nombre}_medio_{i}")
            url = st.text_input("Link", key=f"{nombre}_url_{i}")
            texto = st.text_area("Texto", key=f"{nombre}_texto_{i}")
            data.append((medio, url, texto))
        return data

    facebook = input_menciones("Facebook")
    twitter = input_menciones("Twitter")
    portales = input_menciones("Portales")
    st.subheader("Picos")

    # ======================
    # PICOS FACEBOOK (OBLIGATORIOS)
    # ======================

    st.write("Primeros 3 picos (Facebook obligatorios)")

    picos = []

    for i in range(3):
        st.write(f"Pico Facebook {i+1}")
        medio = st.text_input("Medio", key=f"fb_medio_{i}")
        url = st.text_input("Link", key=f"fb_url_{i}")
        texto = st.text_area("Texto", key=f"fb_texto_{i}")
        if medio and url:
            picos.append(("Facebook", medio, url, texto))

    # ======================
    # PICOS EXTRA
    # ======================

    st.write("Picos adicionales")

    num_picos = st.number_input(
        "Número de picos extra",
        min_value=0,
        step=1,
        key="num_picos_extra"
    )

    for i in range(num_picos):
        st.write(f"Pico extra {i+1}")
        fuente = st.text_input("Fuente", key=f"extra_fuente_{i}")
        medio = st.text_input("Medio", key=f"extra_medio_{i}")
        url = st.text_input("Link", key=f"extra_url_{i}")
        texto = st.text_area("Texto", key=f"extra_texto_{i}")
        picos.append((fuente, medio, url, texto))

    st.subheader("Imágenes")

    img1 = st.file_uploader("Gráfica fuentes", type=["png", "jpg"])
    img2 = st.file_uploader("Gráfica picos", type=["png", "jpg"])

    def make_link(text, url):
        return f"<a href='{url}'>{text}</a>"

    def formato_publicacion(medio, url, descripcion):
        return f"📍 {make_link(medio, url)}\n{descripcion}\n"

    if st.button("Enviar reporte"):

        # HEADER
        mensaje_header = f"<b>Reporte {fecha} 2026</b>\n👨🏻‍💼PABLO LEMUS NAVARRO"

        # MENSAJE PRINCIPAL
        mensaje = ""
        mensaje += "<b>FUENTES COMPARTIDAS &gt; PLN 👨🏻‍💼</b>\n"

    # 🔥 ordenar de mayor a menor por porcentaje
        fuentes_ordenadas = sorted(
            fuentes.items(),
            key=lambda x: (
            float(x[1][0]) if x[1][0] else 0,
            int(x[1][1]) if x[1][1] else 0
        ),
            reverse=True
    )

        for red, (p, m) in fuentes_ordenadas:
            mensaje += f"<b>{red}:</b> {p}%, {m} menciones\n"

        mensaje += "\n<b>Menciones con mayores puntos de influencia:</b>\n"

        # FACEBOOK
        mensaje += "<b>Facebook ↓</b>\n"
        for medio, url, texto in facebook:
            mensaje += formato_publicacion(medio, url, texto)

        # TWITTER
        mensaje += "\n<b>Twitter ↓</b>\n"
        for medio, url, texto in twitter:
            mensaje += formato_publicacion(medio, url, texto)

        # PORTALES
        mensaje += "\n<b>Portales ↓</b>\n"
        for medio, url, texto in portales:
            mensaje += formato_publicacion(medio, url, texto)

        # ======================
        # PICOS AGRUPADOS
        # ======================

        mensaje_picos = "<b>MENCIONES EN EL TIEMPO POR FUENTE &gt; PLN👨🏻‍💼</b>\n"

        mensaje_picos += "Respecto a los picos de tendencia de las menciones por fuente, se registraron los siguientes comportamientos:\n"

        # 🔥 Agrupar por fuente
        picos_agrupados = {}

        for fuente, medio, url, texto in picos:
            if fuente not in picos_agrupados:
                picos_agrupados[fuente] = []
            picos_agrupados[fuente].append((medio, url, texto))

        # 🔥 Imprimir por bloque (como tu reporte)
        for fuente, lista in picos_agrupados.items():

            mensaje_picos += f"<b>{fuente} ↓</b>\n"

            for medio, url, texto in lista:
                mensaje_picos += formato_publicacion(medio, url, texto)

            mensaje_picos += "\n"

        # enviar header
        requests.post(url_api, data={
            "chat_id": CHAT_ID,
            "text": mensaje_header,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        })

        # imagen 1
        if img1:
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
                          data={"chat_id": CHAT_ID},
                          files={"photo": img1})

        # mensaje principal
        requests.post(url_api, data={
            "chat_id": CHAT_ID,
            "text": mensaje,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        })

        # imagen 2
        if img2:
            requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto",
                          data={"chat_id": CHAT_ID},
                          files={"photo": img2})

        # picos
        requests.post(url_api, data={
            "chat_id": CHAT_ID,
            "text": mensaje_picos,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        })

        st.success("Reporte enviado 🚀")

