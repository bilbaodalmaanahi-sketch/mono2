import streamlit as st
import pandas as pd
import random


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Monky2a BIN Analyzer",
    page_icon="🐒",
    layout="wide"
)


# ============================================================
# ESTILO
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #080808;
    color: #00ff66;
}

html, body, [class*="css"] {
    font-family: "Courier New", monospace;
}

h1 {
    color: #00ff66 !important;
    font-family: "Courier New", monospace !important;
    font-weight: bold;
    letter-spacing: 3px;
    text-transform: uppercase;
}

h2, h3 {
    color: #00ff66 !important;
    font-family: "Courier New", monospace !important;
}

p {
    color: #b0ffcc;
}

input {
    background-color: #111111 !important;
    color: #00ff66 !important;
    border: 1px solid #00ff66 !important;
    font-family: "Courier New", monospace !important;
}

.stButton > button {
    background-color: #001a0a;
    color: #00ff66;
    border: 1px solid #00ff66;
    border-radius: 0px;
    font-family: "Courier New", monospace;
    font-weight: bold;
    letter-spacing: 2px;
}

.stButton > button:hover {
    background-color: #00ff66;
    color: #000000;
}

[data-testid="stMetric"] {
    background-color: #0d0d0d;
    border: 1px solid #00ff66;
    padding: 15px;
}

[data-testid="stMetricLabel"] {
    color: #00ff66 !important;
}

[data-testid="stMetricValue"] {
    color: #ffffff !important;
}

[data-testid="stDataFrame"] {
    border: 1px solid #00ff66;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# TÍTULO
# ============================================================

st.title("🐒 MONKY EEPROM LAB")

st.markdown(
    "### ECU / EEPROM Binary Memory Analyzer"
)

st.caption("Concept by Ariel Calacaterra")

st.write(
    "Busca valores de kilometraje en formato BIG-ENDIAN y "
    "LITTLE-ENDIAN, analiza equivalentes en metros y permite "
    "generar un BIN modificado."
)


# ============================================================
# CARGAR ARCHIVO BIN
# ============================================================

st.subheader("ARCHIVO BIN")

archivo = st.file_uploader(
    "Seleccionar archivo BIN",
    type=["bin"]
)


# ============================================================
# DATOS A BUSCAR / MODIFICAR
# ============================================================

st.subheader("PARÁMETROS")

col1, col2, col3 = st.columns(3)


with col1:

    valor_buscado = st.number_input(
        "Kilometraje a buscar (KM)",
        min_value=0,
        value=None,
        placeholder="Ingrese el KM",
        step=1
    )


with col2:

    nuevov = st.number_input(
        "Nuevo valor (KM)",
        min_value=0,
        value=None,
        placeholder="Ingrese el nuevo KM",
        step=1
    )


with col3:

    margen_metros = st.number_input(
        "Margen de búsqueda (metros)",
        min_value=0,
        value=1_000_000,
        step=1000
    )


# ============================================================
# PROCESAR BIN
# ============================================================

if archivo is not None:

    # --------------------------------------------------------
    # LEER ARCHIVO
    # --------------------------------------------------------

    datos = archivo.read()

    st.success(
        f"Archivo cargado: {archivo.name}"
    )

    st.write(
        f"**Tamaño:** {len(datos):,} bytes"
    )


    # ========================================================
    # VALIDAR DATOS
    # ========================================================

    if valor_buscado is None or nuevov is None:

        st.warning(
            "Ingrese el kilometraje a buscar y el nuevo valor."
        )


    else:

        # ====================================================
        # EQUIVALENTE ORIGINAL EN METROS
        # ====================================================

        valor_metros_objetivo = int(
            valor_buscado * 1000
        )


        # ====================================================
        # MARGEN DE BÚSQUEDA
        # ====================================================

        limite_metros_inicio = (
            valor_metros_objetivo - margen_metros
        )

        limite_metros_fin = (
            valor_metros_objetivo + margen_metros
        )


        # ====================================================
        # INFORMACIÓN
        # ====================================================

        st.subheader("PARÁMETROS DE BÚSQUEDA")


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(
                "KM BUSCADO",
                f"{int(valor_buscado):,}"
            )


        with col2:

            st.metric(
                "EQUIVALENTE EN METROS",
                f"{valor_metros_objetivo:,}"
            )


        with col3:

            st.metric(
                "NUEVO VALOR",
                f"{int(nuevov):,} KM"
            )


        # ====================================================
        # RANGO
        # ====================================================

        st.write(
            f"**Rango de búsqueda:** "
            f"{int(limite_metros_inicio):,} → "
            f"{int(limite_metros_fin):,} metros"
        )


        # ====================================================
        # DATOS INTERNOS
        # ====================================================

        st.write("### DATOS CALCULADOS")


        datos_calculados = pd.DataFrame({
            "Parámetro": [
                "KM buscado",
                "Nuevo KM",
                "KM buscado en metros",
                "Margen",
                "Límite inferior",
                "Límite superior",
                "Tamaño BIN"
            ],

            "Valor": [
                int(valor_buscado),
                int(nuevov),
                valor_metros_objetivo,
                int(margen_metros),
                int(limite_metros_inicio),
                int(limite_metros_fin),
                f"{len(datos):,} bytes"
            ]
        })


        st.dataframe(
            datos_calculados,
            use_container_width=True,
            hide_index=True
        )


        # ====================================================
        # BOTÓN DE BÚSQUEDA
        # ====================================================

        st.markdown("---")


        buscar = st.button(
            "BUSCAR VALORES EN BIN",
            use_container_width=True
        )


        if buscar:

            st.info(
                "Archivo listo para realizar la búsqueda "
                "BIG-ENDIAN / LITTLE-ENDIAN."
            )

            st.write(
                f"Valor buscado: **{int(valor_buscado):,} KM**"
            )

            st.write(
                f"Nuevo valor: **{int(nuevov):,} KM**"
            )

            st.write(
                f"Objetivo en metros: "
                f"**{valor_metros_objetivo:,}**"
            )

            st.write(
                f"Rango: "
                f"**{int(limite_metros_inicio):,}** "
                f"→ "
                f"**{int(limite_metros_fin):,}** metros"
            )


else:

    st.info(
        "Seleccione un archivo BIN para comenzar."
    )



