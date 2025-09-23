from database.core import DbSession
from . import model
from entities import Post, User
from sqlalchemy import desc, func
from exceptions import SQLErrorException, map_sqlalchemy_error

def search_post(db: DbSession, username: str) -> list[model.PostResponse]:
    try:
        user = db.query(User).filter(func.lower(User.username) == username.lower()).first()
        if not user:
            raise SQLErrorException(404, "User not found")
        return user.posts
    except Exception as error:
        status, message = map_sqlalchemy_error(error)
        raise SQLErrorException(status, f'{message}')

def add_post(db: DbSession, post: model.PostCreate) -> model.PostResponse:
    db_post = Post(**post.model_dump())
    try:
        user = db.query(User).filter(User.id == post.user_id).first()
        if not user:
            raise SQLErrorException(404, "User not found")
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post
    except Exception as error:
        status, message = map_sqlalchemy_error(error)
        raise SQLErrorException(status, f'{message}')

def list_post(db: DbSession, skip: int = 0, limit: int = 3) -> list[model.PostResponse]:
    try: 
        return db.query(Post).order_by(desc(Post.id)).offset(skip).limit(limit).all()
    except Exception as error:
        status, message = map_sqlalchemy_error(error)
        raise SQLErrorException(status, f'{message}')

def update_post(db: DbSession, post_id: int, updated_post: model.PostUpdate) -> model.PostResponse:
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise SQLErrorException(404, "Post not found")
    for key, value in updated_post.model_dump(exclude_unset=True).items():
        setattr(db_post, key, value)
    
    try: 
        db.commit()
        db.refresh(db_post)
        return db_post
    except Exception as error:
        status, message = map_sqlalchemy_error(error)
        raise SQLErrorException(status, f'{message}') 
    
def delete_post(db: DbSession, post_id: int) -> list[model.PostResponse]:
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise SQLErrorException(404, "Post not found")
    try:
        db.delete(db_post)
        db.commit()
        return db.query(Post).all()
    except Exception as error:
        status, message = map_sqlalchemy_error(error)
        raise SQLErrorException(status, f'{message}')



