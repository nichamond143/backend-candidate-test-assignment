from typing import List, Optional
from pydantic import BaseModel

from posts.model import PostResponse

class UserBase(BaseModel):
    name: str
    username: str
    email: str

# Pydantic model for request data
class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    name: Optional[str]
    username: Optional[str]
    email: Optional[str]

# Pydantic model for response data
class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserDetailResponse(UserResponse):
    posts: List[PostResponse]