from starlette.config import Config

config = Config('.env')

DEBUG = config('DEBUG', cast=bool, default=False)
SECRET_KEY = config('SECRET_KEY')
DATABASE_URL = config('DATABASE_URL')
