from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

from app import config
from app.core.auth import auth_router
from app.db.redis.session import redis

from app.api.v1.user.endpoints import user_router
from app.api.v1.project.endpoints import project_router
from app.api.v1.measurement.endpoints import measurement_router

from app.db.pgsql.base_model import Base
from app.db.pgsql.session import get_engine

Base.metadata.create_all(bind=get_engine(config.DATABASE_URL))

app = FastAPI(debug=config.DEBUG)
app.include_router(auth_router, tags=['auth'])
app.include_router(user_router, tags=['user'])
app.include_router(project_router, tags=["project"])
app.include_router(measurement_router, tags=["measurement"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:3000",
                   "https://pulmorad.lamis.life"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.on_event('startup')
# async def starup_event():
#     await redis.init_redis_pool()


# @app.on_event('shutdown')
# async def shutdown_event():
#     await redis.terminate()


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
