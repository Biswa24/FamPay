import time, traceback
from datetime import datetime
import schedule
from datetime import timedelta
from util.date_time_util import get_time_from_string, get_time_in_string
from service.fetch_data import fetch_youtube_data
from Db.db_operations import store_youtube_video_data



def schedule_task(time_interval, config):

    """
    Creates a schedule.

    Args:
    - time_interval(int) : time interval for job run
    - config(configparser): configparser instance
    """
    time_interval = int(config["Application"]["time_interval_in_sec"])
    

    try:
        # # triggers func - job after time_interval
        schedule.every(time_interval).seconds.do(job, config)
        while True:
            schedule.run_pending()
            time.sleep(1)
    except Exception as e:
        print(e)
        traceback.print_exc()



def job(config):

    """
    Job that schedule is running.

    Args:
    - config(configparser): configparser instance

    Use global variable 'published_after' to keep track of time for which data is fetched
    better to use job returned data or class based approach instead of global 
    """
    
     # for 1st iteration fetches time from db default handling current time
    published_after = config.get("Application","published_after")
    time_interval = int(config["Application"]["time_interval_in_sec"])

    record_list = fetch_youtube_data(published_after, config)

    print(f"Data  fetched from - {published_after} records fetched - {len(record_list)}")

    last_record_time = None

    if record_list:
        # storing videos data in db 
        store_youtube_video_data(record_list)

        # extracting published time of last video which is fetched
        last_record_time = get_time_from_string(record_list[-1]["published_at"])
    else:
        # default/None case handling
        last_record_time = datetime.utcnow()
    
    # calculating the time for next iterationg
    next_interval_time = get_time_from_string(published_after) + timedelta(seconds= time_interval)
    update_date_time = max(last_record_time, next_interval_time)
    
    # setting the time for next iteration, as using global variable
    published_after = get_time_in_string(update_date_time)
    config.set("Application", "published_after", published_after)

