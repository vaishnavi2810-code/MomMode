"""
Auth API Routes

All /api/auth/* endpoints for OAuth handling.
"""

from typing import Optional
from urllib.parse import quote
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import RedirectResponse

from src.core.auth import auth_manager
from src.api.schemas.calendar import CalendarAuthResponse

router = APIRouter(prefix="/api/auth", tags=["Auth"])


@router.get("/google/callback")
def handle_google_callback(code: str = Query(...), state: Optional[str] = Query(None)):
    """
    Handle OAuth callback from Google (redirect endpoint).
    This endpoint matches the redirect URI configured in Google Cloud Console.
    After successful authentication, redirects to the frontend.
    """
    success, message, email = auth_manager.handle_callback(code)
    
    if not success:
        # Redirect to frontend with error (URL encode the message)
        error_msg = quote(message)
        return RedirectResponse(
            url=f"/connect-calendar?error={error_msg}",
            status_code=307
        )
    
    # Redirect to frontend with success
    return RedirectResponse(
        url=f"/connect-calendar?success=true&email={quote(email) if email else ''}",
        status_code=307
    )
