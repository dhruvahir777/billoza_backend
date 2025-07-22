from fastapi import APIRouter, Depends, HTTPException, Path
from typing import List
from app.middleware.auth_middleware import get_current_user
from app.middleware.access_control import verify_user_access
from app.schemas.menu import MenuItem, MenuItemCreate, MenuItemUpdate
from app.services.menu_service import (
    get_menu_items, 
    get_menu_item, 
    create_menu_item, 
    update_menu_item,
    delete_menu_item
)
from bson import ObjectId

router = APIRouter()

@router.get("/{user_id}/menu", response_model=List[MenuItem])
async def read_menu_items(
    user_id: str = Path(...),
    current_user=Depends(get_current_user)
):
    """
    Get all menu items for a specific user.
    """
    verify_user_access(current_user, user_id)
    
    items = await get_menu_items(user_id)
    return items

@router.post("/{user_id}/menu", response_model=MenuItem, status_code=201)
async def add_menu_item(
    item: MenuItemCreate,
    user_id: str = Path(...),
    current_user=Depends(get_current_user)
):
    """
    Add a new menu item for a specific user.
    """
    verify_user_access(current_user, user_id)
    
    created_item = await create_menu_item(user_id, item)
    return created_item

@router.get("/{user_id}/menu/{item_id}", response_model=MenuItem)
async def read_menu_item(
    item_id: str,
    user_id: str = Path(...),
    current_user=Depends(get_current_user)
):
    """
    Get a specific menu item.
    """
    verify_user_access(current_user, user_id)
    
    item = await get_menu_item(user_id, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item

@router.put("/{user_id}/menu/{item_id}", response_model=MenuItem)
async def edit_menu_item(
    item: MenuItemUpdate,
    item_id: str,
    user_id: str = Path(...),
    current_user=Depends(get_current_user)
):
    """
    Update a specific menu item.
    """
    verify_user_access(current_user, user_id)
    
    updated_item = await update_menu_item(user_id, item_id, item)
    if not updated_item:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return updated_item

@router.delete("/{user_id}/menu/{item_id}", status_code=204)
async def remove_menu_item(
    item_id: str,
    user_id: str = Path(...),
    current_user=Depends(get_current_user)
):
    """
    Delete a specific menu item.
    """
    verify_user_access(current_user, user_id)
    
    success = await delete_menu_item(user_id, item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Menu item not found")
