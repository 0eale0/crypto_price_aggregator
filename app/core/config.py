import os
from dotenv import load_dotenv

load_dotenv()


class Configuration:
    SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://postgres:{os.environ.get("DB_PASSWORD")}@{os.environ.get("DB_HOSTNAME")}'
    # "postgresql+psycopg2://postgres:03082002@localhost:5432/database2"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True
    SECRET_KEY = "ekjhrkgwkhjsdghkt"

    print(SQLALCHEMY_DATABASE_URL)
