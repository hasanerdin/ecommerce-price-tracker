"""CRUD operations for products"""
from typing import Optional, List
from datetime import date
from sqlalchemy.orm import Session

from backend.models import Product, PriceHistory
from backend.schemas import ProductCreate, PriceHistoryCreate

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

def get_product_by_external_id(db: Session, external_id: int) -> Optional[Product]:
    """
    Get a product by external ID given by API

    Args:
        db: Database session
        external_id: External ID

    Returns:
        Product instance or None if not found
    """
    return db.query(Product).filter(Product.external_id == external_id).first()

def get_all_products(db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
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

def create_product(db: Session, product_data: ProductCreate) -> Product:
    """
    Create a new product

    Args:
        db: Database session
        product_data: Product create data

    Returns:
        Created Product Instance
    """
    product = Product(
        title=product_data.title,
        description=product_data.description,
        base_price=product_data.base_price,
        rating=product_data.rating
    )

    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def create_price_history(db: Session, price_history_data: PriceHistoryCreate) -> PriceHistory:
    """
    Create a new price history

    Args:
        db: Database session
        price_history_data: Price history create data

    Returns:
        Created Price History Instance
    """
    price_history = PriceHistory(
        product_id=price_history_data.product_id,
        price=price_history_data.price,
        price_change_reason=price_history_data.price_change_reason,
        event_name=price_history_data.event_name,
        price_source=price_history_data.price_source,
        recorded_date=price_history_data.recorded_date
    )

    db.add(price_history)
    db.commit()
    db.refresh(price_history)
    return price_history