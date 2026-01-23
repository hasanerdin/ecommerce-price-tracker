"""CRUD operations for analytics"""
from typing import Optional, Dict, Any
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.models import PriceHistory

def get_price_summary(db: Session, product_id: int, start_date: date, end_date: date) -> Optional[Dict[str, Any]]:
    """
    Summarize the price history of the product

    Args:
        db: Database session
        product_id: Product ID
        start_date: beginning date of the summary
        end_date: end date of the summary

    Returns:
        summary of the price history
    """
    summary = db.query(
        func.min(PriceHistory.price).label("min_price"),
        func.max(PriceHistory.price).label("max_price"),
        func.avg(PriceHistory.price).label("avg_price")
    ).filter(
        PriceHistory.product_id == product_id,
        PriceHistory.recorded_date >= start_date,
        PriceHistory.recorded_date <= end_date
    ).one()

    if summary.min_price is None:
        return None 

    return {
        "product_id": product_id,
        "start_date": start_date,
        "end_date": end_date,
        "min_price": summary.min_price,
        "max_price": summary.max_price,
        "avg_price": summary.avg_price
    }

def get_discount_summary(db: Session, product_id: int, start_date: date, end_date: date) -> Optional[Dict[str, Any]]:
    """
    Summarize the discount history of the product

    Args:
        db: Database session
        product_id: Product ID
        start_date: beginning date of the summary
        end_date: end date of the summary

    Returns:
        summary of the discount history
    """
    summary = db.query(
        func.min(PriceHistory.discount_percent).label("min_discount"),
        func.max(PriceHistory.discount_percent).label("max_discount"),
        func.avg(PriceHistory.discount_percent).label("avg_discount")
    ).filter(
        PriceHistory.product_id == product_id,
        PriceHistory.recorded_date >= start_date,
        PriceHistory.recorded_date <= end_date
    ).one()

    if not summary.min_discount:
        return None 

    return {
        "product_id": product_id,
        "start_date": start_date,
        "end_date": end_date,
        "min_discount": summary.min_discount,
        "max_discount": summary.max_discount,
        "avg_discount": summary.avg_discount
    }