from fastapi import FastAPI
from database.core import engine, Base
from entities.user import User
from api import register_routes
import uvicorn

app = FastAPI()

# Base.metadata.create_all(bind=engine)

register_routes(app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000)
