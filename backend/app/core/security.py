import time
import json
import base64
import hmac
import hashlib
from typing import Optional, Dict, Any
import bcrypt
from backend.app.core.config import settings

def _base64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')

def _base64url_decode(data: str) -> bytes:
    padding = '=' * (4 - len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a bcrypt hashed password."""
    try:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except Exception:
        return False

def hash_password(password: str) -> str:
    """Hashes a password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def create_access_token(data: Dict[str, Any], expires_delta: Optional[int] = None) -> str:
    """Creates an HMAC-SHA256 JWT access token."""
    header = {"alg": settings.JWT_ALGORITHM, "typ": "JWT"}
    payload = data.copy()
    
    expire_seconds = (expires_delta if expires_delta is not None else settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    now = int(time.time())
    payload["iat"] = now
    payload["exp"] = now + expire_seconds
    
    header_bytes = json.dumps(header, separators=(',', ':')).encode('utf-8')
    payload_bytes = json.dumps(payload, separators=(',', ':')).encode('utf-8')
    
    encoded_header = _base64url_encode(header_bytes)
    encoded_payload = _base64url_encode(payload_bytes)
    
    signing_input = f"{encoded_header}.{encoded_payload}".encode('utf-8')
    signature = hmac.new(settings.JWT_SECRET_KEY.encode('utf-8'), signing_input, hashlib.sha256).digest()
    encoded_signature = _base64url_encode(signature)
    
    return f"{encoded_header}.{encoded_payload}.{encoded_signature}"

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Decodes and verifies an HMAC-SHA256 JWT token."""
    try:
        parts = token.split('.')
        if len(parts) != 3:
            return None
        encoded_header, encoded_payload, encoded_signature = parts
        
        # Verify signature
        signing_input = f"{encoded_header}.{encoded_payload}".encode('utf-8')
        expected_sig = hmac.new(settings.JWT_SECRET_KEY.encode('utf-8'), signing_input, hashlib.sha256).digest()
        actual_sig = _base64url_decode(encoded_signature)
        
        if not hmac.compare_digest(expected_sig, actual_sig):
            return None
            
        # Parse payload
        payload_bytes = _base64url_decode(encoded_payload)
        payload = json.loads(payload_bytes.decode('utf-8'))
        
        # Check expiration
        now = int(time.time())
        if payload.get("exp") and payload["exp"] < now:
            return None
            
        return payload
    except Exception:
        return None
