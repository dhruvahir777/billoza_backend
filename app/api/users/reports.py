from fastapi import APIRouter, Depends, HTTPException, Path, Query
from typing import List, Optional
from datetime import datetime, date
from app.middleware.auth_middleware import get_current_user
from app.middleware.access_control import verify_user_access
from app.schemas.report import SalesReport, RevenueReport, ReportTimeFrame
from app.services.report_service import generate_sales_report, generate_revenue_report

router = APIRouter()

@router.get("/{user_id}/reports/sales", response_model=SalesReport)
async def get_sales_report(
    user_id: str = Path(...),
    time_frame: ReportTimeFrame = Query(ReportTimeFrame.DAILY),
    start_date: date = Query(...),
    end_date: Optional[date] = Query(None),
    current_user=Depends(get_current_user)
):
    """
    Generate a sales report for a specific user.
    """
    verify_user_access(current_user, user_id)
    
    report = await generate_sales_report(
        user_id=user_id,
        time_frame=time_frame,
        start_date=start_date,
        end_date=end_date
    )
    return report

@router.get("/{user_id}/reports/revenue", response_model=RevenueReport)
async def get_revenue_report(
    user_id: str = Path(...),
    time_frame: ReportTimeFrame = Query(ReportTimeFrame.DAILY),
    start_date: date = Query(...),
    end_date: Optional[date] = Query(None),
    current_user=Depends(get_current_user)
):
    """
    Generate a revenue report for a specific user.
    """
    verify_user_access(current_user, user_id)
    
    report = await generate_revenue_report(
        user_id=user_id,
        time_frame=time_frame,
        start_date=start_date,
        end_date=end_date
    )
    return report
