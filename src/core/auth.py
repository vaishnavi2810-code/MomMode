"""
Google OAuth authentication handling.
"""

import os
import json
from typing import Optional, Tuple
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from src import config

# Named constants (can be overridden via environment variables)
DEFAULT_TOKEN_FILE = "./token.json"


class GoogleAuthManager:
    """Manages Google OAuth authentication."""

    def __init__(self):
        # Use old environment variable names for compatibility
        self.client_id = os.getenv("GOOGLE_OAUTH_CLIENT_ID", "")
        self.client_secret = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET", "")
        self.redirect_uri = os.getenv("GOOGLE_REDIRECT_URI", "")

        # Validate required fields
        if not self.redirect_uri:
            raise ValueError("GOOGLE_REDIRECT_URI environment variable is required")

        # Parse scopes from comma or space-separated string
        scopes_str = os.getenv("GOOGLE_OAUTH_SCOPES", "")
        if scopes_str:
            # Handle both comma and space-separated formats
            self.scopes = [s.strip() for s in scopes_str.replace(",", " ").split() if s.strip()]
        else:
            raise ValueError("GOOGLE_OAUTH_SCOPES environment variable is required")

        # Token file uses DEFAULT_TOKEN_FILE constant (can be overridden via env var)
        self.token_file = os.getenv("GOOGLE_TOKEN_FILE", DEFAULT_TOKEN_FILE)
    
    def get_auth_url(self) -> str:
        """
        Generate Google OAuth authorization URL.

        Returns:
            Authorization URL to redirect user to
        """
        print(f"[GOOGLE AUTH] get_auth_url() called")
        print(f"[GOOGLE AUTH]   client_id: {self.client_id[:20] if self.client_id else 'MISSING'}...")
        print(f"[GOOGLE AUTH]   client_secret: {self.client_secret[:20] if self.client_secret else 'MISSING'}...")
        print(f"[GOOGLE AUTH]   redirect_uri: {self.redirect_uri}")
        print(f"[GOOGLE AUTH]   scopes: {self.scopes}")

        flow = Flow.from_client_config(
            client_config={
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "redirect_uris": [self.redirect_uri]
                }
            },
            scopes=self.scopes
        )
        flow.redirect_uri = self.redirect_uri

        auth_url, state = flow.authorization_url(
            access_type="offline",
            include_granted_scopes="true",
            prompt="consent"
        )

        print(f"[GOOGLE AUTH] ✅ Auth URL generated")
        print(f"[GOOGLE AUTH]   Auth URL: {auth_url}")
        print(f"[GOOGLE AUTH]   State: {state}")

        return auth_url
    
    def handle_callback(self, code: str) -> Tuple[bool, str, Optional[str]]:
        """
        Handle OAuth callback and exchange code for tokens.
        
        Args:
            code: Authorization code from Google
            
        Returns:
            Tuple of (success, message, email)
        """
        try:
            flow = Flow.from_client_config(
                client_config={
                    "web": {
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                        "token_uri": "https://oauth2.googleapis.com/token",
                        "redirect_uris": [self.redirect_uri]
                    }
                },
                scopes=self.scopes
            )
            flow.redirect_uri = self.redirect_uri
            
            # Exchange code for tokens
            flow.fetch_token(code=code)
            credentials = flow.credentials
            
            # Save tokens
            self._save_tokens(credentials)
            
            # Get user email
            email = self._get_user_email(credentials)
            
            return True, "Successfully connected to Google Calendar", email
            
        except Exception as e:
            return False, f"Authentication failed: {str(e)}", None
    
    def get_credentials(self) -> Optional[Credentials]:
        """
        Get valid credentials from stored token.
        
        Returns:
            Valid Credentials object or None if not authenticated
        """
        if not os.path.exists(self.token_file):
            return None
        
        try:
            credentials = Credentials.from_authorized_user_file(
                self.token_file, 
                self.scopes
            )
            
            # Refresh if expired
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
                self._save_tokens(credentials)
            
            # Check if valid
            if credentials and credentials.valid:
                return credentials
                
            return None
            
        except Exception:
            return None
    
    def is_authenticated(self) -> bool:
        """Check if we have valid credentials."""
        return self.get_credentials() is not None
    
    def get_calendar_service(self):
        """
        Get authenticated Google Calendar service.
        
        Returns:
            Google Calendar API service or None
        """
        credentials = self.get_credentials()
        if not credentials:
            return None
        
        return build("calendar", "v3", credentials=credentials)
    
    def get_status(self) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Get current authentication status.
        
        Returns:
            Tuple of (connected, email, calendar_id)
        """
        credentials = self.get_credentials()
        if not credentials:
            return False, None, None
        
        email = self._get_user_email(credentials)
        return True, email, "primary"
    
    def disconnect(self) -> Tuple[bool, str]:
        """
        Disconnect by removing stored tokens.
        
        Returns:
            Tuple of (success, message)
        """
        try:
            if os.path.exists(self.token_file):
                os.remove(self.token_file)
            return True, "Successfully disconnected from Google Calendar"
        except Exception as e:
            return False, f"Failed to disconnect: {str(e)}"
    
    def _save_tokens(self, credentials: Credentials) -> None:
        """Save credentials to token file."""
        token_data = {
            "token": credentials.token,
            "refresh_token": credentials.refresh_token,
            "token_uri": credentials.token_uri,
            "client_id": credentials.client_id,
            "client_secret": credentials.client_secret,
            "scopes": credentials.scopes
        }
        
        with open(self.token_file, "w") as f:
            json.dump(token_data, f)
    
    def _get_user_email(self, credentials: Credentials) -> Optional[str]:
        """Get user email from credentials."""
        try:
            service = build("oauth2", "v2", credentials=credentials)
            user_info = service.userinfo().get().execute()
            return user_info.get("email")
        except Exception:
            return None


# Global auth manager instance
auth_manager = GoogleAuthManager()