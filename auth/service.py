from typing import Annotated
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import requests
from jose import jwt, jws, jwk
from fastapi import Depends
from exceptions import UnauthorizedException, UnauthenticatedException

from config import get_settings
from . import model

config = get_settings()
token_auth_scheme = HTTPBearer()


def login() -> RedirectResponse:
    return RedirectResponse(
        f"https://{config.auth0_domain}/authorize"
        "?response_type=code"
        f"&client_id={config.auth0_client_id}"
        "&redirect_uri=http://127.0.0.1:8000/auth/token"
        f"&audience={config.auth0_api_audience}"
    )


def get_access_token(code: str) -> dict:
    payload = (
        "grant_type=authorization_code"
        f"&client_id={config.auth0_client_id}"
        f"&client_secret={config.auth0_client_secret}"
        f"&code={code}"
        f"&redirect_uri=http://127.0.0.1:8000/auth/token"
    )
    headers = {"content-type": "application/x-www-form-urlencoded"}
    response = requests.post(
        f"https://{config.auth0_domain}/oauth/token",
        data=payload,
        headers=headers
    )
    return response.json()


def get_jwks():
    """Fetch latest JWKS (Auth0 rotates keys periodically)."""
    jwks_endpoint = f"https://{config.auth0_domain}/.well-known/jwks.json"
    return requests.get(jwks_endpoint).json()["keys"]


def find_public_key(kid: str):
    for key in get_jwks():
        if key["kid"] == kid:
            return key
    return None


def validate(
    token: Annotated[HTTPAuthorizationCredentials, Depends(token_auth_scheme)]
):
    if token is None:
        raise UnauthorizedException("No token provided")

    try:
        # extract unverified header
        unverified_token = jws.get_unverified_header(token.credentials)

        # find correct key
        public_key = find_public_key(unverified_token["kid"])
        if public_key is None:
            raise UnauthorizedException("Public Key not Found")

        # construct usable JWK
        key = jwk.construct(public_key)

        # verify + decode
        payload = jwt.decode(
            token.credentials,
            key,
            algorithms=["RS256"],
            audience=config.auth0_api_audience,
            issuer=config.auth0_issuer,
        )

        return model.UserClaims(sub=payload["sub"])

    except (
        jwt.ExpiredSignatureError,
        jwt.JWTError,
        jwt.JWTClaimsError,
        jwt.JWSError
    ):
        raise UnauthenticatedException("Invalid or expired token")
