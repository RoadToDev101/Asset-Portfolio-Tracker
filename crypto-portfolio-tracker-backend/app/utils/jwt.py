from fastapi import HTTPException, status
from jose import jwt
from datetime import datetime, timedelta
from typing import Optional
import os
from dotenv import load_dotenv
from uuid import UUID

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET")  # Import from environment variables for production
ALGORITHM = "HS256"


class TokenCreationError(Exception):
    pass


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    try:
        # Convert UUID to string for JWT
        to_encode = {k: (str(v) if isinstance(v, UUID) else v) for k, v in data.items()}

        # Set expiration time for token
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)

        to_encode.update({"exp": expire})  # Add expiration time to token

        encoded_jwt = jwt.encode(
            to_encode, SECRET_KEY, algorithm=ALGORITHM
        )  # Create token
        return encoded_jwt
    except Exception as e:
        raise TokenCreationError(f"Failed to create token: {e}")


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Failed to decode token"
        )
