from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, NoResultFound, DataError, StatementError, TimeoutError, DisconnectionError

class UnauthorizedException(HTTPException):
    '''No JWT token is given'''
    def __init__(self, detail: str, **kwargs):
        super().__init__(status.HTTP_403_FORBIDDEN, detail=detail)

class UnauthenticatedException(HTTPException):
    '''JWT validation fails'''
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=detail
        )

class SQLErrorException(HTTPException):
    '''SQLAlchemy Exceptions'''
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)
    
def map_sqlalchemy_error(error: Exception) -> tuple[int, str]:
    if isinstance(error, IntegrityError):
        return 409, "Conflict with existing data"
    elif isinstance(error, NoResultFound):
        return 404, "Resource doesn't exist"
    elif isinstance(error, DataError) or isinstance(error, StatementError):
        return 400, "Client sent invalid data"
    elif isinstance(error, TimeoutError):
        return 504, "DB didn't respond in time"
    elif isinstance(error, DisconnectionError):
        return 503, "Temporary DB outage"
    else:
        return 500, str(error)
        