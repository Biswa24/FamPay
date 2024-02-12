from util.date_time_util import get_time_in_string
from googleapiclient.discovery import build
from Db.db_operations import get_new_api_key
from googleapiclient.errors import HttpError

def create_youtube_client(api_key):
    """
    Creates a YouTube API client.

    Args:
    - api_key (str): Your YouTube Data API key.

    Returns:
    - googleapiclient.discovery.Resource: The YouTube API client.
    """
    api_service_name = "youtube"
    api_version = "v3"
    youtube = build(api_service_name, api_version, developerKey=api_key)
    return youtube

def fetch_youtube_data(published_after, config):

    """
    Fetches data from youtube

    Args:
    - youtube (googleapiclient.discovery.Resource ): youtube client.
    - keyword (string) : query for data fetch
    - published_after(string): string formatted date for data fetch

    Returns:
    - dict 
        - list of object: processed data
        - key expiry status
    """
    keyword = config["Application"]["query_keyword"] 
    api_key = config["Application"]["api_key"]
    if(api_key == None or len(api_key) == 0):
        updateKey(config)
    youtube = create_youtube_client(config["Application"]["api_key"])

    request = youtube.search().list(
        q = keyword,
        part = "snippet",
        type = "video",
        publishedAfter = published_after,
        maxResults = 20
    )
    video_data_list = []
    try:
        response = request.execute()
        
        for item in response['items']:
            record = get_cleaned_data(item)
            if(record != None):
                video_data_list.append(record)
    except HttpError as e:
        print(f"Quota Exhausted: {e.error_details}")

        # fetch new key from db and update in config for next iteration
        updateKey(config)

    except Exception as e:
        print(f"An error occurred: {e}")
    
    return video_data_list

def get_cleaned_data(item):
    """
    Process record data fetched youtube

    Args:
    - item (object ): youtube record of video

    Returns:
    - object: processed data
    """

    record = None
    if(item.get('snippet', None) != None):
        record = {}
        record["title"] = item['snippet'].get('title','')
        record["desc"] = item['snippet'].get('description','')
        record["published_at"] = item['snippet'].get('publishedAt', get_time_in_string())
        record["video_id"] = item.get("id",{}).get("videoId",'')
        record["thumbnail_urls"] = {}
        for quality in item['snippet'].get('thumbnails',{}).keys():
            if(item['snippet']['thumbnails'][quality].get('url', None) != None ):
                record['thumbnail_urls'][quality] = item['snippet']['thumbnails'][quality]['url']
    
    return record




# Raises an exception to halt the process of fetching data from youtube, once all key is exhausted
def updateKey(config):
    """
    Update Api key in config after quota exhausted

    Args:
    - config (configparser ): youtube record of video

    """
    api_key_record = get_new_api_key(config["Application"]["api_key"])
    if api_key_record != None and api_key_record.get("key", None) != None:
        config.set("Application", "api_key", api_key_record["key"])
    else:
        raise RuntimeError("No new key found")
