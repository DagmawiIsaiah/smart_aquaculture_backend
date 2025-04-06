from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://localhost:27017"  # or use a cloud URI like MongoDB Atlas
client = AsyncIOMotorClient(MONGO_URI)
db = client.smart_aquaculture
user_collection = db.get_collection("users")
temperature_collection = db.get_collection("temperatures")
ph_collection = db.get_collection("ph")
turbidity_collection = db.get_collection("turbidity")
feeding_collection = db.get_collection("feeding")
