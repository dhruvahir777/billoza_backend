from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from app.db.models.menu import FoodCategory

class MenuItemBase(BaseModel):
    """Base schema for menu items."""
    name: str
    price: float
    description: str
    category: FoodCategory
    is_vegetarian: bool = False
    is_available: bool = True
    
    @validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        return v

class MenuItemCreate(MenuItemBase):
    """Schema for creating a new menu item."""
    pass

class MenuItemUpdate(BaseModel):
    """Schema for updating a menu item."""
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    category: Optional[FoodCategory] = None
    is_vegetarian: Optional[bool] = None
    is_available: Optional[bool] = None
    
    @validator('price')
    def price_must_be_positive(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Price must be positive')
        return v

class MenuItem(MenuItemBase):
    """Schema for menu item response."""
    id: str = Field(..., alias="_id")
    user_id: str
    image: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        populate_by_name = True
