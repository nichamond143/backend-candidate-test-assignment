from fastapi import APIRouter
from . import service

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.get("/login")
def login():
    '''Redirect to authentication api (Auth0)'''
    return service.login()


@router.get("/token")
def get_access_token(code: str):
    '''Exchange authentication code for access token'''
    return service.get_access_token(code)
