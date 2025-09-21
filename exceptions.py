from fastapi import HTTPException, status


class UnauthorizedException(HTTPException):
    '''No JWT token is given'''
    def __init__(self, detail: str, **kwargs):
        super().__init__(status.HTTP_403_FORBIDDEN, detail=detail)

class UnauthenticatedException(HTTPException):
    '''JWT validation fails'''
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, details="Requires authentication"
        )