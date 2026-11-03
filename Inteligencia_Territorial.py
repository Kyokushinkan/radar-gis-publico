"""Radar GIS V1.1: interfaz multisectorial aislada."""
from pathlib import Path
import html
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium


def _gis_v12_render_osm(country):
    from pathlib import Path
    import streamlit as st
    import streamlit.components.v1 as components

    aliases = {
        "Todos": "todos",
        "Perú": "peru",
        "Peru": "peru",
        "Brasil": "brasil",
        "Chile": "chile",
        "todos": "todos",
        "peru": "peru",
        "brasil": "brasil",
        "chile": "chile",
    }

    key = aliases.get(str(country))

    if key is None:
        st.error("Cobertura geografica no reconocida")
        return

    path = (
        Path(__file__).resolve().parent
        / "mapas_osm"
        / (key + ".html")
    )

    if not path.is_file():
        st.error("Mapa OSM no encontrado")
        return

    components.html(
        path.read_text(encoding="utf-8"),
        height=750,
        scrolling=True
    )


ROOT = Path(__file__).resolve().parent
DEMO = ROOT / "data" / "demo" / "puntos.csv"
MODULES = {
    "Inmobiliario": "Propiedades, Tokko, eXp y REMAJU",
    "Airbnb": "Oferta, ocupación, tarifas y competencia",
    "Estado Perú": "Entidades públicas y funcionarios",
    "Estado Brasil": "Órgãos federais, estaduais, prefeituras e servidores públicos",
    "Contrataciones Perú": "PLADICOP, SIE y Perú Compras",
    "Contrataciones Brasil": "Siga Pregão y entidades brasileñas",
    "Importaciones": "Productos, importadores, aduanas y puertos",
    "Exportaciones": "Productos, exportadores, destinos y puertos",
    "Autos y subastas": "Vehículos, depósitos y remates",
    "Logística": "Rutas, almacenes y corredores",
    "Centro de Datos": "Fuentes, integridad y próximas conexiones",
}

st.set_page_config(page_title="Radar GIS V1.2", layout="wide")
st.title("Radar GIS — Inteligencia Territorial V1.2")
st.caption("Plataforma independiente · Perú y Brasil · Fuentes originales protegidas")

COUNTRIES_BY_MODULE = {
    "Estado Perú": ["Perú"],
    "Estado Brasil": ["Brasil"],
    "Contrataciones Perú": ["Perú"],
    "Contrataciones Brasil": ["Brasil"],
}

with st.sidebar:
    st.header("Explorar")
    module = st.selectbox("Módulo", list(MODULES))

    allowed_countries = COUNTRIES_BY_MODULE.get(
        module, ["Todos", "Perú", "Brasil", "Chile"]
    )

    if len(allowed_countries) == 1:
        country = allowed_countries[0]
        st.selectbox(
            "País",
            allowed_countries,
            disabled=True,
            key="fixed_country"
        )
    else:
        country = st.selectbox(
            "País",
            allowed_countries,
            key="selected_country"
        )

    st.caption("Sin conexión a los radares originales")

st.subheader(module)
st.write(MODULES[module])


if module == "Inmobiliario":
    st.subheader("Mapa territorial de Peru, Brasil y Chile")

    if country == "Brasil":
        st.info(
            "Cartografia IBGE: 27 unidades federativas. "
            "Sin datos inmobiliarios brasile?os conectados."
        )
    elif country == "Chile":
        st.info(
            "Cartografia de Chile: 16 regiones. "
            "Sin datos inmobiliarios chilenos conectados."
        )
    else:
        st.warning(
            "Los registros Tokko corresponden exclusivamente a Peru "
            "y no representan necesariamente propiedades activas."
        )

    import os

    import os
    from urllib.parse import urlsplit

    public_base = os.environ.get(
        "GIS_V12_PUBLIC_BASE_URL", ""
    ).strip().rstrip("/")

    parsed = urlsplit(public_base)


    map_routes = {
        "Todos": "/mapas/todos",
        "Per?": "/mapas/peru",
        "Brasil": "/mapas/brasil",
        "Chile": "/mapas/chile",
    }

    _gis_v12_render_osm(country)

    if country in ("Todos", "Perú"):
        datos_path = (
            ROOT / "data/procesados/"
            "tokko_concentracion_distrital_v1.csv"
        )
        df = pd.read_csv(datos_path, dtype={"ubigeo": str})

        if (
            len(df) != 246
            or df["ubigeo"].duplicated().any()
            or int(df["cantidad_registros"].sum()) != 9233
        ):
            st.error("Los datos Tokko no superan la validación.")
            st.stop()

        col1, col2 = st.columns(2)
        col1.metric("Distritos de Perú", len(df))
        col2.metric(
            "Registros Tokko Perú",
            int(df["cantidad_registros"].sum())
        )

        st.dataframe(
            df.sort_values(
                "cantidad_registros",
                ascending=False
            ),
            hide_index=True,
            width="stretch"
        )

else:
    st.info("Pendiente de integración. No hay datos reales conectados en este módulo.")
    if module == "Centro de Datos":
        st.write("Los conectores futuros leerán copias validadas, sin escribir en las fuentes originales.")
