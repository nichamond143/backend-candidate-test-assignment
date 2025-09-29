from sqlalchemy import desc
from database.core import DbSession
from . import model
from entities.user import User
from exceptions import SQLErrorException, map_sqlalchemy_error
from redis_client.client import r
from redis_client.message import EventMessage
from faststream.redis import RedisBroker

async def create_user(db: DbSession, user: model.UserCreate, broker: RedisBroker) -> model.UserResponse:
    db_user = User(**user.model_dump())
    try: 
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        # r.xadd("event-stream", {"message": f"User created"})
        message = EventMessage(event_type="user_created", message=f"User {db_user.username} created")
        async with broker as br:
            await br.publish(
                message=message.model_dump_json().encode("utf-8"),
                stream="event-stream"
                )

        return db_user
    except Exception as error:
        status, message = map_sqlalchemy_error(error)
        raise SQLErrorException(status, f'{message}')

def list_users(db: DbSession, skip: int = 0, limit: int = 3) -> list[model.UserResponse]:
    try: 
        return db.query(User).order_by(desc(User.id)).offset(skip).limit(limit).all()
    except Exception as error:
        status, message = map_sqlalchemy_error(error)
        raise SQLErrorException(status, f'{message}')

def update_user(db: DbSession, user_id: int, updated_user: model.UserUpdate) -> model.UserResponse:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise SQLErrorException(404, "User not found")
    
    for key, value in updated_user.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)

    try:
        db.commit()
        db.refresh(db_user)

        r.xadd("event-stream", {"message": f"User updated"})
        return db_user
    except Exception as error:
        status, message = map_sqlalchemy_error(error)
        raise SQLErrorException(status, f'{message}')

def delete_user(db: DbSession, user_id: int) -> list[model.UserResponse]:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise SQLErrorException(404, "User not found")
    try:
        db.delete(db_user)
        db.commit()

        r.xadd("event-stream", {"message": f"User deleted"})
        
    except Exception as error:
        status, message = map_sqlalchemy_error(error)
        raise SQLErrorException(status, f'{message}')
    
    return db.query(User).all()
