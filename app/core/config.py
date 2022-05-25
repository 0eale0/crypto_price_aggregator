import os
from dotenv import load_dotenv

load_dotenv()


class Configuration:
    SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://postgres:{os.environ.get("DB_PASSWORD")}@{os.environ.get("DB_HOSTNAME")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True
    SECRET_KEY = "ekjhrkgwkhjsdghkt"
