from pymongo import MongoClient
from sqlalchemy import create_engine
import os

def connect_to_database():
    uri = os.environ.get('DB_URI')
    client = MongoClient(uri)
    db = client["test_database"]
    return db

def get_db_connection_myzonego():
    database_url = f'mysql+mysqlconnector://{os.environ.get("DB_USERNAME")}:{os.environ.get("DB_PASSWORD")}@{"192.168.0.102"}:{3307}/{os.environ.get("DB_DATABASE")}'
    engine = create_engine(database_url)    
    return engine
