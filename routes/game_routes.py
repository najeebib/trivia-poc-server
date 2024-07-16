from fastapi import APIRouter, HTTPException, status
from models.user import User
import utils.data_functions as data_functions
import requests
import random
from data.database import MongoAPI
mongo_api = MongoAPI()
router = APIRouter()

categories = {
    "General Knowledge": 9,
    "Entertainment: Books": 10,
    "Entertainment: Film": 11,
    "Entertainment: Music": 12,
    "Entertainment: Musicals & Theatres": 13,
    "Entertainment: Television": 14,
    "Entertainment: Video Games": 15,
    "Entertainment: Board Games": 16,
    "Science & Nature": 17,
    "Science: Computers": 18,
    "Science: Mathematics": 19,
    "Mythology": 20,
    "Sports": 21,
    "Geography": 22,
    "History": 23,
    "Politics": 24,
    "Art": 25,
    "Celebrities": 26,
    "Animals": 27,
    "Vehicles": 28,
    "Entertainment: Comics": 29,
    "Science: Gadgets": 30,
    "Entertainment: Japanese Anime & Manga": 31,
    "Entertainment: Cartoon & Animations": 32
}

TRIVIA_API_URL = "https://opentdb.com/api.php?amount=1&type=boolean&category="

@router.post("/trivia/start")
async def insert_user(user: User):
    if data_functions.get_user(user.user_id, mongo_api) is None:
        result = data_functions.insert_user(user.user_id, mongo_api)
        if result["Status"] == "Successfully Inserted":
            return {status.HTTP_201_CREATED: "User created"}
        else:
            raise HTTPException(status_code=500, detail="Server error")
    else:
        raise HTTPException(status_code=409, detail="User already exists")

@router.post("/trivia/score")
async def increment_score(user: User):
    result = data_functions.update_user_score(user.user_id, mongo_api)
    if result["Status"] == "Successfully Updated" and result["Matched_Count"] == 1:
        return {status.HTTP_200_OK: "User score incremented"}
    raise HTTPException(status_code=404, detail="No user with this ID exists")

@router.get("/trivia/score")
async def get_user(user: User):
    result = data_functions.get_user(user.user_id, mongo_api)
    if result:
        return {"HTTP status code": status.HTTP_200_OK, "user": result}
    raise HTTPException(status_code=404, detail="No user with this ID exists")


@router.get("/trivia/{category}")
async def get_trivia(category: str):
    category_id = 0
    if category == "Random":
        category_id = random.choice(list(categories.values()))
    elif category in categories:  # Check if the category is valid
        category_id = categories[category]
    else:
        raise HTTPException(status_code=404, detail="Invalid category")
    response = requests.get(f"{TRIVIA_API_URL}{category_id}")
    
    if response.status_code == 200:
        trivia_data = response.json()
        return trivia_data['results'][0] if trivia_data['results'] else {"question": "No questions available"}
    
    raise HTTPException(status_code=response.status_code, detail="Unable to fetch trivia questions")
    
    
