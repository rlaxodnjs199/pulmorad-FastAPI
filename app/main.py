from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import config
#from app.db.redis.session import redis

from app.api.v1.project.endpoints import project_router
from app.api.v1.cfd.endpoints import cfd_router

from app.db.pgsql.base_model import Base
from app.db.pgsql.session import get_engine

Base.metadata.create_all(bind=get_engine(config.DATABASE_URL))

app = FastAPI(debug=config.DEBUG)
app.include_router(project_router, tags=["project"])
app.include_router(cfd_router, tags=["cfd"], prefix="/cfd")

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
