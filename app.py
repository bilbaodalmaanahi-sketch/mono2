from pathlib import Path
import pandas as pd


# ============================================================
# ARCHIVO BIN
# ============================================================

archivo1 = Path(
    "FIAT 500-ECU MARELLI 8GMF-MOD-123KM.bin"
)

with open(archivo1, "rb") as f:
    datos = f.read()

print("Tamaño:", len(datos), "bytes")


# ============================================================
# VALOR ORIGINAL
# ============================================================

ingrekk = 123

bytes_originales = ingrekk.to_bytes(
    4,
    byteorder="big",
    signed=False
)

print("Valor original:", ingrekk)
print("HEX BIG:", bytes_originales.hex(" ").upper())


# ============================================================
# DATAFRAME
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
    # GUARDAR
    # ========================================================

    registros.append({

        "Direccion":
            f"0x{direccion:04X}",

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


# ============================================================
# DATAFRAME
# ============================================================

df = pd.DataFrame(registros)


# ============================================================
# MOSTRAR
# ============================================================

print()
print("==============================================================")
print("BIG-ENDIAN VS LITTLE-ENDIAN")
print("==============================================================")

print(
    df.to_string(index=False)
)


# ============================================================
# BUSCAR 185971 EN AMBAS REPRESENTACIONES
# ============================================================

resultado = df[
    (df["Decimal_BIG"] == ingrekk) |
    (df["Decimal_LITTLE"] == ingrekk)
]

print()
print("==============================================================")
print("OCURRENCIAS DE 185971")
print("==============================================================")

if not resultado.empty:

    print(
        resultado.to_string(index=False)
    )

else:

    print("No se encontró 185971.")
    
    
    
from pathlib import Path
import pandas as pd
import random


# ============================================================
# ARCHIVO BIN
# ============================================================

archivo1 = Path(
    "FIAT 500-ECU MARELLI 8GMF (185971 KM).bin"
)

with open(archivo1, "rb") as f:
    datos = f.read()

print("Tamaño:", len(datos), "bytes")


# ============================================================
# VALORES
# ============================================================

valor_buscado = 185971

nuevov = 123


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

print()
print("=" * 100)
print("BIG-ENDIAN VS LITTLE-ENDIAN")
print("=" * 100)

print(
    df.to_string(index=False)
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
