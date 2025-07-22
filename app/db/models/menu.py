from datetime import datetime
from typing import List, Optional
from enum import Enum

# Food category enum
class FoodCategory(str, Enum):
    APPETIZER = "appetizer"
    MAIN = "main"
    DESSERT = "dessert"
    BEVERAGE = "beverage"
    SIDE = "side"
    DRINK = "drink"  # Drink category added

# MongoDB document structure for Menu Item
menu_item_model = {
    "user_id": str,
    "name": str,
    "price": float,
    "description": str,
    "category": str,
    "image": Optional[str],
    "is_vegetarian": bool,
    "is_available": bool,
    "created_at": datetime,
    "updated_at": datetime
}
