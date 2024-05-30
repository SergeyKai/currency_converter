from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())


class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = True if os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS') == 1 else False
    EXCHANGE_RATE_API_URL = 'https://api.apilayer.com/currency_data/'
    API_KEY = os.environ.get('API_KEY')
