from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from app.db.models.order import OrderStatus, PaymentStatus, PaymentMethod

class OrderItemBase(BaseModel):
    """Base schema for order items."""
    menu_item_id: str
    name: str
    quantity: int
    price: float
    
    @property
    def subtotal(self) -> float:
        return self.price * self.quantity
    
    @validator('quantity')
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Quantity must be positive')
        return v
    
    @validator('price')
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Price must be positive')
        return v

class OrderItem(OrderItemBase):
    """Schema for order item."""
    subtotal: float

class OrderBase(BaseModel):
    """Base schema for orders."""
    table_number: Optional[str] = None
    notes: Optional[str] = None

class OrderCreate(OrderBase):
    """Schema for creating a new order."""
    items: List[OrderItemBase]
    payment_method: PaymentMethod = PaymentMethod.CASH
    
    @validator('items')
    def items_not_empty(cls, v):
        if not v:
            raise ValueError('Order must have at least one item')
        return v

class OrderUpdate(BaseModel):
    """Schema for updating an order."""
    table_number: Optional[str] = None
    status: Optional[OrderStatus] = None
    payment_status: Optional[PaymentStatus] = None
    payment_method: Optional[PaymentMethod] = None
    notes: Optional[str] = None

class Order(OrderBase):
    """Schema for order response."""
    id: str = Field(..., alias="_id")
    user_id: str
    order_number: str
    items: List[OrderItem]
    subtotal: float
    tax: float
    discount: float
    total: float
    status: OrderStatus
    payment_status: PaymentStatus
    payment_method: PaymentMethod
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        populate_by_name = True
