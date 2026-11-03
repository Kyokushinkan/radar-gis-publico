from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Radar GIS V1.2 - Mapas OSM",
    layout="wide"
)

st.title("Radar GIS V1.2")
st.subheader("Inteligencia territorial - OpenStreetMap")

options = {
    "Todos": "todos.html",
    "Perú": "peru.html",
    "Brasil": "brasil.html",
    "Chile": "chile.html",
}

selected = st.selectbox(
    "Seleccionar cobertura geográfica",
    list(options.keys())
)

base = Path(__file__).resolve().parent.parent
map_path = base / "mapas_osm" / options[selected]

if not map_path.is_file():
    st.error("Mapa no encontrado")
    st.stop()

html = map_path.read_text(encoding="utf-8")

components.html(
    html,
    height=750,
    scrolling=True
)

st.caption(
    "GIS V1.2 - Validación local. "
    "Sin publicación Cloudflare."
)