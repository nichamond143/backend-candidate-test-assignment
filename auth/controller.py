from fastapi import APIRouter
from . import service

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.get("/login")
def login():
    return service.login()


@router.get("/token")
def get_access_token(code: str):
    return service.get_access_token(code)
