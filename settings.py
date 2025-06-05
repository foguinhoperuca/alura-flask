import os

from dotenv import load_dotenv


load_dotenv()
SECRET_KEY = str(os.getenv('SECRET_KEY'))
DEBUG = bool(int(os.getenv('DEBUG', 0)))
ALLOWED_HOST: str = str(os.getenv('ALLOWED_HOST', 'localhost'))
ALLOWED_PORT: str = str(os.getenv('ALLOWED_PORT', '8080'))

DB_ENGINE = str(os.getenv('DB_ENGINE'))
DB_NAME = str(os.getenv('DB_NAME'))
DB_HOST = str(os.getenv('DB_HOST'))
DB_USER = str(os.getenv('DB_USER'))
DB_PASSWORD = str(os.getenv('DB_PASSWORD'))
SQLALCHEMY_DATABASE_URI = f'{DB_ENGINE}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/media/uploads'
