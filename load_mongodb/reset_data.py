from pymongo import MongoClient

client = MongoClient("mongodb+srv://mitgoel:mitul@cluster0.znrp0w5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = client["softsensor"]

for name in db.list_collection_names():
    db.drop_collection(name)
    print(f"Dropped collection: {name}")

print(" All collections dropped.")
