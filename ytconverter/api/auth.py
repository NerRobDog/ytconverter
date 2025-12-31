"""API key authentication for FastAPI endpoints."""

import os
from typing import Optional
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

# API key header scheme
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def get_api_keys() -> set:
    """
    Get valid API keys from environment variable.
    
    Returns:
        Set of valid API keys.
    """
    keys_env = os.environ.get("YTCONVERTER_API_KEYS", "")
    if not keys_env:
        # If no API keys configured, allow all requests (open mode)
        return set()
    return set(key.strip() for key in keys_env.split(",") if key.strip())


async def verify_api_key(api_key: Optional[str] = Security(api_key_header)) -> str:
    """
    Verify the API key from request headers.
    
    Args:
        api_key: API key from X-API-Key header
        
    Returns:
        The verified API key
        
    Raises:
        HTTPException: If API key is invalid or missing
    """
    valid_keys = get_api_keys()
    
    # If no keys configured, allow all requests
    if not valid_keys:
        return "open"
    
    # If keys are configured, validate
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key. Provide X-API-Key header.",
        )
    
    if api_key not in valid_keys:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key.",
        )
    
    return api_key
