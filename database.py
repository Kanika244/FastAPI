from motor.motor_asyncio import AsyncIOMotorClient





Mongo_url = "mongodb://127.0.0.1:27017"

client = AsyncIOMotorClient(Mongo_url)
database = client.get_database("college")
collection = database.get_collection("student")

user_collection=database["Authen"]

