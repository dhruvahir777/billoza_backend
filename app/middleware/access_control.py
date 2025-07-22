from fastapi import HTTPException, status
from bson import ObjectId

def verify_user_access(current_user, requested_user_id):
    """
    Verify that the current user has access to the requested user's resources.
    This prevents users from accessing other users' data.
    
    Args:
        current_user: The authenticated user document
        requested_user_id: The user ID being accessed in the request (BZU format)
        
    Raises:
        HTTPException: If the current user doesn't match the requested user ID
    """
    # Get the user_id (BZU format) from current user
    current_user_custom_id = current_user.get("user_id", "")
    
    # Check if the authenticated user is trying to access their own resources
    if current_user_custom_id != requested_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: You can only access your own resources"
        )
