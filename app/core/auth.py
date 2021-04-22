import datetime
from fastapi import Depends, APIRouter, HTTPException, status, Request, Security
from fastapi.security import OAuth2PasswordRequestFormStrict, SecurityScopes
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app.core.settings import get_JWT_settings
from app.db.pgsql.session import get_db
from app.db.redis.session import redis
from app.api.v1.user.util import get_user_by_id, get_user_by_username, get_permissions_from_user
from .schemas import Token, TokenData
from .util import authenticate_user, validate_user_permission, get_username_from_jwt

auth_router = auth = APIRouter()


@AuthJWT.load_config
def load_JWT_settings():
    return get_JWT_settings()


# @auth.get('/check-auth',
#           response_model=TokenData,
#           dependencies=[Security(validate_user_permission, scopes=["me:view"])])
# async def check_auth(username: str = Depends(get_username_from_jwt)):
#     return {'username': username}


@auth.post('/login', response_model=Token)
async def login(db: Session = Depends(get_db),
                form_data: OAuth2PasswordRequestFormStrict = Depends(),
                Authorize: AuthJWT = Depends()):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    expires_access_token = datetime.timedelta(minutes=30)
    expires_refresh_token = datetime.timedelta(hours=24)

    access_token = Authorize.create_access_token(
        subject=form_data.username, expires_time=expires_access_token)
    refresh_token = Authorize.create_refresh_token(
        subject=form_data.username, expires_time=expires_refresh_token)

    Authorize.set_access_cookies(access_token)
    Authorize.set_refresh_cookies(refresh_token)
    # Set Cookie: Permission in Redis
    scopes = get_permissions_from_user(db, user.id)
    str_scopes = ' '.join(scopes)
    # await redis.set(access_token, 'user')

    return {"access_token": access_token, "token_type": "bearer"}


@auth.post('/refresh')
def refresh(Authorize: AuthJWT = Depends()):
    Authorize.jwt_refresh_token_required()

    current_user = Authorize.get_jwt_subject()
    expires_access_token = datetime.timedelta(minutes=30)
    new_access_token = Authorize.create_access_token(
        subject=current_user, expires_time=expires_access_token)

    Authorize.set_access_cookies(new_access_token)

    return {"msg": "The token has been refresh"}


@auth.delete('/logout')
def logout(request: Request, Authorize: AuthJWT = Depends()):
    # Authorize.jwt_required()
    # redis.delete()
    # Redis unset Key
    Authorize.unset_jwt_cookies()

    return {"msg": "Successfully logout"}
