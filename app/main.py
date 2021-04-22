from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

from app import config
from app.core.auth import auth_router
from app.db.redis.session import get_redis

from app.api.v1.user.endpoints import user_router
from app.api.v1.project.endpoints import project_router

from app.db.pgsql.base_model import Base
from app.db.pgsql.session import get_engine
Base.metadata.create_all(bind=get_engine(config.DATABASE_URL))

app = FastAPI(debug=config.DEBUG)
app.include_router(auth_router, tags=['auth'])
app.include_router(user_router, tags=['user'])
app.include_router(project_router, tags=["project"])

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event('startup')
async def starup_event():
    await get_redis().init_redis_pool()


@app.on_event('shutdown')
async def shutdown_event():
    get_redis().close()
    await get_redis().close()


@app.get('/protected')
def protected(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )
