from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from faststream.redis import RedisBroker
from faststream.redis import BinaryMessageFormatV1
from contextlib import asynccontextmanager

from database.core import engine, Base
from api import register_routes
import uvicorn

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis_broker = RedisBroker(
        "redis://localhost:6379",
        message_format=BinaryMessageFormatV1(data=True, headers=True),
    )

    try:
        yield
    finally:
        await app.state.redis_broker.stop()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base.metadata.create_all(bind=engine)

register_routes(app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
