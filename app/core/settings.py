from functools import lru_cache
from app.config import SECRET_KEY
from pydantic import BaseModel


class JWT_Settings(BaseModel):
    authjwt_secret_key: str = SECRET_KEY
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_csrf_protect: bool = True
    authjwt_cookie_samesite: str = 'lax'


@lru_cache
def get_JWT_settings():
    return JWT_Settings()
