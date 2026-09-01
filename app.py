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
    "LITTLE-ENDIAN, analiza equivalentes en metros y "
    "genera un BIN modificado."
)


# ============================================================
# ARCHIVO BIN
# ============================================================

st.subheader("ARCHIVO BIN")

archivo = st.file_uploader(
    "Seleccionar archivo BIN",
    type=["bin"]
)


# ============================================================
# PARÁMETROS
# ============================================================

st.subheader("PARÁMETROS DE BÚSQUEDA")

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
# VALIDACIONES
# ============================================================

if archivo is None:

    st.info(
        "Seleccione un archivo BIN para comenzar."
    )

    st.stop()


if valor_buscado is None:

    st.warning(
        "Ingrese el kilometraje que desea buscar."
    )

    st.stop()


if nuevov is None:

    st.warning(
        "Ingrese el nuevo kilometraje."
    )

    st.stop()


# ============================================================
# CONVERTIR A ENTEROS
# ============================================================

valor_buscado = int(valor_buscado)

nuevov = int(nuevov)

margen_metros = int(margen_metros)


# ============================================================
# LEER BIN
# ============================================================

datos = archivo.getvalue()


st.success(
    f"Archivo cargado: {archivo.name}"
)


st.write(
    f"**Tamaño:** {len(datos):,} bytes"
)


# ============================================================
# EQUIVALENTE ORIGINAL EN METROS
# ============================================================

valor_metros_objetivo = (
    valor_buscado * 1000
)


# ============================================================
# RANGO DE BÚSQUEDA
# ============================================================

limite_metros_inicio = (
    valor_metros_objetivo
    - margen_metros
)

limite_metros_fin = (
    valor_metros_objetivo
    + margen_metros
)


# ============================================================
# MÉTRICAS
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "KM BUSCADO",
        f"{valor_buscado:,}"
    )


with col2:

    st.metric(
        "METROS OBJETIVO",
        f"{valor_metros_objetivo:,}"
    )


with col3:

    st.metric(
        "NUEVO KM",
        f"{nuevov:,}"
    )


with col4:

    st.metric(
        "TAMAÑO BIN",
        f"{len(datos):,} B"
    )


st.write(
    f"**Rango de búsqueda:** "
    f"{limite_metros_inicio:,} → "
    f"{limite_metros_fin:,} metros"
)


# ============================================================
# BOTÓN ANALIZAR
# ============================================================

st.markdown("---")

analizar = st.button(
    "ANALIZAR BIN",
    use_container_width=True,
    key="btn_analizar_bin"
)


# ============================================================
# ANÁLISIS
# ============================================================

if analizar:

    # ========================================================
    # DATAFRAME BIG + LITTLE
    # ========================================================

    registros = []


    for direccion in range(
        0,
        len(datos) - 3,
        4
    ):

        bloque = datos[
            direccion:direccion + 4
        ]


        # ----------------------------------------------------
        # BIG-ENDIAN
        # ----------------------------------------------------

        decimal_big = int.from_bytes(
            bloque,
            byteorder="big",
            signed=False
        )


        hex_big = (
            f"{decimal_big:08X}"
        )


        # ----------------------------------------------------
        # LITTLE-ENDIAN
        # ----------------------------------------------------

        decimal_little = int.from_bytes(
            bloque,
            byteorder="little",
            signed=False
        )


        hex_little = (
            f"{decimal_little:08X}"
        )


        # ----------------------------------------------------
        # REGISTRO
        # ----------------------------------------------------

        registros.append({

            "Direccion":
                f"0x{direccion:04X}",

            "Direccion_decimal":
                direccion,

            "Bytes_BIN":
                bloque.hex(" ").upper(),

            "HEX_BIG":
                hex_big,

            "Decimal_BIG":
                decimal_big,

            "HEX_LITTLE":
                hex_little,

            "Decimal_LITTLE":
                decimal_little
        })


    # ========================================================
    # DATAFRAME
    # ========================================================

    df = pd.DataFrame(
        registros
    )


    # ========================================================
    # BUSCAR VALOR EXACTO
    # ========================================================

    resultado = df[
        (df["Decimal_BIG"] == valor_buscado)
        |
        (df["Decimal_LITTLE"] == valor_buscado)
    ].copy()


    # ========================================================
    # RESULTADOS EXACTOS
    # ========================================================

    st.markdown("---")

    st.subheader(
        f"COINCIDENCIAS DE {valor_buscado:,} KM"
    )


    if not resultado.empty:

        st.success(
            f"Coincidencias encontradas: "
            f"{len(resultado)}"
        )


        st.dataframe(
            resultado[
                [
                    "Direccion_decimal",
                    "Direccion",
                    "Bytes_BIN",
                    "HEX_BIG",
                    "Decimal_BIG",
                    "HEX_LITTLE",
                    "Decimal_LITTLE"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )


    else:

        st.warning(
            f"No se encontró "
            f"{valor_buscado:,} KM."
        )


    # ========================================================
    # DATAFRAME DE METROS
    # ========================================================

    filas_metros = []


    for direccion in range(
        0,
        len(datos) - 3,
        4
    ):

        bloque = datos[
            direccion:direccion + 4
        ]


        # ----------------------------------------------------
        # BIG
        # ----------------------------------------------------

        valor_big = int.from_bytes(
            bloque,
            byteorder="big",
            signed=False
        )


        # ----------------------------------------------------
        # LITTLE
        # ----------------------------------------------------

        valor_little = int.from_bytes(
            bloque,
            byteorder="little",
            signed=False
        )


        # ====================================================
        # BUSCAR METROS BIG
        # ====================================================

        if (
            limite_metros_inicio
            <= valor_big
            <= limite_metros_fin
        ):

            filas_metros.append({

                "Direccion_decimal":
                    direccion,

                "Direccion":
                    f"0x{direccion:04X}",

                "Endian":
                    "BIG",

                "Metros":
                    valor_big,

                "HEX":
                    f"{valor_big:08X}",

                "Bytes_BIN":
                    bloque.hex(" ").upper()
            })


        # ====================================================
        # BUSCAR METROS LITTLE
        # ====================================================

        if (
            limite_metros_inicio
            <= valor_little
            <= limite_metros_fin
        ):

            if valor_little != valor_big:

                filas_metros.append({

                    "Direccion_decimal":
                        direccion,

                    "Direccion":
                        f"0x{direccion:04X}",

                    "Endian":
                        "LITTLE",

                    "Metros":
                        valor_little,

                    "HEX":
                        f"{valor_little:08X}",

                    "Bytes_BIN":
                        bloque.hex(" ").upper()
                })


    # ========================================================
    # DATAFRAME METROS
    # ========================================================

    df_metros = pd.DataFrame(
        filas_metros
    )


    # ========================================================
    # MOSTRAR METROS
    # ========================================================

    st.markdown("---")

    st.subheader(
        "VALORES ENCONTRADOS EN METROS"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "OBJETIVO",
            f"{valor_metros_objetivo:,}"
        )


    with col2:

        st.metric(
            "MARGEN",
            f"±{margen_metros:,}"
        )


    with col3:

        st.metric(
            "COINCIDENCIAS",
            f"{len(df_metros)}"
        )


    if not df_metros.empty:

        st.dataframe(
            df_metros,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.warning(
            "No se encontraron valores "
            "en el rango de metros."
        )


    # ========================================================
    # DATAFRAME COMPLETO
    # ========================================================

    with st.expander(
        "MOSTRAR ANÁLISIS COMPLETO"
    ):

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )


    # ============================================================
# GENERAR BIN MODIFICADO
# ============================================================

st.markdown("---")

st.subheader(
    "GENERAR BIN MODIFICADO"
)


# ============================================================
# ESTADO DE STREAMLIT
# ============================================================

if "bin_generado" not in st.session_state:
    st.session_state.bin_generado = False

if "datos_modificados" not in st.session_state:
    st.session_state.datos_modificados = None

if "nombre_salida" not in st.session_state:
    st.session_state.nombre_salida = None


# ============================================================
# BOTÓN GENERAR
# ============================================================

generar_bin = st.button(
    "GENERAR BIN MODIFICADO",
    use_container_width=True,
    key="btn_generar_bin_modificado"
)


# ============================================================
# GENERAR
# ============================================================

if generar_bin:

    # ========================================================
    # COPIA DEL BIN ORIGINAL
    # ========================================================

    datos_modificados = bytearray(datos)

    cambios_km = 0
    cambios_metros = 0


    # ========================================================
    # CAMBIAR VALORES DE KM
    # ========================================================

    for _, fila in resultado.iterrows():

        direccion = int(
            fila["Direccion_decimal"]
        )


        # ----------------------------------------------------
        # BIG-ENDIAN
        # ----------------------------------------------------

        if fila["Decimal_BIG"] == valor_buscado:

            datos_modificados[
                direccion:direccion + 4
            ] = int(nuevov).to_bytes(
                4,
                byteorder="big",
                signed=False
            )

            cambios_km += 1


            st.write(
                f"KM BIG | "
                f"0x{direccion:04X} | "
                f"{valor_buscado:,} → "
                f"{nuevov:,}"
            )


        # ----------------------------------------------------
        # LITTLE-ENDIAN
        # ----------------------------------------------------

        elif fila["Decimal_LITTLE"] == valor_buscado:

            datos_modificados[
                direccion:direccion + 4
            ] = int(nuevov).to_bytes(
                4,
                byteorder="little",
                signed=False
            )

            cambios_km += 1


            st.write(
                f"KM LITTLE | "
                f"0x{direccion:04X} | "
                f"{valor_buscado:,} → "
                f"{nuevov:,}"
            )


    # ========================================================
    # GENERAR NUEVOS VALORES DE METROS
    # ========================================================

    if not df_metros.empty:

        df_metros_nuevo = df_metros.copy()

        df_metros_nuevo["Metros_Nuevo"] = (
            df_metros_nuevo["Metros"].apply(
                lambda x:
                nuevov * 1000
                + random.randint(0, 999)
            )
        )

    else:

        df_metros_nuevo = pd.DataFrame()


    # ========================================================
    # MOSTRAR NUEVOS VALORES
    # ========================================================

    st.markdown("---")

    st.subheader(
        "NUEVOS VALORES EN METROS"
    )


    if not df_metros_nuevo.empty:

        st.dataframe(
            df_metros_nuevo[
                [
                    "Direccion_decimal",
                    "Direccion",
                    "Endian",
                    "Metros",
                    "Metros_Nuevo",
                    "HEX",
                    "Bytes_BIN"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )


    # ========================================================
    # ESCRIBIR NUEVOS VALORES DE METROS
    # ========================================================

    for _, fila in df_metros_nuevo.iterrows():

        direccion = int(
            fila["Direccion_decimal"]
        )

        nuevo_metros = int(
            fila["Metros_Nuevo"]
        )

        endian = fila["Endian"]


        # ----------------------------------------------------
        # VALIDAR QUE ENTRE EN 32 BITS
        # ----------------------------------------------------

        if nuevo_metros > 0xFFFFFFFF:

            st.error(
                f"El valor {nuevo_metros:,} "
                f"no puede almacenarse en 32 bits."
            )

            st.stop()


        # ----------------------------------------------------
        # BIG-ENDIAN
        # ----------------------------------------------------

        if endian == "BIG":

            datos_modificados[
                direccion:direccion + 4
            ] = nuevo_metros.to_bytes(
                4,
                byteorder="big",
                signed=False
            )

            cambios_metros += 1


        # ----------------------------------------------------
        # LITTLE-ENDIAN
        # ----------------------------------------------------

        elif endian == "LITTLE":

            datos_modificados[
                direccion:direccion + 4
            ] = nuevo_metros.to_bytes(
                4,
                byteorder="little",
                signed=False
            )

            cambios_metros += 1


    # ========================================================
    # NOMBRE DEL ARCHIVO
    # ========================================================

    nombre_original = archivo.name


    if nombre_original.lower().endswith(".bin"):

        nombre_salida = (
            nombre_original[:-4]
            + "-MODIFICADO-"
            + str(nuevov)
            + "KM.bin"
        )

    else:

        nombre_salida = (
            nombre_original
            + "-MODIFICADO-"
            + str(nuevov)
            + "KM.bin"
        )


    # ========================================================
    # GUARDAR EN SESSION STATE
    # ========================================================

    st.session_state.datos_modificados = bytes(
        datos_modificados
    )

    st.session_state.nombre_salida = (
        nombre_salida
    )

    st.session_state.bin_generado = True


    # ========================================================
    # RESUMEN
    # ========================================================

    st.markdown("---")

    st.subheader(
        "RESULTADO FINAL"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "VALORES KM MODIFICADOS",
            cambios_km
        )


    with col2:

        st.metric(
            "VALORES METROS MODIFICADOS",
            cambios_metros
        )


    with col3:

        st.metric(
            "TOTAL POSICIONES",
            cambios_km + cambios_metros
        )


# ============================================================
# DESCARGA
# ============================================================

if st.session_state.bin_generado:

    st.markdown("---")

    st.success(
        f"BIN modificado generado: "
        f"{st.session_state.nombre_salida}"
    )


    st.download_button(
        label="DESCARGAR BIN MODIFICADO",
        data=st.session_state.datos_modificados,
        file_name=st.session_state.nombre_salida,
        mime="application/octet-stream",
        use_container_width=True,
        key="download_bin_modificado"
    )

