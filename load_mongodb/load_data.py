from pymongo import MongoClient
import json

client = MongoClient("mongodb+srv://mitgoel:mitul@cluster0.znrp0w5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = client["softsensor"]

collections = {
    "vehicles": "json_data/vehicles.json",
    "logistics_companies": "json_data/logistics_companies.json",
    "drivers": "json_data/drivers.json",
    "stops": "json_data/stops.json",
    "zones": "json_data/zones.json",
    "inspections": "json_data/inspections.json"
}

for name, file in collections.items():
    with open(file, "r") as f:
        data = json.load(f)
        if isinstance(data, list):
            db[name].insert_many(data)
        else:
            db[name].insert_one(data)

print("All data loaded into MongoDB!")
