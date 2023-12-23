from jose import jwt
from datetime import datetime, timedelta
from typing import Optional
import os
from dotenv import load_dotenv
from uuid import UUID

load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET")  # Import from environment variables for production
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    # Convert UUID to string for JWT
    to_encode = {k: (str(v) if isinstance(v, UUID) else v) for k, v in data.items()}

    # Set expiration time for token
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})  # Add expiration time to token

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Create token
    return encoded_jwt


def decode_access_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return payload
