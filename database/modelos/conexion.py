from pymongo import MongoClient

uri = ""

client = MongoClient(uri)

print("Conectado a MongoDB Atlas")

print(client.list_database_names())
