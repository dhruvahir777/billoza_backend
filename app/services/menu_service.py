from app.db.connection import db
from bson import ObjectId
from app.schemas.menu import MenuItemCreate, MenuItemUpdate
from datetime import datetime
from typing import Optional, Dict, Any, List
from app.utils.image_upload import save_upload_file, delete_file
from fastapi import UploadFile
from app.db.models.menu import FoodCategory

def serialize_menu_item(item):
    if not item:
        return None
    item["_id"] = str(item["_id"])
    item["id"] = item["_id"]  # Always include 'id' for frontend
    if "category" in item and not isinstance(item["category"], FoodCategory):
        try:
            item["category"] = FoodCategory(item["category"])
        except Exception:
            pass
    return item

async def get_menu_items(user_id: str) -> List[Dict[str, Any]]:
    """
    Get all menu items for a user.
    
    Args:
        user_id: The user's ID
        
    Returns:
        List[dict]: The menu items
    """
    if db.menu_items is None:
        return []
    
    try:
        cursor = db.menu_items.find({"user_id": user_id})
        items = await cursor.to_list(length=None)
        return [serialize_menu_item(i) for i in items]
    except Exception:
        return []

async def get_menu_item(user_id: str, item_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a specific menu item.
    
    Args:
        user_id: The user's ID
        item_id: The menu item's ID
        
    Returns:
        dict: The menu item if found, None otherwise
    """
    if db.menu_items is None:
        return None
    
    try:
        item_id_obj = ObjectId(item_id)
        item = await db.menu_items.find_one({"_id": item_id_obj, "user_id": user_id})
        return serialize_menu_item(item)
    except Exception:
        return None

async def create_menu_item(user_id: str, item_data: MenuItemCreate) -> Dict[str, Any]:
    """
    Create a new menu item.
    
    Args:
        user_id: The user's ID
        item_data: The menu item data
        
    Returns:
        dict: The created menu item
    """
    if db.menu_items is None:
        # This should not happen in production
        raise Exception("Database not initialized")
    
    # Prepare menu item document
    now = datetime.utcnow()
    item_doc = {
        "user_id": user_id,
        "name": item_data.name,
        "price": item_data.price,
        "description": item_data.description,
        "category": item_data.category.value,  # Ensure category is stored as string
        "image": None,
        "is_vegetarian": item_data.is_vegetarian,
        "is_available": item_data.is_available,
        "created_at": now,
        "updated_at": now
    }
    
    # Insert menu item
    result = await db.menu_items.insert_one(item_doc)
    
    # Get the inserted menu item
    item = await db.menu_items.find_one({"_id": result.inserted_id})
    return serialize_menu_item(item)

async def update_menu_item(user_id: str, item_id: str, item_data: MenuItemUpdate) -> Optional[Dict[str, Any]]:
    """
    Update a menu item.
    
    Args:
        user_id: The user's ID
        item_id: The menu item's ID
        item_data: The menu item data to update
        
    Returns:
        dict: The updated menu item if found, None otherwise
    """
    if db.menu_items is None:
        return None
    
    try:
        item_id_obj = ObjectId(item_id)
        
        # Prepare update document
        update_data = {}
        for field, value in item_data.dict(exclude_unset=True).items():
            if value is not None:
                if field == "category" and hasattr(value, "value"):
                    update_data[field] = value.value
                else:
                    update_data[field] = value

        # Add updated_at timestamp
        update_data["updated_at"] = datetime.utcnow()
        
        # Update menu item
        result = await db.menu_items.update_one(
            {"_id": item_id_obj, "user_id": user_id},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            return None
        
        # Get the updated menu item
        updated_item = await db.menu_items.find_one({"_id": item_id_obj})
        return serialize_menu_item(updated_item)
    except Exception:
        return None

async def delete_menu_item(user_id: str, item_id: str) -> bool:
    """
    Delete a menu item.
    
    Args:
        user_id: The user's ID
        item_id: The menu item's ID
        
    Returns:
        bool: True if deleted, False otherwise
    """
    if db.menu_items is None:
        return False
    
    try:
        item_id_obj = ObjectId(item_id)
        
        # Get the menu item first to delete the image if exists
        item = await db.menu_items.find_one({"_id": item_id_obj, "user_id": user_id})
        if not item:
            return False
        
        # Delete the image if exists
        if item.get("image"):
            delete_file(item["image"])
        
        # Delete the menu item
        result = await db.menu_items.delete_one({"_id": item_id_obj, "user_id": user_id})
        return result.deleted_count > 0
    except Exception:
        return False

async def update_menu_item_image(user_id: str, item_id: str, file: UploadFile) -> Optional[Dict[str, Any]]:
    """
    Update a menu item's image.
    
    Args:
        user_id: The user's ID
        item_id: The menu item's ID
        file: The uploaded file
        
    Returns:
        dict: The updated menu item if found, None otherwise
    """
    if db.menu_items is None:
        return None
    
    try:
        item_id_obj = ObjectId(item_id)
        
        # Get the current menu item
        item = await db.menu_items.find_one({"_id": item_id_obj, "user_id": user_id})
        if not item:
            return None
        
        # Delete old image if exists
        if item.get("image"):
            delete_file(item["image"])
        
        # Save new image
        file_path = await save_upload_file(file, "menu")
        
        # Update menu item with new image
        await db.menu_items.update_one(
            {"_id": item_id_obj, "user_id": user_id},
            {
                "$set": {
                    "image": file_path,
                    "updated_at": datetime.utcnow()
                }
            }
        )
        
        # Get the updated menu item
        updated_item = await db.menu_items.find_one({"_id": item_id_obj})
        return updated_item
    except Exception:
        return None
