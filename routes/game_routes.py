from fastapi import APIRouter, HTTPException, status
from models.user import User
import utils.data_functions as data_functions
import requests
import random

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
async def inser_user(user: User):
    if data_functions.get_user(user.user_id) is None:
        data_functions.insert_user(user.user_id)
        return {status.HTTP_201_CREATED: "User created"}
    else:
        return {status.HTTP_409_CONFLICT: "User already exists"}

@router.post("/trivia/score")
async def inser_user(user: User):
    data_functions.update_user_score(user.user_id)
    return {status.HTTP_200_OK: "User score incremented"}

@router.get("/trivia/score")
async def inser_user(user: User):
    result = data_functions.get_user(user.user_id)
    return {"HTTP status code": status.HTTP_200_OK, "user": result}


@router.get("/trivia/{category}")
async def get_trivia(category: str):
    category_id = 0
    if category == "random":
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
    
    
