from typing import Optional
from pydantic import BaseModel

class PostBase(BaseModel):
    user_id: int
    description: str

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int

    class Config:
        from_attributes = True

class PostUpdate(BaseModel):
    description: Optional[str]