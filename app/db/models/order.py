from datetime import datetime
from typing import List, Optional
from enum import Enum

# Order status enum
class OrderStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

# Payment status enum
class PaymentStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
    REFUNDED = "refunded"

# Payment method enum
class PaymentMethod(str, Enum):
    CASH = "cash"
    CARD = "card"
    UPI = "upi"
    WALLET = "wallet"

# Order item structure
order_item_schema = {
    "menu_item_id": str,
    "name": str,
    "quantity": int,
    "price": float,
    "subtotal": float
}

# MongoDB document structure for Order
order_model = {
    "user_id": str,
    "order_number": str,
    "customer_name": Optional[str],
    "customer_phone": Optional[str],
    "table_number": Optional[str],
    "items": List[dict],  # List of order_item_schema
    "subtotal": float,
    "tax": float,
    "discount": float,
    "total": float,
    "status": str,
    "payment_status": str,
    "payment_method": str,
    "notes": Optional[str],
    "created_at": datetime,
    "updated_at": datetime
}
