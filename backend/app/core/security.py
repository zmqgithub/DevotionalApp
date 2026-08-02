from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
import bcrypt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from app.core.config import settings

# Password hashing with passlib (which handles bcrypt internally)
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password using passlib"""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(f"Password verification error: {e}")
        return False


def get_password_hash(password: str) -> str:
    """Hash a password using passlib with bcrypt"""
    try:
        return pwd_context.hash(password)
    except Exception as e:
        print(f"Password hashing error: {e}")
        raise ValueError(f"Failed to hash password: {str(e)}")


def create_access_token(user_id: int, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {
        "sub": str(user_id),
        "exp": expire,
        "type": "access"
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(user_id: int, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT refresh token"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode = {
        "sub": str(user_id),
        "exp": expire,
        "type": "refresh"
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify a JWT token and return the payload"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None


def verify_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify an access token"""
    payload = verify_token(token)
    if not payload or payload.get("type") != "access":
        return None
    return payload


def verify_refresh_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify a refresh token"""
    payload = verify_token(token)
    if not payload or payload.get("type") != "refresh":
        return None
    return payload


def get_token_payload(token: str) -> Dict[str, Any]:
    """Get token payload or raise exception"""
    payload = verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload


def get_current_user_id(token: str) -> int:
    """Extract user ID from token"""
    payload = get_token_payload(token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return int(user_id)


def is_token_expired(token: str) -> bool:
    """Check if a token is expired"""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_exp": True}
        )
        return False
    except JWTError:
        return True


def create_reset_password_token(email: str) -> str:
    """Create a password reset token"""
    expire = datetime.utcnow() + timedelta(hours=settings.PASSWORD_RESET_EXPIRE_HOURS)
    to_encode = {
        "sub": email,
        "exp": expire,
        "type": "reset_password"
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_reset_password_token(token: str) -> Optional[str]:
    """Verify a password reset token and return the email"""
    payload = verify_token(token)
    if not payload or payload.get("type") != "reset_password":
        return None
    return payload.get("sub")


def create_verification_token(email: str) -> str:
    """Create an email verification token"""
    expire = datetime.utcnow() + timedelta(days=settings.EMAIL_VERIFICATION_EXPIRE_DAYS)
    to_encode = {
        "sub": email,
        "exp": expire,
        "type": "email_verification"
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_verification_token(token: str) -> Optional[str]:
    """Verify an email verification token and return the email"""
    payload = verify_token(token)
    if not payload or payload.get("type") != "email_verification":
        return None
    return payload.get("sub")


def generate_api_key() -> str:
    """Generate a secure API key"""
    import secrets
    return secrets.token_urlsafe(32)


def hash_api_key(api_key: str) -> str:
    """Hash an API key using passlib"""
    return pwd_context.hash(api_key)


def verify_api_key(plain_api_key: str, hashed_api_key: str) -> bool:
    """Verify an API key"""
    try:
        return pwd_context.verify(plain_api_key, hashed_api_key)
    except Exception:
        return False