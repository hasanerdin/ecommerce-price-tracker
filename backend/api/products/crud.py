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
        external_id=product_data.extarnal_id,
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
        event_id=price_history_data.event_id,
        price=price_history_data.price,
        price_change_reason=price_history_data.price_change_reason,
        price_source=price_history_data.price_source,
        recorded_date=price_history_data.recorded_date
    )

    db.add(price_history)
    db.commit()
    db.refresh(price_history)
    return price_history