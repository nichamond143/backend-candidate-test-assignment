from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    username: str
    email: str

# Pydantic model for request data
class UserCreate(UserBase):
    pass

# Pydantic model for response data
class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True

class UserUpdate(UserBase):
    name: Optional[str]
    username: Optional[str]
    email: Optional[str]