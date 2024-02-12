import threading
import argparse
import configparser

from flask import Flask, request, make_response
from Db.db_connection import init_mongo_client
from service.get_data import get_video_data, get_search_data
from service.scheduling import schedule_task

# load all the config
config = configparser.ConfigParser()
config.read("./config/config.ini")

# initiating Flask app & db connection
app = Flask(__name__)
init_mongo_client(app, config)


# get api with pagination
@app.route("/get_videos", methods=['GET'])
def get_videos():
    
    
    page_number = int(request.args.get('page',0))
    page_limit = int(config["Application"]["data_query_limit"])

    # service function to get data 
    response_data = get_video_data(page_number, page_limit) 
    return make_response(response_data)


# search data api with pagination
@app.route("/search_videos", methods=['GET'])
def search_videos():

    page_number = int(request.args.get('page',0))
    page_limit = int(config["Application"]["data_query_limit"])
    text = request.args.get('search','')

    # service function to get data 
    response_data = get_search_data(text, page_number, page_limit)
    
    return make_response(response_data)

    

if __name__ == "__main__":
    
    # Arg parser for local developement customisation
    PARSER = argparse.ArgumentParser(description="FamPay-Assignment")

    PARSER.add_argument('-d', '--debug', help="Use flask debug mode", default= False, type= bool)
    PARSER.add_argument('-p', '--port', help="change port", default= 5002, type= int)
    ARGS = PARSER.parse_args()

    PORT = ARGS.port
    DEBUG = ARGS.debug

    time_interval = int(config["Application"]["time_interval_in_sec"])

    # start a schedule job in a thread, which keeps on fetching the data parallel of web server
    threading.Thread(target = schedule_task, args = (time_interval, config)).start()

    app.run(host='0.0.0.0', port = PORT, debug = DEBUG)
 