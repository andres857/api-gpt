from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy import create_engine
import os

client = AsyncIOMotorClient(os.environ.get('DB_URI'))
database = client.get_database("test_database")

def get_database():
    return database

def get_db_connection_myzonego():
    database_url = f'mysql+mysqlconnector://{os.environ.get("DB_USERNAME")}:{os.environ.get("DB_PASSWORD")}@{"192.168.0.102"}:{3307}/{os.environ.get("DB_DATABASE")}'
    engine = create_engine(database_url)    
    return engine
