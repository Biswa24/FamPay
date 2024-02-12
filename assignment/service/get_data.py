from Db.db_operations import get_data, search_data
from flask_api import status

def get_video_data(page_number, page_limit):

    """
    Prepare the data for get api

    Args:
    - page_number (int ): current page number 
    - page_limit (int ): page limit from config

    Returns:
    - list of object: processed data
    """

    if(page_number < 0):
        return ({}, status.HTTP_400_BAD_REQUEST)
    
    offset = page_number * page_limit
    limit = (page_number+1) * page_limit

    video_data_list = get_data(limit, offset)
    data_list = prepare_data(video_data_list)
    prev_page = None
    next_page = None

    if page_number>0:
        prev_page = page_number -1
    
    if len(video_data_list) == page_limit :
        next_page = page_number+1
    
    response_data = {
        "data" : data_list,
        "prev_page" : prev_page,
        "next_page" : next_page
    }

    return (response_data, status.HTTP_200_OK)

def get_search_data(text, page_number, page_limit):
    """
    Prepare the data for search api

    Args:
    - text (string) : query text for search
    - page_number (int ): current page number 
    - page_limit (int ): page limit from config

    Returns:
    - list of object: processed data
    """

    if(page_number < 0 or text == None or len(text) == 0):
        return ({}, status.HTTP_400_BAD_REQUEST)
    
    offset = page_number * page_limit
    limit = (page_number+1) * page_limit

    video_data_list = search_data(text, limit, offset)
    data_list = prepare_data(video_data_list)
    prev_page = None
    next_page = None

    if page_number>0:
        prev_page = page_number -1
    
    if len(video_data_list) == page_limit :
        next_page = page_number+1
    
    response_data = {
        "data" : data_list,
        "prev_page" : prev_page,
        "next_page" : next_page
    }
    return (response_data, status.HTTP_200_OK)


def prepare_data(record_list):

    """
    Prepare the data for search api

    Args:
    - record_list (list of db object) : db fetched object

    Returns:
    - list of object: processed data
    """
        
    data = []
    for record in record_list:
        data_record = {
            "title" : record["title"],
            "description" : record["desc"],
            "published_at" : record["published_at"],
            "video_id" : record["video_id"],
            "thumbnails": record["thumbnail_urls"]
        }
        data.append(data_record)
    
    return data
