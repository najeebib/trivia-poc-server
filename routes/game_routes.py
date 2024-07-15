from fastapi import APIRouter, HTTPException, status
from models.user import User
import utils.data_functions as data_functions
import requests
import random

router = APIRouter()

categories = {
    "animals": 27,
    "sports": 21,
    "geography": 22,
    "history": 23,
    "art": 25,
    "books": 10,
    "television": 14,
    "film": 11
}

TRIVIA_API_URL = "https://opentdb.com/api.php?amount=1&type=boolean&category="

@router.post("/trivia/start")
async def inser_user(user: User):
    data_functions.insert_user(user.username)
    return {status.HTTP_201_CREATED: "User created"}

@router.post("/trivia/score")
async def inser_user(user: User):
    data_functions.update_user_score(user.username)
    return {status.HTTP_200_OK: "User score increased"}

@router.get("/trivia/score")
async def inser_user(user: User):
    result = data_functions.get_user(user.username)
    return {status.HTTP_200_OK: "User score increased", "user": result}


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
    
    
