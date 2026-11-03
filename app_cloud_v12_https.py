import streamlit as st

pages = [
    st.Page(
        "Inteligencia_Territorial.py",
        title="Inteligencia Territorial",
        icon=":material/public:",
        default=True,
    ),
    st.Page(
        "pages/01_Explorador_Geografico.py",
        title="Explorador Geográfico",
        icon=":material/map:",
    ),
]

navigation = st.navigation(pages)
navigation.run()