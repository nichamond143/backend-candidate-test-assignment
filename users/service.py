from database.core import DbSession
from . import model
from entities.user import User

def create_user(db: DbSession, user: model.UserCreate) -> model.UserResponse:
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def list_users(db: DbSession, skip: int = 0, limit: int = 3) -> list[model.UserResponse]:
    return db.query(User).offset(skip).limit(limit).all()
