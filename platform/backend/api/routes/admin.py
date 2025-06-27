"""
Admin panel routes for system management.
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/dashboard")
async def admin_dashboard():
    """Get admin dashboard data."""
    return {"message": "Admin dashboard endpoint - TODO"}

@router.get("/streams")
async def admin_streams():
    """Get all streams for admin management."""
    return {"message": "Admin streams endpoint - TODO"}

@router.get("/users")
async def admin_users():
    """Get all users for admin management."""
    return {"message": "Admin users endpoint - TODO"} 