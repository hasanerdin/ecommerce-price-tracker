"""Pydantic schemas for request/response validation"""
from datetime import date, datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator

# Product Schemas
class ProductCreate(BaseModel):
    """Schema for product information"""
    extarnal_id: int
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1, max_length=255)
    base_price: float
    rating: float

class ProductResponse(ProductCreate):
    """Schema for proudct response"""
    id: int

    class Config:
        from_attributes = True

# Price History

class PriceHistoryCreate(BaseModel):
    """Schema for price history information"""
    product_id: int
    price: float
    price_change_reason: str = Field(None, min_length=1, max_length=50)
    event_name: str = Field(None, min_length=1, max_length=255)
    price_source: Optional[str] = Field(None, pattern="^(synthetic|api|scraping)$")

    recorded_date: datetime

class PriceHistoryResponse(PriceHistoryCreate):
    """Schema for price history response"""
    id: int
    
    class Config:
        from_attributes = True

# Events

class EventCreate(BaseModel):
    """Schema for creating event"""
    event_name: str = Field(..., min_length=1, max_length=255)

    start_date: date
    end_date: date

    min_discount: float
    max_discount: float

class EventUpdate(BaseModel):
    """Schema for updating event"""
    event_name: Optional[str] = Field(None, min_length=1, max_length=255)

    start_date: Optional[date]
    end_date: Optional[date]

    min_discount: Optional[float]
    max_discount: Optional[float]

class EventResponse(BaseModel):
    """Schema for event response"""
    event_id: int
    event_name: str = Field(None, min_length=1, max_length=255)

    start_date: date
    end_date: date

    min_discount: float
    max_discount: float

    class Config:
        from_attributes = True


# Analytics
class PriceSummaryResponse(BaseModel):
    """Schema for price summary"""
    product_id: int

    start_date: date
    end_date: date

    min_price: float
    max_price: float
    avg_price: float

    class Config:
        from_attributes = True

class DiscountSummaryResponse(BaseModel):
    """Schema for price summary"""
    product_id: int

    start_date: date
    end_date: date

    min_discount: float
    max_discount: float
    avg_discount: float

    class Config:
        from_attributes = True

# Health Check Schema
class HealthResponse(BaseModel):
    """Schema for health check response."""
    status: str
    timestamp: datetime
    database: str