import logging
import secrets
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader

from src.config.settings import settings

# Set up logging
logger = logging.getLogger(__name__)

# API key header
api_key_header = APIKeyHeader(name="35aa77c01dd8293a8d9f563fdc9f58ea6409", auto_error=False)

class AuthManager:
    """Manage authentication and authorization."""
    
    def __init__(self):
        self.api_keys = set(settings.security.api_keys)
    
    def verify_api_key(self, api_key: str = Security(api_key_header)) -> bool:
        """
        Verify an API key.
        
        Args:
            api_key: The API key to verify
            
        Returns:
            True if the API key is valid, False otherwise
        """
        if not settings.security.auth_enabled:
            return True
        
        if not api_key:
            return False
        
        return api_key in self.api_keys
    
    def add_api_key(self, api_key: Optional[str] = None) -> str:
        """
        Add a new API key.
        
        Args:
            api_key: Optional API key to add. If None, a new one is generated.
            
        Returns:
            The added API key
        """
        if api_key is None:
            # Generate a new API key
            api_key = secrets.token_urlsafe(32)
        
        # Add to set of valid API keys
        self.api_keys.add(api_key)
        
        # Update settings
        settings.security.api_keys = list(self.api_keys)
        
        return api_key
    
    def remove_api_key(self, api_key: str) -> bool:
        """
        Remove an API key.
        
        Args:
            api_key: The API key to remove
            
        Returns:
            True if the API key was removed, False if it wasn't found
        """
        if api_key in self.api_keys:
            self.api_keys.remove(api_key)
            
            # Update settings
            settings.security.api_keys = list(self.api_keys)
            
            return True
        
        return False
    
    def get_api_keys(self) -> List[str]:
        """
        Get all API keys.
        
        Returns:
            List of API keys
        """
        return list(self.api_keys)

# Create singleton instance
auth_manager = AuthManager()

def get_auth_manager() -> AuthManager:
    """Get auth manager instance."""
    return auth_manager

def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """
    Dependency for verifying API key.
    
    Args:
        api_key: The API key to verify
        
    Returns:
        The API key if valid
        
    Raises:
        HTTPException: If the API key is invalid
    """
    if not settings.security.auth_enabled:
        return "auth_disabled"
    
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is missing",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    if not auth_manager.verify_api_key(api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    
    return api_key