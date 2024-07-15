from data.database import mongo_api

def get_user(username: str):
    document = mongo_api.users_collection.find_one({"username": username})
    if document and '_id' in document:
            document['_id'] = str(document['_id'])
    return document

def insert_user(username: str):
    user = {'username': username, 'score': 0}
    response = mongo_api.users_collection.insert_one(user)
    output = {'Status': 'Successfully Inserted',
                  'Document_ID': str(response.inserted_id)}
    return output

def update_user_score(username: str):
    query = {'username': username}
    update = {"$inc": {'score': 1}}
    
    response = mongo_api.users_collection.update_one(query, update)
    if response.matched_count > 0:
        output = {'Status': 'Successfully Updated',
                  'Matched_Count': response.matched_count,
                  'Modified_Count': response.modified_count}
    else:
        output = {'Status': 'User Not Found'}

    return output

