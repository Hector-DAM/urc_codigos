import pandas as pd

# Read CSV file into a DataFrame
df = pd.read_csv("base01.csv")

# Convert DataFrame to JSON
json_data = df.to_json(orient='records')

# Specify the file path for saving the JSON file
json_file_path = "base01.json"

# Write JSON data to the specified file path
with open(json_file_path, 'w') as json_file:
    json_file.write(json_data)

print(f"CSV file 'base01.csv' has been successfully converted to JSON: {json_file_path}")
