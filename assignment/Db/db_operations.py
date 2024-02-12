from Db.db_connection import mongo
from util.date_time_util import get_time_in_string


def get_new_api_key(old_api_key):
    
    """
    Update old key and return new key
    Args:
        - old_api_key(string) : key to mark as quota exhasuted
    Returns:
    - string: start datetime formatted in string 
    """
    mongo.db.get_collection("ApiKey").update_one({"key" : old_api_key}, {"$set" : {"exhausted" : True}})

    record = mongo.db.get_collection("ApiKey").find_one({"exhausted" : {"$ne" : True}},{"key":1})
    return record

def store_youtube_video_data(record_list):
    """
    Storing videos data
    Args:
        - list of object: videos data list 
        
    """
    mongo.db.get_collection('VideoData').insert_many(record_list)



def get_data(limit, offset):
    """
    fetching videos data
    Args:
        - limit (int): query limit
        - offset (int): query skip
    Returns:
        - list of object : video data list
        
    """
    return list(mongo.db.get_collection('VideoData').find().sort([('_id', -1)]).skip(offset).limit(limit))
     

def search_data(text, limit, offset):

    """
    fetching videos data for a text
    Args:
        - limit (int): query limit
        - offset (int): query skip
        - text (string): query text string  
    Returns:
        - list of object : video data list
        
    """

    return list(mongo.db.get_collection('VideoData').find({
        "$or" : [
            {"title" : {"$regex" : text, "$options": "i"}},
            {"desc" : {"$regex" : text, "$options": "i"}}]
    }).sort([('_id', -1)]).skip(offset).limit(limit))