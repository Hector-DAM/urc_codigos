from itertools import product
import pandas as pd
import numpy as np
import random as rd
from datetime import datetime, timedelta

def generate_curp(nombre, apellido_paterno, apellido_materno, fecha_nacimiento, genero, lugar_nacimiento):
    # Placeholder for place of birth (you may need a more accurate method)
    lugar_nacimiento = "DF" if lugar_nacimiento is None else lugar_nacimiento

    # Extract components from the birthdate
    year = fecha_nacimiento.year % 100
    month = fecha_nacimiento.month
    day = fecha_nacimiento.day

    # Generate the first part of the CURP
    curp_first_part = (
        apellido_paterno[:2].upper() +
        apellido_materno[0].upper() +
        nombre[0].upper() +
        f"{year:02d}{month:02d}{day:02d}" +
        genero.upper() +
        lugar_nacimiento.upper()
    )

    # Generate the second part of the CURP using a specific rule
    # (you may need to adjust this rule based on official guidelines)
    consonants = ''.join(filter(str.isalpha, curp_first_part))  # Extract consonants
    curp_second_part = (
        consonants[:2] +
        str(rd.randint(10, 99)) +  # Random two-digit number
        rd.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")  # Random letter
    )

    return curp_first_part + curp_second_part

df_base = pd.read_csv("bd_402.csv")

df_hombre = df_base[df_base["genero"] == "Hombre"]
df_mujer = df_base[df_base["genero"] == "Mujer"]

combinaciones_hombre = list(product(df_hombre["nombre1"], df_hombre["nombre2"], df_hombre["apellido1"], df_hombre["apellido2"]))
combinaciones_hombre = list(set(combinaciones_hombre))  # Remove duplicates

combinaciones_mujer = list(product(df_mujer["nombre1"], df_mujer["nombre2"], df_mujer["apellido1"], df_mujer["apellido2"]))
combinaciones_mujer = list(set(combinaciones_mujer))  # Remove duplicates

# Create DataFrames for each gender"s combinations
df_combinaciones_hombre = pd.DataFrame(combinaciones_hombre, columns=["nombre1", "nombre2", "apellido1", "apellido2"])
df_combinaciones_mujer = pd.DataFrame(combinaciones_mujer, columns=["nombre1", "nombre2", "apellido1", "apellido2"])

# Add the GENDER column back to each combination DataFrame
df_combinaciones_hombre["genero"] = "Hombre"
df_combinaciones_mujer["genero"] = "Mujer"

# Generate random ages in the range of 20 to 30
df_combinaciones_hombre["edad"] = [rd.randint(20, 30) for _ in range(len(df_combinaciones_hombre))]
df_combinaciones_mujer["edad"] = [rd.randint(20, 30) for _ in range(len(df_combinaciones_mujer))]

# Generate birthdate based on the calculated age
current_year = datetime.now().year
df_combinaciones_hombre["fecha_nacimiento"] = df_combinaciones_hombre["edad"].apply(
    lambda age: datetime(current_year, 1, 1) - timedelta(days=age * 365))
df_combinaciones_mujer["fecha_nacimiento"] = df_combinaciones_mujer["edad"].apply(
    lambda age: datetime(current_year, 1, 1) - timedelta(days=age * 365))

# Generate CURP based on the generated data
df_combinaciones_hombre["curp"] = df_combinaciones_hombre.apply(
    lambda row: generate_curp(row["nombre1"], row["apellido1"], row["apellido2"], row["fecha_nacimiento"], row["genero"], "DF"),
    axis=1
)
df_combinaciones_mujer["curp"] = df_combinaciones_mujer.apply(
    lambda row: generate_curp(row["nombre1"], row["apellido1"], row["apellido2"], row["fecha_nacimiento"], row["genero"], "DF"),
    axis=1
)

# Combine the results into a single DataFrame
result_df = pd.concat([df_combinaciones_hombre, df_combinaciones_mujer], ignore_index=True)
result_df.columns = ["nombre1", "nombre2", "apellido1", "apellido2", "genero", "edad", "fecha_nacimiento", "curp"]
result_df["id"] = [i for i in range(1, len(result_df) + 1)]

result_df["voto"] = [rd.randint(1, 5) for _ in range(len(result_df))]
result_df["email"] = result_df.apply(
    lambda row: f"{row['nombre1'].lower()}{row['apellido1'].lower()}{row['id']}@urcmac.edu.mx", axis=1)
result_df["password"] = result_df.apply(
    lambda row: f"{row['apellido1'].lower()}{row['nombre1'].lower()}{row['id']}", axis=1)

result_df.to_csv("base01.csv", index=False)
