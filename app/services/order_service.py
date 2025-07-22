from app.db.connection import db
from bson import ObjectId
from app.schemas.order import OrderCreate, OrderUpdate, OrderStatus, PaymentStatus
from datetime import datetime
from typing import Optional, Dict, Any, List
import uuid

async def get_orders(user_id: str, filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    """
    Get all orders for a user with optional filtering.
    
    Args:
        user_id: The user's ID
        filters: Optional filters (status, date range, etc.)
        
    Returns:
        List[dict]: The orders
    """
    if db.orders is None:
        return []
    
    try:
        # Start with the base query
        query = {"user_id": user_id}
        
        # Add filters if provided
        if filters:
            if "status" in filters:
                query["status"] = filters["status"]
            
            if "start_date" in filters:
                if "created_at" not in query:
                    query["created_at"] = {}
                query["created_at"]["$gte"] = datetime.combine(filters["start_date"], datetime.min.time())
            
            if "end_date" in filters:
                if "created_at" not in query:
                    query["created_at"] = {}
                query["created_at"]["$lte"] = datetime.combine(filters["end_date"], datetime.max.time())
        
        # Execute query
        cursor = db.orders.find(query).sort("created_at", -1)  # Sort by created_at desc
        orders = await cursor.to_list(length=None)
        return orders
    except Exception as e:
        print(f"Error getting orders: {str(e)}")
        return []

async def get_order(user_id: str, order_id: str) -> Optional[Dict[str, Any]]:
    """
    Get a specific order.
    
    Args:
        user_id: The user's ID
        order_id: The order's ID
        
    Returns:
        dict: The order if found, None otherwise
    """
    if db.orders is None:
        return None
    
    try:
        order_id_obj = ObjectId(order_id)
        order = await db.orders.find_one({"_id": order_id_obj, "user_id": user_id})
        return order
    except Exception:
        return None

async def create_order(user_id: str, order_data: OrderCreate) -> Dict[str, Any]:
    """
    Create a new order.
    
    Args:
        user_id: The user's ID
        order_data: The order data
        
    Returns:
        dict: The created order
    """
    if db.orders is None:
        # This should not happen in production
        raise Exception("Database not initialized")
    
    # Calculate financial data
    items = []
    subtotal = 0.0
    
    for item in order_data.items:
        item_dict = item.dict()
        item_subtotal = item.price * item.quantity
        item_dict["subtotal"] = item_subtotal
        items.append(item_dict)
        subtotal += item_subtotal
    
    # Apply tax (assuming 10% tax rate)
    tax = round(subtotal * 0.1, 2)
    
    # Apply discount (can be updated later)
    discount = 0.0
    
    # Calculate total
    total = subtotal + tax - discount
    
    # Generate order number (format: YYYYMMDD-XXXX)
    now = datetime.utcnow()
    date_part = now.strftime("%Y%m%d")
    random_part = str(uuid.uuid4().int)[:4]
    order_number = f"{date_part}-{random_part}"
    
    # Prepare order document
    order_doc = {
        "user_id": user_id,
        "order_number": order_number,
        "customer_name": order_data.customer_name,
        "customer_phone": order_data.customer_phone,
        "table_number": order_data.table_number,
        "items": items,
        "subtotal": subtotal,
        "tax": tax,
        "discount": discount,
        "total": total,
        "status": OrderStatus.PENDING,
        "payment_status": PaymentStatus.PENDING,
        "payment_method": order_data.payment_method,
        "notes": order_data.notes,
        "created_at": now,
        "updated_at": now
    }
    
    # Insert order
    result = await db.orders.insert_one(order_doc)
    
    # Get the inserted order
    order = await db.orders.find_one({"_id": result.inserted_id})
    return order

async def update_order(user_id: str, order_id: str, order_data: OrderUpdate) -> Optional[Dict[str, Any]]:
    """
    Update an order.
    
    Args:
        user_id: The user's ID
        order_id: The order's ID
        order_data: The order data to update
        
    Returns:
        dict: The updated order if found, None otherwise
    """
    if db.orders is None:
        return None
    
    try:
        order_id_obj = ObjectId(order_id)
        
        # Prepare update document
        update_data = {}
        for field, value in order_data.dict(exclude_unset=True).items():
            if value is not None:
                update_data[field] = value
        
        # Add updated_at timestamp
        update_data["updated_at"] = datetime.utcnow()
        
        # Update order
        result = await db.orders.update_one(
            {"_id": order_id_obj, "user_id": user_id},
            {"$set": update_data}
        )
        
        if result.modified_count == 0:
            return None
        
        # Get the updated order
        updated_order = await db.orders.find_one({"_id": order_id_obj})
        return updated_order
    except Exception:
        return None

async def delete_order(user_id: str, order_id: str) -> bool:
    """
    Delete an order.
    
    Args:
        user_id: The user's ID
        order_id: The order's ID
        
    Returns:
        bool: True if deleted, False otherwise
    """
    if db.orders is None:
        return False
    
    try:
        order_id_obj = ObjectId(order_id)
        result = await db.orders.delete_one({"_id": order_id_obj, "user_id": user_id})
        return result.deleted_count > 0
    except Exception:
        return False
