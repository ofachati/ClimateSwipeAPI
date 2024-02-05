import motor.motor_asyncio
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
from decouple import config

MONGO_DETAILS = config("MONGO_DETAILS")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.nuitinfo
users_collection = database.get_collection("users_collection")

# helpers
def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "full_name": user["full_name"],
        "password": user["password"],
    }

# Retrieve all users present in the database
async def retrieve_users():
    users = []
    async for user in users_collection.find():
        users.append(user_helper(user))
    return users

# Add a new user into the database
async def add_user(user_data: dict) -> dict:
    user = await users_collection.insert_one(user_data)
    new_user = await users_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)

# Retrieve a user with a matching username
async def retrieve_user(username: str) -> dict:
    user = await users_collection.find_one({"username": username})
    if user:
        return user_helper(user)

# Update a user with a matching username
async def update_user(username: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    user = await users_collection.find_one({"username": username})
    if user:
        updated_user = await users_collection.update_one(
            {"username": username}, {"$set": data}
        )
        if updated_user:
            return True
        return False

# Delete a user from the database
async def delete_user(username: str):
    user = await users_collection.find_one({"username": username})
    if user:
        await users_collection.delete_one({"username": username})
        return True
