from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from app.middleware.auth_middleware import get_current_user
from app.schemas.user import UserProfile, UserProfileUpdate
from app.services.user_service import (
    get_user_profile,
    update_user_profile,
    update_profile_image,
)

router = APIRouter()


@router.get("/profile", response_model=UserProfile)
async def read_user_profile(current_user=Depends(get_current_user)):
    """
    Get the profile for the currently authenticated user.
    """
    user = await get_user_profile(str(current_user["_id"]))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/profile", response_model=UserProfile)
async def update_profile(
    profile_update: UserProfileUpdate,
    current_user=Depends(get_current_user),
):
    """
    Update the profile for the currently authenticated user.
    """
    updated_user = await update_user_profile(
        user_id=str(current_user["_id"]),
        profile_data=profile_update,
    )
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user


@router.put("/profile/image", response_model=UserProfile)
async def update_profile_image_endpoint(
    file: UploadFile = File(...), current_user=Depends(get_current_user)
):
    """
    Update the profile image for the currently authenticated user.
    """
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    updated_user = await update_profile_image(
        user_id=str(current_user["_id"]),
        file=file,
    )
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user
