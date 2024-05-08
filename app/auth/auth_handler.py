import os
import time
from typing import Annotated, Dict
from fastapi import Header, HTTPException
import jwt
from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader

from app.auth.api_key import check_api_key, get_user_from_api_key


JWT_SECRET = os.getenv('JWT_SECRET')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')


api_key_header = APIKeyHeader(name="X-API-Key")

async def get_user(X_API_Key: Annotated[str, Header()]):
    if check_api_key(X_API_Key):
        user = get_user_from_api_key(X_API_Key)
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid API key"
    )

# def get_user1(api_key_header: str = Security(api_key_header)):
#     if check_api_key(api_key_header):
#         user = get_user_from_api_key(api_key_header)
#         return user
#     raise HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Missing or invalid API key"
#     )

###########################################
def token_response(token: str):
    return {
        "access_token": token
    }


def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM=JWT_ALGORITHM)

    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, JWT_ALGORITHMs=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return {}
    
# Function to verify the access token extracted from the request
def verify_access_token(request):
    # Extract the token from the request
    token = get_token_from_request(request)
    
    try:
        print("verify access token called")
        # Decode and verify the token using the secret key and JWT_ALGORITHM
        decoded_token = jwt.decode(token, JWT_SECRET, JWT_ALGORITHMs=[JWT_ALGORITHM])
        # return payload
        print("{} token is decoded ".format(decoded_token))
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except jwt.ExpiredSignatureError:
        # Raise an HTTPException with status code 401 if the token has expired
        print(">>>Token expired")
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        # Raise an HTTPException with status code 401 if the token is invalid
        print(">>>Invalid token")
        raise HTTPException(status_code=401, detail="Invalid token")
    
def get_token_from_request(request):
    # Extract the token from the request
    token = request.headers.get('Authorization')
    if not token:
        print(">>>Token not found")
        # Raise an HTTPException with status code 401 if the token is not found
        raise HTTPException(status_code=401, detail="Token not found")
    return token.replace("Bearer ", "")

def signJWT(user_id: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 600
    }
    token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM=JWT_ALGORITHM)

    return token_response(token)