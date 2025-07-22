from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import date, datetime
from enum import Enum

class ReportTimeFrame(str, Enum):
    """Time frame options for reports."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

class SalesDataPoint(BaseModel):
    """Data point for sales reports."""
    date: datetime
    orders_count: int
    items_sold: int

class SalesReport(BaseModel):
    """Schema for sales report response."""
    time_frame: ReportTimeFrame
    start_date: date
    end_date: date
    total_orders: int
    total_items_sold: int
    data: List[SalesDataPoint]

class RevenueDataPoint(BaseModel):
    """Data point for revenue reports."""
    date: datetime
    revenue: float
    tax: float
    discount: float
    net_amount: float

class RevenueReport(BaseModel):
    """Schema for revenue report response."""
    time_frame: ReportTimeFrame
    start_date: date
    end_date: date
    total_revenue: float
    total_tax: float
    total_discount: float
    total_net_amount: float
    data: List[RevenueDataPoint]

class CategorySalesData(BaseModel):
    """Data for category-wise sales report."""
    category: str
    items_sold: int
    revenue: float
    percentage: float

class CategorySalesReport(BaseModel):
    """Schema for category-wise sales report."""
    time_frame: ReportTimeFrame
    start_date: date
    end_date: date
    data: List[CategorySalesData]
