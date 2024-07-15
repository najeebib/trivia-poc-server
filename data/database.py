import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

class MongoAPI:
    def __init__(self) -> None:
        user = os.getenv("MONGODB_USER")
        password = os.getenv("MONGODB_PASSWORD")

        connection_string = f"mongodb+srv://{user}:{password}@cluster0.3pfnmy3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        
        self.client = MongoClient(connection_string)

        database = "trivia-game"
        users_collection = "users"
        cursor = self.client[database]
        self.users_collection = cursor[users_collection]
    
mongo_api = MongoAPI()