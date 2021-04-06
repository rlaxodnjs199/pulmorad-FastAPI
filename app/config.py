from starlette.config import Config
from starlette.datastructures import URL, CommaSeparatedStrings, Secret

config = Config('.env')

DEBUG = config('DEBUG', cast=bool, default=False)
SECRET_KEY = config('SECRET_KEY')
DATABASE_URL = config('DATABASE_URL', cast=URL)
REDIS_URL = config('REDIS_URL')
