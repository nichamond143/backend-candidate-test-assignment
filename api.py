from fastapi import FastAPI
from auth.controller import router as auth_router
from users.controller import router as users_router
from posts.controller import router as posts_router
from streams.controller import router as streams_router

def register_routes(app: FastAPI):
    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(posts_router)
    app.include_router(streams_router)