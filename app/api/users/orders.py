from fastapi import APIRouter, Depends, HTTPException, Path, Query
from typing import List, Optional
from datetime import datetime, date
from app.middleware.auth_middleware import get_current_user
from app.middleware.access_control import verify_user_access
from app.schemas.order import Order, OrderCreate, OrderUpdate, OrderStatus
from app.services.order_service import (
    get_orders, 
    get_order, 
    create_order, 
    update_order,
    delete_order
)

router = APIRouter()

@router.get("/{user_id}/orders", response_model=List[Order])
async def read_orders(
    user_id: str = Path(...),
    status: Optional[OrderStatus] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user=Depends(get_current_user)
):
    """
    Get all orders for a specific user with optional filtering.
    """
    verify_user_access(current_user, user_id)
    
    filters = {}
    if status:
        filters["status"] = status
    if start_date:
        filters["start_date"] = start_date
    if end_date:
        filters["end_date"] = end_date
        
    orders = await get_orders(user_id, filters)
    return orders

@router.post("/{user_id}/orders", response_model=Order, status_code=201)
async def add_order(
    order: OrderCreate,
    user_id: str = Path(...),
    current_user=Depends(get_current_user)
):
    """
    Create a new order for a specific user.
    """
    verify_user_access(current_user, user_id)
    
    created_order = await create_order(user_id, order)
    return created_order

@router.get("/{user_id}/orders/{order_id}", response_model=Order)
async def read_order(
    order_id: str,
    user_id: str = Path(...),
    current_user=Depends(get_current_user)
):
    """
    Get a specific order.
    """
    verify_user_access(current_user, user_id)
    
    order = await get_order(user_id, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.put("/{user_id}/orders/{order_id}", response_model=Order)
async def edit_order(
    order: OrderUpdate,
    order_id: str,
    user_id: str = Path(...),
    current_user=Depends(get_current_user)
):
    """
    Update a specific order.
    """
    verify_user_access(current_user, user_id)
    
    updated_order = await update_order(user_id, order_id, order)
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order

@router.delete("/{user_id}/orders/{order_id}", status_code=204)
async def remove_order(
    order_id: str,
    user_id: str = Path(...),
    current_user=Depends(get_current_user)
):
    """
    Delete a specific order.
    """
    verify_user_access(current_user, user_id)
    
    success = await delete_order(user_id, order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
