"""Product-related API endpoints"""
from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from backend.schemas import ProductResponse, PriceHistoryResponse
from backend.database import get_db
from backend.api.products import crud

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=List[ProductResponse])
def list_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List products

    Args:
        db: Database session

    Returns:
        List of products
    """

    products = crud.get_all_products(db, skip, limit)
    return products

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Get a product by ID

    Args:
        product_id: Product ID
        db: Database session

    Returns:
        Product Details
    
    Raises:
        HTTPException if product not found
    """
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found."
        )
    return product