import base64
import hashlib
import time
from fastapi import HTTPException, Request
from typing import Tuple

def decode_basic_auth(auth_header: str) -> Tuple[str, str]:
    try:
        # Remove 'Basic ' prefix and decode
        encoded_credentials = auth_header.split(' ')[1]
        decoded = base64.b64decode(encoded_credentials).decode('utf-8')
        username, password = decoded.split(':')
        return username, password
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

def generate_token(username: str, ip_address: str) -> str:
    # Generate a token using username, IP and timestamp
    timestamp = str(int(time.time()))
    token_string = f"{username}{ip_address}{timestamp}"
    return hashlib.md5(token_string.encode()).hexdigest()