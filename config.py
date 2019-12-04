import os
from datetime import timedelta


class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY')
	JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
	JWT_TOKEN_LOCATION = ["json"]
	JWT_COOKIE_SECURE = False
	JWT_ACCESS_COOKIE_PATH = "/"
	JWT_REFRESH_COOKIE_PATH = "/token/refresh"
	JWT_COOKIE_CSRF_PROTECT = True
	JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=3)
	MIXPANEL_PROJECT_ID = os.environ.get("MIXPANEL_PROJECT_ID")
	SQLALCHEMY_DATABASE_URI = f'postgresql://{os.environ.get("POSTGRES_USER")}:{os.environ.get("POSTGRES_PW")}@localhost:5432/{os.environ.get("POSTGRES_DB")}'
	SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
	BASE_URL = "https://www.example.com"
	JWT_COOKIE_SECURE = True
	JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)
	SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class DevelopmentConfig(Config):
    BASE_URL = "http://localhost:5000"
    DEVELOPMENT = True
    DEBUG = True
