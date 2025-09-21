from typing import List
from fastapi import APIRouter, Depends

from database.core import DbSession
from . import model
from . import service
from auth.service import validate
from auth.model import UserClaims

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/create", response_model=model.UserResponse)
def create(
    user: model.UserCreate,
    db: DbSession,
    user_claims: UserClaims = Depends(validate)
):
    return service.create_user(db, user)


@router.get("/list", response_model=List[model.UserResponse])
def list_users(
    db: DbSession,
    skip: int = 0,
    limit: int = 3,
    user_claims: UserClaims = Depends(validate)
):
    """List all users with pagination"""
    return service.list_users(db, skip=skip, limit=limit)
