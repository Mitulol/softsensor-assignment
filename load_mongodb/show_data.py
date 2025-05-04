from pymongo import MongoClient

client = MongoClient("mongodb+srv://mitgoel:mitul@cluster0.znrp0w5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = client["softsensor"]

print("Collections:", db.list_collection_names())
for collection_name in db.list_collection_names():
    count = db[collection_name].count_documents({})
    print(f"{collection_name}: {count} documents")
