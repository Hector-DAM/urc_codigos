from itertools import product
import pandas as pd
import random as rd

# Read the base CSV file
df_base = pd.read_csv("bd_402.csv")

# Generate all combinations of surnames (apellido1)
all_apellido1_combinations = list(product(df_base["apellido1"], df_base["apellido2"]))
all_apellido1_combinations = list(set(all_apellido1_combinations))  # Remove duplicates

# Create a DataFrame for all apellido1 combinations
df_all_apellido1 = pd.DataFrame(all_apellido1_combinations, columns=["apellido1", "apellido2"])

# Separate names based on gender
df_hombre = df_base[df_base["genero"] == "Hombre"]
df_mujer = df_base[df_base["genero"] == "Mujer"]

# Generate all combinations of names for each gender
combinaciones_hombre = list(product(df_hombre["nombre1"], df_hombre["nombre2"], df_hombre["apellido1"], df_hombre["apellido2"]))
combinaciones_mujer = list(product(df_mujer["nombre1"], df_mujer["nombre2"], df_mujer["apellido1"], df_mujer["apellido2"]))

# Create DataFrames for hombres and mujeres
df_combinaciones_hombre = pd.DataFrame(combinaciones_hombre, columns=["nombre1", "nombre2", "apellido1", "apellido2"])
df_combinaciones_mujer = pd.DataFrame(combinaciones_mujer, columns=["nombre1", "nombre2", "apellido1", "apellido2"])

# Add the GENDER column back to each combination DataFrame
df_combinaciones_hombre["genero"] = "Hombre"
df_combinaciones_mujer["genero"] = "Mujer"

# Generate random ages in the range of 20 to 30
df_combinaciones_hombre["edad"] = [rd.randint(20, 30) for _ in range(len(df_combinaciones_hombre))]
df_combinaciones_mujer["edad"] = [rd.randint(20, 30) for _ in range(len(df_combinaciones_mujer))]

# Combine the results into a single DataFrame
result_df = pd.concat([df_combinaciones_hombre, df_combinaciones_mujer], ignore_index=True)

# Add additional columns
result_df["id"] = [i for i in range(1, len(result_df) + 1)]
result_df["voto"] = [rd.randint(1, 5) for _ in range(len(result_df))]
result_df["email"] = result_df.apply(lambda row: f"{row['nombre1'].lower()}{row['apellido1'].lower()}{row['id']}@urcmac.edu.mx", axis=1)
result_df["password"] = result_df.apply(lambda row: f"{row['apellido1'].lower()}{row['nombre1'].lower()}{row['id']}", axis=1)

# Save the result to a CSV file
result_df.to_csv("base01.csv", index=False)
