import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    TINYDB_PATH = os.getenv('TINYDB_PATH', 'db.json')
    API_KEY = os.getenv('API_KEY')
