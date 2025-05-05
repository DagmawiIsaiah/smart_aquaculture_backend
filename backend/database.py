# used motor package to connect to mongodb
from motor.motor_asyncio import AsyncIOMotorClient

# define monogodb uri
MONGO_URI = "mongodb://localhost:27017" # localhost = 172.0.0.1

client = AsyncIOMotorClient(MONGO_URI)
db = client.smart_aquaculture

# collections are tables in our db
user_collection = db.get_collection("users")
temperature_collection = db.get_collection("temperatures")
ph_collection = db.get_collection("ph")
turbidity_collection = db.get_collection("turbidity")
