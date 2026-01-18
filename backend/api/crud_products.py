"""CRUD operations for products"""
from typing import Optional, List
from sqlalchemy.orm import Session

from backend.models import Product, PriceHistory

def get_product(db: Session, product_id: int) -> Optional[Product]:
    """
    Get a product by ID

    Args:
        db: Database session
        product_id: Product ID

    Returns:
        Product instance or None if not found
    """
    return db.query(Product).filter(Product.product_id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
    """
    Get list of all products

    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return

    Returns:
        List of products
    """
    return db.query(Product).order_by(Product.rating.desc()).offset(skip).limit(limit).all()

def count_products(db: Session) -> int:
    """
    Count products

    Args:
        db: Database session
    
    Returns:
        Count of products
    """
    return db.query(Product).count()

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