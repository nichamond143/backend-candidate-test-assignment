from typing import List
from fastapi import APIRouter, Depends

from database.core import DbSession
from . import model
from . import service
from auth.service import validate
from auth.model import UserClaims

router = APIRouter(
    prefix="/posts",
    tags=["posts"]
)

@router.post("/add", response_model=model.PostResponse)
def add_post(
    db: DbSession,
    post: model.PostCreate,
    user_claims: UserClaims = Depends(validate)
):
    '''Add new post for user by user id'''
    return service.add_post(db, post)


@router.get("/search", response_model=List[model.PostResponse])
def search_posts(
    db: DbSession,
    username: str,
    user_claims: UserClaims = Depends(validate)
):
    """Search posts by username"""
    return service.search_post(db, username)

@router.get("/list", response_model=List[model.PostResponse])
def list_posts(
        db: DbSession,
        user_claims: UserClaims = Depends(validate)
):
    '''Get all posts'''
    return service.list_post(db)

@router.put("/update", response_model=model.PostResponse)
def update_post(
    db: DbSession,
    post_id: int,
    updated_post: model.PostUpdate,
    user_claims: UserClaims = Depends(validate)
):
    '''Update post description by post id'''
    return service.update_post(db, post_id, updated_post)

@router.delete("/delete", response_model=List[model.PostResponse])
def delete_post(
    db: DbSession, 
    post_id: int,
    user_claims: UserClaims = Depends(validate)):
    '''Delete post by post id'''
    return service.delete_post(db, post_id)