from flask_pymongo import PyMongo



# global varible for processing db transactions
mongo = PyMongo()

def init_mongo_client(app, config):
    """
    Setting up mongo client connection
    Args:
        app (flask): flask app for uri configuration setup
        config (configparser): extracting config from resources
        
    """
    app.config['MONGO_URI'] = get_mongo_uri(config)
    mongo.init_app(app)


def construct_mongo_uri(username, password, host, port, database, auth_source="admin"):
    """
    creating mongo uri
    Args:
        username (string) : db username
        password (string) : db password
        host (string) : db host
        port (int) : db port
        database (string) : default db
        auth_source (string) : authentication db
    
    Returns:
        - string : mongo uri
        
    """
    if username and password:
        return f"mongodb://{username}:{password}@{host}:{port}/{database}?authSource={auth_source}"
    else:
        return f"mongodb://{host}:{port}/{database}"
    
def get_mongo_uri(config):
    
    """
    parses db config 
    Args:
        config(configparser) : config parser object
    Returns:
        - string : mongo uri
        
    """
    
    host =  config["Database"]["host"] 
    port = int(config["Database"]["port"])
    user = config["Database"]["user"]
    password = config["Database"]["password"]
    database = config["Database"]["database"]
    auth_db = config["Database"]["authenticate_db"] 

    return construct_mongo_uri(user, password, host, port, database, auth_db)
