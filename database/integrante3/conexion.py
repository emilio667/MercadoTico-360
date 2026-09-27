from pymongo import MongoClient

uri = "mongodb+srv://jmezgustavo_db_user:****@cluster0.qw0lle9.mongodb.net/?appName=Cluster0"

client = MongoClient(uri)

print("Conectado a MongoDB Atlas")

print(client.list_database_names())
