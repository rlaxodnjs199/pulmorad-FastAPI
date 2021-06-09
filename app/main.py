from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import config
from app.api.v1.router import api_router

app = FastAPI(debug=config.DEBUG)
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:3000",
                   "https://pulmorad.lamis.life"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
