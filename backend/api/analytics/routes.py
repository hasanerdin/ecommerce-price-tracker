"""Analytics API endpoints"""
from typing import List, Optional
from datetime import date, timedelta
from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy.orm import Session

from backend.schemas import (
                            PriceSummaryResponse, 
                            DiscountSummaryResponse, 
                            PriceHistoryResponse,
                            EventImpactResponse
                            )
from backend.database import get_db
from backend.api.analytics import crud as crud_analytics

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/{product_id}/price_history", response_model=List[PriceHistoryResponse])
def get_price_histories(product_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get a list of price history of product

    Args:
        product_id: Product ID
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session

    Returns:
        List of price history
    
    Raises:
        HTTPException if any price history for that product not found
    """
    price_histories = crud_analytics.get_price_history(db, product_id, skip, limit)
    if not price_histories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Price history for product with id {product_id} not found."
        )
    
    return price_histories

@router.get("/{product_id}/price-summary", response_model=PriceSummaryResponse)
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

@router.get("/{product_id}/discount-summary", response_model=DiscountSummaryResponse)
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

    summary = crud_analytics.get_discount_summary(db, product_id, start_date, end_date)
    if not summary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is not any history for product with id {product_id}."
        )
    
    return summary

@router.get("/{event_id}/products/{product_id}/impact", response_model=EventImpactResponse)
def get_event_impact(event_id: int, product_id: int, db: Session = Depends(get_db)):
    """
    Summarize the impact of the event on the product

    Args:
        event_id: Event ID
        product_id: Product ID
        db: Database session

    Returns:
        summary of the event changings

    Raises:
        HTTPException if event with event_id or product with product_id not found
    """
    impact = crud_analytics.get_event_price_impact(db=db, event_id=event_id, product_id=product_id)
    if not impact:
        raise HTTPException(
            status_code=404,
            detail="Not enough data to calculate event impact.",
        )

    return impact