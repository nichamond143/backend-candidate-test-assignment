from pydantic import BaseModel

class UserClaims(BaseModel):
    sub: str