"""Analytics API endpoints"""
from typing import List, Optional
from datetime import date, timedelta
from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy.orm import Session

from backend.schemas import PriceSummaryResponse, DiscountSummaryResponse
from backend.database import get_db
from backend.api import crud_analytics

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/price-summary", response_model=PriceSummaryResponse)
def price_summary_by_product_id(product_id: int, 
                                start_date: Optional[date] = Query(None), 
                                end_date: Optional[date] = Query(None), 
                                db: Session = Depends(get_db)):
    """
    Summarize the price history of the product

    Args:
        product_id: Product ID
        start_date: beginning date of the summary
        end_date: end date of the summary
        db: Database session

    Returns:
        summary of the price history

    Raises:
        HTTPException if product with product_id not found or there is no price history between dates
    """
    if not end_date:
        end_date = date.today()

    if not start_date:
        start_date = end_date - timedelta(days=30)

    summary = crud_analytics.get_price_summary(db, product_id, start_date, end_date)
    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is not any history for product with id {product_id}."
        )
    
    return summary

@router.get("/discount-summary", response_model=PriceSummaryResponse)
def discount_summary_by_product_id(product_id: int, 
                                start_date: Optional[date] = Query(None), 
                                end_date: Optional[date] = Query(None), 
                                db: Session = Depends(get_db)):
    """
    Summarize the discount history of the product

    Args:
        product_id: Product ID
        start_date: beginning date of the summary
        end_date: end date of the summary
        db: Database session

    Returns:
        summary of the discount history

    Raises:
        HTTPException if product with product_id not found or there is no price history between dates
    """
    if not end_date:
        end_date = date.today()

    if not start_date:
        start_date = end_date - timedelta(days=30)

    summary = crud_analytics.get_price_summary(db, product_id, start_date, end_date)
    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is not any history for product with id {product_id}."
        )
    
    return summary