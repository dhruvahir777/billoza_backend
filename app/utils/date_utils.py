from datetime import datetime, date, timedelta
import calendar
from typing import List, Dict, Tuple, Union

def get_date_range(time_frame: str, start_date: date, end_date: date = None) -> Tuple[date, date]:
    """
    Get a date range based on the time frame.
    
    Args:
        time_frame: The time frame (daily, weekly, monthly, yearly)
        start_date: The start date
        end_date: The end date (optional)
        
    Returns:
        Tuple[date, date]: The start and end dates
    """
    if end_date is None:
        if time_frame == "daily":
            end_date = start_date
        elif time_frame == "weekly":
            # Get the end of the week (Sunday)
            days_ahead = 6 - start_date.weekday()
            end_date = start_date + timedelta(days=days_ahead)
        elif time_frame == "monthly":
            # Get the end of the month
            last_day = calendar.monthrange(start_date.year, start_date.month)[1]
            end_date = date(start_date.year, start_date.month, last_day)
        elif time_frame == "yearly":
            # Get the end of the year
            end_date = date(start_date.year, 12, 31)
        else:
            # Default to today
            end_date = start_date
    
    return start_date, end_date

def format_date_for_timeframe(dt: Union[date, datetime], time_frame: str) -> str:
    """
    Format a date based on the time frame.
    
    Args:
        dt: The date to format
        time_frame: The time frame (daily, weekly, monthly, yearly)
        
    Returns:
        str: The formatted date
    """
    if isinstance(dt, datetime):
        dt = dt.date()
        
    if time_frame == "daily":
        return dt.strftime("%Y-%m-%d")
    elif time_frame == "weekly":
        # Format as Week X of YYYY
        return f"Week {dt.isocalendar()[1]} of {dt.year}"
    elif time_frame == "monthly":
        # Format as Month YYYY
        return dt.strftime("%B %Y")
    elif time_frame == "yearly":
        # Format as YYYY
        return str(dt.year)
    else:
        return dt.strftime("%Y-%m-%d")
