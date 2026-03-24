import streamlit as st
from builder_view import builder_ui
from pln_view import pln_ui

st.set_page_config(page_title="Reporte PLN", layout="wide")

modo = st.sidebar.selectbox(
    "Selecciona herramienta",
    ["Reporte PLN", "Builder Telegram"]
)

if modo == "Reporte PLN":
    pln_ui()

elif modo == "Builder Telegram":
    builder_ui()
