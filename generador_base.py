from itertools import product
import pandas as pd
import numpy as np
import random as rd 
from tkinter import *

df_base = pd.read_csv("bd_402.csv")


df_hombre = df_base[df_base["genero"] == "Hombre"]
df_mujer = df_base[df_base["genero"] == "Mujer"]


combinaciones_hombre = list(product(df_hombre["nombre1"], df_hombre["nombre2"], df_hombre["apellido1"], df_hombre["apellido2"]))
combinaciones_hombre  = list(set(combinaciones_hombre ))  # Remove duplicates

combinaciones_mujer = list(product(df_mujer["nombre1"], df_mujer["nombre2"], df_mujer["apellido1"], df_mujer["apellido2"]))
combinaciones_mujer = list(set(combinaciones_mujer))  # Remove duplicates

# Create DataFrames for each gender"s combinations
df_combinaciones_hombre  = pd.DataFrame(combinaciones_hombre , columns=["nombre1", "nombre2", "apellido1", "apellido2"])
df_combinaciones_mujer = pd.DataFrame(combinaciones_mujer, columns=["nombre1", "nombre2", "apellido1", "apellido2"])

# Add the GENDER column back to each combination DataFrame
df_combinaciones_hombre ["genero"] = "Hombre"
df_combinaciones_mujer["genero"] = "Mujer"

# Generate random ages in the range of 20 to 30
df_combinaciones_hombre ["edad"] = [rd.randint(20, 30) for _ in range(len(df_combinaciones_hombre ))]
df_combinaciones_mujer["edad"] = [rd.randint(20, 30) for _ in range(len(df_combinaciones_mujer))]

# Combine the results into a single DataFrame
result_df = pd.concat([df_combinaciones_hombre , df_combinaciones_mujer], ignore_index=True)
result_df.columns = ["nombre1", "nombre2", "apellido1", "apellido2", "genero", "edad"]
result_df["id"] = [i for i in range(1, len(result_df) + 1)]

result_df["voto"] = [rd.randint(1, 5) for _ in range(len(result_df))]
result_df["email"] = result_df.apply(lambda row: f"{row["nombre1"].lower()}{row["apellido1"].lower()}{row["id"]}@urcmac.edu.mx", axis=1)
result_df["password"] = result_df.apply(lambda row: f"{row["apellido1"].lower()}{row["nombre1"].lower()}{row["id"]}", axis=1)

result_df.to_csv("base.csv")
