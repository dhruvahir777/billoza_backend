from app.db.connection import db
from app.schemas.report import ReportTimeFrame, SalesReport, RevenueReport
from app.utils.date_utils import get_date_range, format_date_for_timeframe
from datetime import datetime, date, timedelta
from typing import Dict, Any, List, Optional
from bson import ObjectId

async def generate_sales_report(
    user_id: str,
    time_frame: ReportTimeFrame,
    start_date: date,
    end_date: Optional[date] = None
) -> SalesReport:
    """
    Generate a sales report.
    
    Args:
        user_id: The user's ID
        time_frame: The time frame (daily, weekly, monthly, yearly)
        start_date: The start date
        end_date: The end date (optional)
        
    Returns:
        SalesReport: The sales report
    """
    if db.orders is None:
        # Return empty report if DB not initialized
        return SalesReport(
            time_frame=time_frame,
            start_date=start_date,
            end_date=end_date or start_date,
            total_orders=0,
            total_items_sold=0,
            data=[]
        )
    
    # Get date range
    start, end = get_date_range(time_frame, start_date, end_date)
    
    # Convert to datetime for query
    start_datetime = datetime.combine(start, datetime.min.time())
    end_datetime = datetime.combine(end, datetime.max.time())
    
    # Query orders within date range
    orders = await db.orders.find({
        "user_id": user_id,
        "created_at": {
            "$gte": start_datetime,
            "$lte": end_datetime
        }
    }).to_list(length=None)
    
    # Calculate total orders and items sold
    total_orders = len(orders)
    total_items_sold = sum(sum(item["quantity"] for item in order["items"]) for order in orders)
    
    # Group data by time frame
    data_points = []
    
    if time_frame == ReportTimeFrame.DAILY:
        # For daily reports, we show each day
        current_date = start
        while current_date <= end:
            current_start = datetime.combine(current_date, datetime.min.time())
            current_end = datetime.combine(current_date, datetime.max.time())
            
            # Filter orders for current day
            day_orders = [o for o in orders if current_start <= o["created_at"] <= current_end]
            
            # Calculate data for current day
            orders_count = len(day_orders)
            items_sold = sum(sum(item["quantity"] for item in order["items"]) for order in day_orders)
            
            # Add data point
            data_points.append({
                "date": current_start,
                "orders_count": orders_count,
                "items_sold": items_sold
            })
            
            # Move to next day
            current_date += timedelta(days=1)
    
    elif time_frame == ReportTimeFrame.WEEKLY:
        # For weekly reports, we group by week
        week_data = {}
        
        for order in orders:
            order_date = order["created_at"].date()
            week_num = order_date.isocalendar()[1]
            week_year = order_date.year
            week_key = f"{week_year}-{week_num}"
            
            if week_key not in week_data:
                week_data[week_key] = {
                    "date": datetime.combine(order_date, datetime.min.time()),
                    "orders_count": 0,
                    "items_sold": 0
                }
            
            week_data[week_key]["orders_count"] += 1
            week_data[week_key]["items_sold"] += sum(item["quantity"] for item in order["items"])
        
        # Convert to list and sort by date
        data_points = sorted(week_data.values(), key=lambda x: x["date"])
    
    elif time_frame == ReportTimeFrame.MONTHLY:
        # For monthly reports, we group by month
        month_data = {}
        
        for order in orders:
            order_date = order["created_at"].date()
            month_key = f"{order_date.year}-{order_date.month}"
            
            if month_key not in month_data:
                month_data[month_key] = {
                    "date": datetime(order_date.year, order_date.month, 1),
                    "orders_count": 0,
                    "items_sold": 0
                }
            
            month_data[month_key]["orders_count"] += 1
            month_data[month_key]["items_sold"] += sum(item["quantity"] for item in order["items"])
        
        # Convert to list and sort by date
        data_points = sorted(month_data.values(), key=lambda x: x["date"])
    
    elif time_frame == ReportTimeFrame.YEARLY:
        # For yearly reports, we group by year
        year_data = {}
        
        for order in orders:
            order_date = order["created_at"].date()
            year_key = str(order_date.year)
            
            if year_key not in year_data:
                year_data[year_key] = {
                    "date": datetime(order_date.year, 1, 1),
                    "orders_count": 0,
                    "items_sold": 0
                }
            
            year_data[year_key]["orders_count"] += 1
            year_data[year_key]["items_sold"] += sum(item["quantity"] for item in order["items"])
        
        # Convert to list and sort by date
        data_points = sorted(year_data.values(), key=lambda x: x["date"])
    
    # Create and return report
    return SalesReport(
        time_frame=time_frame,
        start_date=start,
        end_date=end,
        total_orders=total_orders,
        total_items_sold=total_items_sold,
        data=data_points
    )

async def generate_revenue_report(
    user_id: str,
    time_frame: ReportTimeFrame,
    start_date: date,
    end_date: Optional[date] = None
) -> RevenueReport:
    """
    Generate a revenue report.
    
    Args:
        user_id: The user's ID
        time_frame: The time frame (daily, weekly, monthly, yearly)
        start_date: The start date
        end_date: The end date (optional)
        
    Returns:
        RevenueReport: The revenue report
    """
    if db.orders is None:
        # Return empty report if DB not initialized
        return RevenueReport(
            time_frame=time_frame,
            start_date=start_date,
            end_date=end_date or start_date,
            total_revenue=0,
            total_tax=0,
            total_discount=0,
            total_net_amount=0,
            data=[]
        )
    
    # Get date range
    start, end = get_date_range(time_frame, start_date, end_date)
    
    # Convert to datetime for query
    start_datetime = datetime.combine(start, datetime.min.time())
    end_datetime = datetime.combine(end, datetime.max.time())
    
    # Query orders within date range
    orders = await db.orders.find({
        "user_id": user_id,
        "created_at": {
            "$gte": start_datetime,
            "$lte": end_datetime
        }
    }).to_list(length=None)
    
    # Calculate totals
    total_revenue = sum(order["subtotal"] for order in orders)
    total_tax = sum(order["tax"] for order in orders)
    total_discount = sum(order["discount"] for order in orders)
    total_net_amount = sum(order["total"] for order in orders)
    
    # Group data by time frame
    data_points = []
    
    if time_frame == ReportTimeFrame.DAILY:
        # For daily reports, we show each day
        current_date = start
        while current_date <= end:
            current_start = datetime.combine(current_date, datetime.min.time())
            current_end = datetime.combine(current_date, datetime.max.time())
            
            # Filter orders for current day
            day_orders = [o for o in orders if current_start <= o["created_at"] <= current_end]
            
            # Calculate data for current day
            revenue = sum(order["subtotal"] for order in day_orders)
            tax = sum(order["tax"] for order in day_orders)
            discount = sum(order["discount"] for order in day_orders)
            net_amount = sum(order["total"] for order in day_orders)
            
            # Add data point
            data_points.append({
                "date": current_start,
                "revenue": revenue,
                "tax": tax,
                "discount": discount,
                "net_amount": net_amount
            })
            
            # Move to next day
            current_date += timedelta(days=1)
    
    elif time_frame == ReportTimeFrame.WEEKLY:
        # For weekly reports, we group by week
        week_data = {}
        
        for order in orders:
            order_date = order["created_at"].date()
            week_num = order_date.isocalendar()[1]
            week_year = order_date.year
            week_key = f"{week_year}-{week_num}"
            
            if week_key not in week_data:
                week_data[week_key] = {
                    "date": datetime.combine(order_date, datetime.min.time()),
                    "revenue": 0,
                    "tax": 0,
                    "discount": 0,
                    "net_amount": 0
                }
            
            week_data[week_key]["revenue"] += order["subtotal"]
            week_data[week_key]["tax"] += order["tax"]
            week_data[week_key]["discount"] += order["discount"]
            week_data[week_key]["net_amount"] += order["total"]
        
        # Convert to list and sort by date
        data_points = sorted(week_data.values(), key=lambda x: x["date"])
    
    elif time_frame == ReportTimeFrame.MONTHLY:
        # For monthly reports, we group by month
        month_data = {}
        
        for order in orders:
            order_date = order["created_at"].date()
            month_key = f"{order_date.year}-{order_date.month}"
            
            if month_key not in month_data:
                month_data[month_key] = {
                    "date": datetime(order_date.year, order_date.month, 1),
                    "revenue": 0,
                    "tax": 0,
                    "discount": 0,
                    "net_amount": 0
                }
            
            month_data[month_key]["revenue"] += order["subtotal"]
            month_data[month_key]["tax"] += order["tax"]
            month_data[month_key]["discount"] += order["discount"]
            month_data[month_key]["net_amount"] += order["total"]
        
        # Convert to list and sort by date
        data_points = sorted(month_data.values(), key=lambda x: x["date"])
    
    elif time_frame == ReportTimeFrame.YEARLY:
        # For yearly reports, we group by year
        year_data = {}
        
        for order in orders:
            order_date = order["created_at"].date()
            year_key = str(order_date.year)
            
            if year_key not in year_data:
                year_data[year_key] = {
                    "date": datetime(order_date.year, 1, 1),
                    "revenue": 0,
                    "tax": 0,
                    "discount": 0,
                    "net_amount": 0
                }
            
            year_data[year_key]["revenue"] += order["subtotal"]
            year_data[year_key]["tax"] += order["tax"]
            year_data[year_key]["discount"] += order["discount"]
            year_data[year_key]["net_amount"] += order["total"]
        
        # Convert to list and sort by date
        data_points = sorted(year_data.values(), key=lambda x: x["date"])
    
    # Create and return report
    return RevenueReport(
        time_frame=time_frame,
        start_date=start,
        end_date=end,
        total_revenue=total_revenue,
        total_tax=total_tax,
        total_discount=total_discount,
        total_net_amount=total_net_amount,
        data=data_points
    )
