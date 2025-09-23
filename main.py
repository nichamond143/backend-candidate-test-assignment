from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.core import engine, Base
from api import register_routes
import uvicorn

app = FastAPI()

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
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
