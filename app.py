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
# CARGAR ARCHIVO
# ============================================================

st.divider()

st.subheader("ARCHIVO BIN")

archivo1 = st.file_uploader(
    "Cargar archivo BIN",
    type=["bin"]
)

if archivo1 is None:

    st.info("Seleccione un archivo BIN para comenzar.")

    st.stop()


# Leer archivo
datos = archivo1.getvalue()


# ============================================================
# INFORMACIÓN DEL ARCHIVO
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "ARCHIVO",
        archivo1.name
    )

with col2:
    st.metric(
        "TAMAÑO",
        f"{len(datos):,} bytes"
    )

with col3:
    st.metric(
        "PALABRAS 32-BIT",
        f"{len(datos) // 4:,}"
    )


# ============================================================
# PARÁMETROS
# ============================================================

st.divider()

st.subheader("PARÁMETROS DE BÚSQUEDA")


col1, col2, col3 = st.columns(3)


with col1:

    valor_buscado = st.number_input(
        "Kilometraje a buscar",
        min_value=0,
        value=0,
        step=1
    )


with col2:

    nuevov = st.number_input(
        "Nuevo kilometraje",
        min_value=0,
        value=0,
        step=1
    )


with col3:

    margen_metros = st.number_input(
        "Margen en metros",
        min_value=0,
        value=1_000_000,
        step=1000
    )


# ============================================================
# BOTÓN BUSCAR
# ============================================================

buscar = st.button(
    "BUSCAR EN BIN",
    use_container_width=True
)


if not buscar:

    st.info(
        "Ingrese el kilometraje y presione "
        "**BUSCAR EN BIN**."
    )

    st.stop()


# ============================================================
# VALIDACIÓN
# ============================================================

if valor_buscado <= 0:

    st.warning(
        "Ingrese un kilometraje mayor que cero."
    )

    st.stop()


if nuevov <= 0:

    st.warning(
        "Ingrese un nuevo kilometraje mayor que cero."
    )

    st.stop()


# ============================================================
# DATAFRAME BIG + LITTLE
# ============================================================

registros = []


for direccion in range(0, len(datos) - 3, 4):

    bloque = datos[direccion:direccion + 4]


    # --------------------------------------------------------
    # BIG-ENDIAN
    # --------------------------------------------------------

    decimal_big = int.from_bytes(
        bloque,
        byteorder="big",
        signed=False
    )

    hex_big = f"{decimal_big:08X}"


    # --------------------------------------------------------
    # LITTLE-ENDIAN
    # --------------------------------------------------------

    decimal_little = int.from_bytes(
        bloque,
        byteorder="little",
        signed=False
    )

    hex_little = f"{decimal_little:08X}"


    registros.append({

        "Direccion": f"0x{direccion:04X}",

        "Direccion_decimal": direccion,

        "Bytes_BIN": bloque.hex(" ").upper(),

        "HEX_BIG": hex_big,

        "Decimal_BIG": decimal_big,

        "HEX_LITTLE": hex_little,

        "Decimal_LITTLE": decimal_little

    })


df = pd.DataFrame(registros)


# ============================================================
# RESULTADOS DEL VALOR BUSCADO
# ============================================================

resultado = df[
    (df["Decimal_BIG"] == valor_buscado) |
    (df["Decimal_LITTLE"] == valor_buscado)
].copy()


# ============================================================
# AGREGAR ENDIAN
# ============================================================

if not resultado.empty:

    endians = []

    for _, fila in resultado.iterrows():

        if fila["Decimal_BIG"] == valor_buscado:

            endian = "BIG"

        else:

            endian = "LITTLE"

        endians.append(endian)

    resultado["Endian"] = endians


# ============================================================
# CABECERA RESULTADOS
# ============================================================

st.divider()

st.subheader(
    f"RESULTADOS PARA {valor_buscado:,} KM"
)


# ============================================================
# MÉTRICAS
# ============================================================

c1, c2, c3 = st.columns(3)


with c1:

    st.metric(
        "VALOR BUSCADO",
        f"{valor_buscado:,} km"
    )


with c2:

    st.metric(
        "COINCIDENCIAS",
        len(resultado)
    )


with c3:

    st.metric(
        "NUEVO VALOR",
        f"{nuevov:,} km"
    )


# ============================================================
# MOSTRAR RESULTADOS
# ============================================================

if resultado.empty:

    st.warning(
        f"No se encontró el valor {valor_buscado:,} "
        "en BIG-ENDIAN ni LITTLE-ENDIAN."
    )

else:

    st.success(
        f"Se encontraron {len(resultado)} coincidencia(s)."
    )

    st.dataframe(
        resultado[
            [
                "Direccion",
                "Direccion_decimal",
                "Endian",
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


# ============================================================
# EQUIVALENTE EN METROS
# ============================================================

st.divider()

st.subheader("BÚSQUEDA DE EQUIVALENTES EN METROS")


valor_metros_objetivo = valor_buscado * 1000


limite_metros_inicio = (
    valor_metros_objetivo - margen_metros
)


limite_metros_fin = (
    valor_metros_objetivo + margen_metros
)


c1, c2, c3 = st.columns(3)


with c1:

    st.metric(
        "OBJETIVO",
        f"{valor_metros_objetivo:,} m"
    )


with c2:

    st.metric(
        "INICIO",
        f"{limite_metros_inicio:,} m"
    )


with c3:

    st.metric(
        "FIN",
        f"{limite_metros_fin:,} m"
    )


# ============================================================
# BUSCAR METROS
# ============================================================

filas_metros = []


for direccion in range(0, len(datos) - 3, 4):

    bloque = datos[direccion:direccion + 4]


    # --------------------------------------------------------
    # BIG
    # --------------------------------------------------------

    valor_big = int.from_bytes(
        bloque,
        byteorder="big",
        signed=False
    )


    # --------------------------------------------------------
    # LITTLE
    # --------------------------------------------------------

    valor_little = int.from_bytes(
        bloque,
        byteorder="little",
        signed=False
    )


    # --------------------------------------------------------
    # BIG-ENDIAN
    # --------------------------------------------------------

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

            "Kilometros":
                valor_big / 1000,

            "HEX":
                f"{valor_big:08X}",

            "Bytes_BIN":
                bloque.hex(" ").upper()

        })


    # --------------------------------------------------------
    # LITTLE-ENDIAN
    # --------------------------------------------------------

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

                "Kilometros":
                    valor_little / 1000,

                "HEX":
                    f"{valor_little:08X}",

                "Bytes_BIN":
                    bloque.hex(" ").upper()

            })


# ============================================================
# DATAFRAME METROS
# ============================================================

df_metros = pd.DataFrame(
    filas_metros
)


# ============================================================
# MOSTRAR METROS
# ============================================================

if df_metros.empty:

    st.warning(
        "No se encontraron valores dentro del "
        "rango de metros especificado."
    )

else:

    st.success(
        f"Se encontraron {len(df_metros)} "
        "valores dentro del rango."
    )

    st.dataframe(
        df_metros[
            [
                "Direccion",
                "Direccion_decimal",
                "Endian",
                "Metros",
                "Kilometros",
                "HEX",
                "Bytes_BIN"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# MODIFICAR BIN
# ============================================================

st.divider()

st.subheader("MODIFICAR KILOMETRAJE")


if resultado.empty:

    st.info(
        "No hay coincidencias para modificar."
    )

else:

    st.write(
        f"Se reemplazará **{valor_buscado:,}** "
        f"por **{nuevov:,}** en las posiciones encontradas."
    )


    modificar = st.button(
        "GENERAR BIN MODIFICADO",
        use_container_width=True
    )


    if modificar:

        datos_modificados = bytearray(datos)

        cambios = []


        for _, fila in resultado.iterrows():

            direccion = int(
                fila["Direccion_decimal"]
            )

            endian = fila["Endian"]


            # ------------------------------------------------
            # BIG-ENDIAN
            # ------------------------------------------------

            if endian == "BIG":

                datos_modificados[
                    direccion:direccion + 4
                ] = int(nuevov).to_bytes(
                    4,
                    byteorder="big",
                    signed=False
                )


            # ------------------------------------------------
            # LITTLE-ENDIAN
            # ------------------------------------------------

            elif endian == "LITTLE":

                datos_modificados[
                    direccion:direccion + 4
                ] = int(nuevov).to_bytes(
                    4,
                    byteorder="little",
                    signed=False
                )


            cambios.append({

                "Direccion":
                    f"0x{direccion:04X}",

                "Endian":
                    endian,

                "Anterior":
                    valor_buscado,

                "Nuevo":
                    nuevov

            })


        # ====================================================
        # RESULTADO DE MODIFICACIÓN
        # ====================================================

        st.success(
            f"BIN modificado correctamente. "
            f"Se realizaron {len(cambios)} cambio(s)."
        )


        df_cambios = pd.DataFrame(cambios)


        st.dataframe(
            df_cambios,
            use_container_width=True,
            hide_index=True
        )


        
# ============================================================
# GENERAR NUEVOS VALORES DE METROS
# ============================================================

if not df_metros.empty:

    df_metros["Metros_Nuevo"] = df_metros[
        "Metros"
    ].apply(
        lambda x:
            int(nuevov) * 1000
            + random.randint(0, 999)
    )


# ============================================================
# MOSTRAR NUEVOS VALORES DE METROS
# ============================================================

st.divider()

st.subheader("NUEVOS VALORES EN METROS")


if not df_metros.empty:

    st.dataframe(
        df_metros[
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

else:

    st.info(
        "No existen valores en metros para modificar."
    )


# ============================================================
# BOTÓN PARA GENERAR BIN COMPLETO
# ============================================================

st.divider()

st.subheader("GENERAR BIN MODIFICADO")


if resultado.empty and df_metros.empty:

    st.warning(
        "No hay valores para modificar."
    )

else:

    st.write(
        "El archivo será generado utilizando:"
    )

    st.write(
        f"- KM encontrados: **{len(resultado)}**"
    )

    st.write(
        f"- Valores en metros: **{len(df_metros)}**"
    )

    st.write(
        f"- KM original: **{valor_buscado:,}**"
    )

    st.write(
        f"- KM nuevo: **{nuevov:,}**"
    )


    generar_bin = st.button(
        "GENERAR BIN MODIFICADO",
        use_container_width=True
    )


    if generar_bin:

        # ====================================================
        # COPIA DEL BIN ORIGINAL
        # ====================================================

        datos_modificados = bytearray(datos)


        # ====================================================
        # MODIFICAR VALORES DE KM
        # ====================================================

        cambios_km = 0


        for _, fila in resultado.iterrows():

            direccion = int(
                fila["Direccion_decimal"]
            )

            endian = fila["Endian"]


            # ------------------------------------------------
            # BIG-ENDIAN
            # ------------------------------------------------

            if endian == "BIG":

                datos_modificados[
                    direccion:direccion + 4
                ] = int(nuevov).to_bytes(
                    4,
                    byteorder="big",
                    signed=False
                )


            # ------------------------------------------------
            # LITTLE-ENDIAN
            # ------------------------------------------------

            elif endian == "LITTLE":

                datos_modificados[
                    direccion:direccion + 4
                ] = int(nuevov).to_bytes(
                    4,
                    byteorder="little",
                    signed=False
                )


            cambios_km += 1


        # ====================================================
        # MODIFICAR VALORES DE METROS
        # ====================================================

        cambios_metros = 0


        for _, fila in df_metros.iterrows():

            direccion = int(
                fila["Direccion_decimal"]
            )

            nuevo_metros = int(
                fila["Metros_Nuevo"]
            )

            endian = fila["Endian"]


            # ------------------------------------------------
            # BIG-ENDIAN
            # ------------------------------------------------

            if endian == "BIG":

                datos_modificados[
                    direccion:direccion + 4
                ] = nuevo_metros.to_bytes(
                    4,
                    byteorder="big",
                    signed=False
                )


            # ------------------------------------------------
            # LITTLE-ENDIAN
            # ------------------------------------------------

            elif endian == "LITTLE":

                datos_modificados[
                    direccion:direccion + 4
                ] = nuevo_metros.to_bytes(
                    4,
                    byteorder="little",
                    signed=False
                )


            cambios_metros += 1


        # ====================================================
        # NOMBRE DEL ARCHIVO
        # ====================================================

        nombre_original = archivo1.name


        if nombre_original.lower().endswith(".bin"):

            nombre_salida = (
                nombre_original[:-4]
                + "_MOD.bin"
            )

        else:

            nombre_salida = (
                nombre_original
                + "_MOD.bin"
            )


        # ====================================================
        # RESULTADO FINAL
        # ====================================================

        st.success(
            "BIN MODIFICADO GENERADO CORRECTAMENTE"
        )


        # ====================================================
        # MÉTRICAS
        # ====================================================

        col1, col2, col3, col4 = st.columns(4)


        with col1:

            st.metric(
                "KM MODIFICADOS",
                cambios_km
            )


        with col2:

            st.metric(
                "METROS MODIFICADOS",
                cambios_metros
            )


        with col3:

            st.metric(
                "TOTAL POSICIONES",
                cambios_km + cambios_metros
            )


        with col4:

            st.metric(
                "TAMAÑO BIN",
                f"{len(datos_modificados):,} B"
            )


        # ====================================================
        # INFORMACIÓN
        # ====================================================

        st.write(
            f"**Archivo generado:** `{nombre_salida}`"
        )


        st.write(
            f"**KM:** {valor_buscado:,} → {nuevov:,}"
        )


        st.write(
            f"**Metros nuevos:** "
            f"{nuevov * 1000:,} + últimos 3 dígitos aleatorios"
        )


        # ====================================================
        # DESCARGA
        # ====================================================

        st.download_button(

            label="DESCARGAR BIN MODIFICADO",

            data=bytes(datos_modificados),

            file_name=nombre_salida,

            mime="application/octet-stream",

            use_container_width=True

        )
