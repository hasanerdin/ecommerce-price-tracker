"""Pydantic schemas for request/response validation"""
from datetime import date, datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict, Field

# Product Schemas
class ProductCreate(BaseModel):
    """Schema for product information"""
    extarnal_id: int
    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1, max_length=1000)
    base_price: float
    rating: float

class ProductResponse(ProductCreate):
    """Schema for proudct response"""
    id: int

    model_config=ConfigDict(from_attributes=True)

# Price History

class PriceHistoryCreate(BaseModel):
    """Schema for price history information"""
    product_id: int
    event_id: Optional[int]
    price: float
    price_change_reason: str = Field(None, min_length=1, max_length=50)
    price_source: Optional[str] = Field(None, pattern="^(synthetic|real)$")

    recorded_date: datetime

class PriceHistoryResponse(PriceHistoryCreate):
    """Schema for price history response"""
    id: int

    model_config=ConfigDict(from_attributes=True)

# Events

class EventCreate(BaseModel):
    """Schema for creating event"""
    event_name: str = Field(..., min_length=1, max_length=255)

    start_date: date
    end_date: date

    pre_event_days: int
    pre_event_uplift_min: float
    pre_event_uplift_max: float

    discount_min: float
    discount_max: float

    noise_enabled: bool

class EventUpdate(BaseModel):
    """Schema for updating event"""
    event_name: Optional[str] = Field(None, min_length=1, max_length=255)

    start_date: Optional[date]
    end_date: Optional[date]

    pre_event_days: Optional[int]
    pre_event_uplift_min: Optional[float]
    pre_event_uplift_max: Optional[float]

    discount_min: Optional[float]
    discount_max: Optional[float]

    noise_enabled: Optional[bool]

class EventResponse(EventCreate):
    """Schema for event response"""
    event_id: int

    model_config=ConfigDict(from_attributes=True)


# Analytics
class PriceSummaryResponse(BaseModel):
    """Schema for price summary"""
    product_id: int

    start_date: date
    end_date: date

    min_price: float
    max_price: float
    avg_price: float

    model_config=ConfigDict(from_attributes=True)


class DiscountSummaryResponse(BaseModel):
    """Schema for price summary"""
    product_id: int

    start_date: date
    end_date: date

    min_discount: float
    max_discount: float
    avg_discount: float

    model_config=ConfigDict(from_attributes=True)

class EventImpactResponse(BaseModel):
    """Schema for event impact"""
    event_id: int
    event_name: str = Field(..., min_length=1, max_length=255)

    product_id: int

    pre_event_avg_price: float
    event_avg_price: float
    price_change_pct: float
    price_change_abs: float

# Health Check Schema
class HealthResponse(BaseModel):
    """Schema for health check response."""
    status: str
    timestamp: datetime
    database: str