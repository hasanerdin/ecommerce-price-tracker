"""CRUD operations for analytics"""
from typing import Optional, Dict, Any, List
from datetime import date, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.models import PriceHistory, Event

def get_price_history(db: Session, product_id: int, 
                      skip: int = 0, limit: int = 100) -> Optional[List[PriceHistory]]:
    """
    Get list of all price history of the product

    Args:
        db: Database session
        product_id: Product ID
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of price history or None if product_id not found
    """
    return db.query(PriceHistory).filter(
        PriceHistory.product_id == product_id
    ).order_by(
        PriceHistory.created_at.desc()
        ).offset(skip).limit(limit).all()

def get_price_history_by_recorded_date(db: Session, product_id: int, recorded_date: date) -> Optional[PriceHistory]:
    """
    Get a price history instance by product_id and recorded_date

    Args:
        db: Database session
        product_id: Product ID
        recorded_date: When the instance is recorded

    Returns:
        Price History instance or None if not found
    """
    return db.query(PriceHistory).filter(
        PriceHistory.product_id == product_id,
        PriceHistory.recorded_date == recorded_date
    ).first()

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

def get_event_price_impact(
    db: Session,
    event_id: int,
    product_id: int,
):
    """
    Impact of the Event over product

    Args:
        db: Database session
        event_id: Event Id
        product_id: Prodcut Id

    Returns:
        Dict that holds effect of the event on product if event exists. Otherwise, None
    """

    event = db.query(Event).filter(Event.event_id == event_id).first()
    if not event or event.pre_event_days == 0:
        return None

    # Pre-event window
    pre_start = event.start_date - timedelta(days=event.pre_event_days)
    pre_end = event.start_date - timedelta(days=1)

    pre_event_avg = db.query(
        func.avg(PriceHistory.price)
    ).filter(
        PriceHistory.product_id == product_id,
        PriceHistory.recorded_date >= pre_start,
        PriceHistory.recorded_date <= pre_end,
    ).scalar()

    # Event window
    event_avg = db.query(
        func.avg(PriceHistory.price)
    ).filter(
        PriceHistory.product_id == product_id,
        PriceHistory.event_id == event_id,
    ).scalar()

    if pre_event_avg is None or event_avg is None:
        return None

    return {
        "event_id": event.event_id,
        "event_name": event.event_name,
        "product_id": product_id,
        "pre_event_avg_price": round(pre_event_avg, 2),
        "event_avg_price": round(event_avg, 2),
        "price_change_abs": round(event_avg - pre_event_avg, 2),
        "price_change_pct": round(
            ((event_avg - pre_event_avg) / pre_event_avg) * 100, 2
        ),
    }
