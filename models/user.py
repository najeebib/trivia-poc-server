from pydantic import BaseModel

class User(BaseModel):
    username: str
    score: int
