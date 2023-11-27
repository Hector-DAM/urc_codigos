from pymongo import MongoClient
from pymongo.server_api import ServerApi
import json

# MongoDB connection information
uri = "mongodb+srv://hadaya:24enero98@basedatos1.gamnobr.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Database and collection names
db_name = "BaseDatos1"
collection_name = "DatosPP"

# Access the specified database and collection
db = client[db_name]
collection = db[collection_name]

# JSON file path
json_file_path = "C:/Users/ESTUDIANTE-IRC-29/Documents/PP/final_data.json"

# Read and insert JSON data line by line
with open(json_file_path, 'r', encoding='utf-8-sig') as file:
    for line in file:
        try:
            # Parse each line as a separate JSON object
            json_data = json.loads(line)

            # Insert JSON data into the collection
            result = collection.insert_one(json_data)
            print(f"Inserted document with _id: {result.inserted_id}")

        except json.decoder.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
