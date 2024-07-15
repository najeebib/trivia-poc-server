import pytest
import mongomock
from pymongo.collection import Collection
from data.database import MongoAPI
from utils.data_functions import get_user, insert_user, update_user_score

@pytest.fixture
def mock_mongo_client():
    client = mongomock.MongoClient()
    return client

@pytest.fixture
def mock_mongo_api(mock_mongo_client):
    class MockMongoAPI(MongoAPI):
        def __init__(self):
            self.client = mock_mongo_client
            database = "trivia-game"
            users_collection = "users"
            cursor = self.client[database]
            self.users_collection = cursor[users_collection]
    
    return MockMongoAPI()

def test_get_user(mock_mongo_api):
    mock_mongo_api.users_collection.insert_one({'user_id': 'test_user', 'score': 10})
    user = get_user('test_user', mock_mongo_api)
    assert user['user_id'] == 'test_user'
    assert user['score'] == 10

def test_insert_user(mock_mongo_api):
    response = insert_user('new_user', mock_mongo_api)
    assert response['Status'] == 'Successfully Inserted'
    user = mock_mongo_api.users_collection.find_one({'user_id': 'new_user'})
    assert user['user_id'] == 'new_user'
    assert user['score'] == 0

def test_update_user_score(mock_mongo_api):
    mock_mongo_api.users_collection.insert_one({'user_id': 'test_user', 'score': 10})
    response = update_user_score('test_user', mock_mongo_api)
    assert response['Status'] == 'Successfully Updated'
    assert response['Matched_Count'] == 1
    assert response['Modified_Count'] == 1
    user = mock_mongo_api.users_collection.find_one({'user_id': 'test_user'})
    assert user['score'] == 11

def test_update_user_score_not_found(mock_mongo_api):
    response = update_user_score('non_existing_user', mock_mongo_api)
    assert response['Status'] == 'User Not Found'
