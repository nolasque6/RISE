import os
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

secret_key = os.getenv("JWT_SECRET_KEY", "your_secret_key")
algorithm = "HS256"
Token_expires_in_minutes = 60

security = HTTPBearer()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)    

def create_token(user_id: str) -> str:
    expiration = datetime.now(timezone.utc) + timedelta(minutes=Token_expires_in_minutes)
    data = {"sub": user_id, "exp": expiration}
    return jwt.encode(data, secret_key, algorithm=algorithm)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    token = credentials.credentials
    try:
        data = jwt.decode(token, secret_key, algorithms=[algorithm])
        user_id = data.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )
        return user_id

    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )