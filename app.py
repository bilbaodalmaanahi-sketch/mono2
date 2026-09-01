import streamlit as st
from pathlib import Path
import struct
import pandas as pd
import random


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="Monky2a BIN Analyzer",
    page_icon="",
    layout="wide"
)

# ============================================================
# ESTILO UNDERGROUND
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
    "Busca un valor exacto, realiza un barrido de las "
    "tres últimas cifras y busca equivalentes en metros "
    "dentro de todo el archivo BIN."
)


# ============================================================
# ARCHIVO BIN
# ============================================================

archivo1 = st.file_uploader(
    "Cargar archivo BIN",
    type=["bin"]
)

if archivo1 is None:
    st.info("Seleccione un archivo BIN para comenzar.")
    st.stop()


# Leer BIN cargado por el usuario
datos = archivo1.read()

print("Tamaño:", len(datos), "bytes")


# ============================================================
# VALORES
# ============================================================

valor_buscado = st.number_input(
    "Valor a buscar",
    min_value=0,
    value=,
    step=1
)

nuevov = st.number_input(
    "Nuevo valor",
    min_value=0,
    value=,
    step=1
)


# ============================================================
# EQUIVALENTE ORIGINAL EN METROS
# ============================================================

valor_metros_objetivo = valor_buscado * 1000


# Margen de búsqueda
margen_metros = 1_000_000


limite_metros_inicio = (
    valor_metros_objetivo - margen_metros
)

limite_metros_fin = (
    valor_metros_objetivo + margen_metros
)


# ============================================================
# DATAFRAME BIG + LITTLE
# ============================================================

registros = []

for direccion in range(0, len(datos) - 3, 4):

    bloque = datos[direccion:direccion + 4]


    # ========================================================
    # BIG-ENDIAN
    # ========================================================

    decimal_big = int.from_bytes(
        bloque,
        byteorder="big",
        signed=False
    )

    hex_big = f"{decimal_big:08X}"


    # ========================================================
    # LITTLE-ENDIAN
    # ========================================================

    decimal_little = int.from_bytes(
        bloque,
        byteorder="little",
        signed=False
    )

    hex_little = f"{decimal_little:08X}"


    # ========================================================
    # DATAFRAME
    # ========================================================

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


df = pd.DataFrame(registros)


# ============================================================
# MOSTRAR DATAFRAME
# ============================================================

# ============================================================
# MOSTRAR DATAFRAME
# ============================================================

st.divider()

st.subheader("BIG-ENDIAN VS LITTLE-ENDIAN")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# ============================================================
# BUSCAR VALOR EN BIG O LITTLE
# ============================================================

resultado = df[
    (df["Decimal_BIG"] == valor_buscado) |
    (df["Decimal_LITTLE"] == valor_buscado)
].copy()


print()
print("=" * 100)
print(f"COINCIDENCIAS DE {valor_buscado}")
print("=" * 100)


if not resultado.empty:

    print(
        resultado[[
            "Direccion_decimal",
            "Direccion",
            "Bytes_BIN",
            "HEX_BIG",
            "Decimal_BIG",
            "HEX_LITTLE",
            "Decimal_LITTLE"
        ]].to_string(index=False)
    )

else:

    print(
        f"No se encontró {valor_buscado}."
    )


print()
print(
    f"Coincidencias encontradas: {len(resultado)}"
)


# ============================================================
# CREAR DATAFRAME DE METROS
# ============================================================

filas_metros = []


for direccion in range(0, len(datos) - 3, 4):

    bloque = datos[direccion:direccion + 4]


    # ========================================================
    # INTERPRETACIÓN BIG
    # ========================================================

    valor_big = int.from_bytes(
        bloque,
        byteorder="big",
        signed=False
    )


    # ========================================================
    # INTERPRETACIÓN LITTLE
    # ========================================================

    valor_little = int.from_bytes(
        bloque,
        byteorder="little",
        signed=False
    )


    # ========================================================
    # BUSCAR METROS EN BIG
    # ========================================================

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


    # ========================================================
    # BUSCAR METROS EN LITTLE
    # ========================================================

    # Evitamos duplicar una misma posición cuando
    # ambos valores fueran iguales.

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


# ============================================================
# DATAFRAME METROS
# ============================================================

df_metros = pd.DataFrame(
    filas_metros
)


# ============================================================
# MOSTRAR DATAFRAME METROS
# ============================================================

print()
print("=" * 100)
print("DATAFRAME DE VALORES EN METROS")
print("=" * 100)

print(
    f"Valor buscado       : {valor_buscado:,}"
)

print(
    f"Equivalente metros  : {valor_metros_objetivo:,}"
)

print(
    f"Margen              : ±{margen_metros:,}"
)

print(
    f"Rango               : "
    f"{limite_metros_inicio:,} → "
    f"{limite_metros_fin:,}"
)

print(
    f"Coincidencias       : {len(df_metros)}"
)

print()


if not df_metros.empty:

    print(
        df_metros.to_string(index=False)
    )

else:

    print(
        "No se encontraron valores en el rango."
    )


# ============================================================
# CAMBIAR LOS VALORES DE KM
# ============================================================

datos_modificados = bytearray(datos)


for _, fila in resultado.iterrows():

    direccion = int(
        fila["Direccion_decimal"]
    )

    endian = fila["Endian"] if "Endian" in fila else None


    # --------------------------------------------------------
    # Determinar dónde estaba el valor
    # --------------------------------------------------------

    fila_original = df[
        df["Direccion_decimal"] == direccion
    ].iloc[0]


    if fila_original["Decimal_BIG"] == valor_buscado:

        # BIG-ENDIAN

        datos_modificados[
            direccion:direccion + 4
        ] = int(nuevov).to_bytes(
            4,
            byteorder="big",
            signed=False
        )

        print(
            f"KM BIG  | 0x{direccion:04X} | "
            f"{valor_buscado} → {nuevov}"
        )


    elif fila_original["Decimal_LITTLE"] == valor_buscado:

        # LITTLE-ENDIAN

        datos_modificados[
            direccion:direccion + 4
        ] = int(nuevov).to_bytes(
            4,
            byteorder="little",
            signed=False
        )

        print(
            f"KM LITTLE | 0x{direccion:04X} | "
            f"{valor_buscado} → {nuevov}"
        )


# ============================================================
# GENERAR NUEVOS VALORES DE METROS
# ============================================================

if not df_metros.empty:

    df_metros["Metros_Nuevo"] = df_metros[
        "Metros"
    ].apply(
        lambda x:
            nuevov * 1000
            + random.randint(0, 999)
    )


# ============================================================
# MOSTRAR NUEVOS VALORES
# ============================================================

print()
print("=" * 100)
print("NUEVOS VALORES EN METROS")
print("=" * 100)


if not df_metros.empty:

    print(
        df_metros[[
            "Direccion_decimal",
            "Direccion",
            "Endian",
            "Metros",
            "Metros_Nuevo",
            "HEX",
            "Bytes_BIN"
        ]].to_string(index=False)
    )


# ============================================================
# ESCRIBIR NUEVOS VALORES DE METROS
# ============================================================

for _, fila in df_metros.iterrows():

    direccion = int(
        fila["Direccion_decimal"]
    )

    nuevo_metros = int(
        fila["Metros_Nuevo"]
    )

    endian = fila["Endian"]


    # --------------------------------------------------------
    # BIG-ENDIAN
    # --------------------------------------------------------

    if endian == "BIG":

        datos_modificados[
            direccion:direccion + 4
        ] = nuevo_metros.to_bytes(
            4,
            byteorder="big",
            signed=False
        )


    # --------------------------------------------------------
    # LITTLE-ENDIAN
    # --------------------------------------------------------

    elif endian == "LITTLE":

        datos_modificados[
            direccion:direccion + 4
        ] = nuevo_metros.to_bytes(
            4,
            byteorder="little",
            signed=False
        )


# ============================================================
# GUARDAR BIN MODIFICADO
# ============================================================

archivo_salida = Path(
    "FIAT 500-ECU MARELLI 8GMF-MOD-123KM.bin"
)


with open(archivo_salida, "wb") as f:

    f.write(datos_modificados)


# ============================================================
# RESULTADO FINAL
# ============================================================

print()
print("=" * 100)
print("BIN MODIFICADO GUARDADO")
print("=" * 100)

print(
    f"Archivo: {archivo_salida}"
)

print(
    f"Valores KM modificados: "
    f"{len(resultado)}"
)

print(
    f"Valores metros modificados: "
    f"{len(df_metros)}"
)

print(
    f"Total posiciones modificadas: "
    f"{len(resultado) + len(df_metros)}"
)

print("=" * 100)    
    
