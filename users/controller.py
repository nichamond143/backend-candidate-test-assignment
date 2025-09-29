from typing import List
from fastapi import APIRouter, Depends

from database.core import DbSession
from . import model
from . import service
from auth.service import validate
from auth.model import UserClaims
from faststream.redis import RedisBroker
from redis_client.client import get_broker

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/create", response_model=model.UserResponse)
async def create_users(
    user: model.UserCreate,
    db: DbSession,
    broker: RedisBroker = Depends(get_broker),
    user_claims: UserClaims = Depends(validate)
):
    '''Create user data'''
    return await service.create_user(db, user, broker)


@router.get("/list", response_model=List[model.UserResponse])
def list_users(
    db: DbSession,
    skip: int = 0,
    limit: int = 3,
    user_claims: UserClaims = Depends(validate)
):
    """List all users with pagination"""
    return service.list_users(db, skip=skip, limit=limit)


@router.put("/update", response_model=model.UserResponse)
def update_users(
    db: DbSession,
    user_id: int,
    updated_user: model.UserUpdate,
    user_claims: UserClaims = Depends(validate)
):
    '''Update user with user id'''
    return service.update_user(db, user_id, updated_user)

@router.delete("/delete")
def delete_user(
    db: DbSession,
    user_id: int,
    user_claim: UserClaims = Depends(validate)
):
    '''Delete user with user id'''
    return service.delete_user(db, user_id)