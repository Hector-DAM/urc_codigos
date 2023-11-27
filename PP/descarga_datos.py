from pymongo import MongoClient
import pandas as pd

# MongoDB connection information
uri = "mongodb+srv://hadaya:24enero98@basedatos1.gamnobr.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)

# Database and collection names
db_name = "BaseDatos1"
collection_name = "DatosPP"

# Access the specified database and collection
db = client[db_name]
collection = db[collection_name]

# Fetch all documents from the collection
cursor = collection.find()

# Convert MongoDB cursor to DataFrame
df = pd.DataFrame(list(cursor))

# Specify the file path for saving the CSV file
csv_file_path = "exported_data.csv"

# Save DataFrame to CSV file
df.to_csv(csv_file_path, index=False)

print(f"Data exported to {csv_file_path}")
