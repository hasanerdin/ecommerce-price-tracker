"""Database models for the Ecommerce Price Tracker application"""
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import (
    Column, Integer, String, Float, DateTime,
    Text, ForeignKey, Boolean, JSON, Date
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Product(Base):
    """Products represents products in ecommerce"""

    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String[255], nullable=False)
    description = Column(String[255], nullable=True)
    base_price = Column(Float, nullable=False)
    rating = Column(Float, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    # Relationships
    price_histories = relationship("PriceHistory", back_populates="product", cascade="all, delete-orphan", order_by="PriceHistory.created_at")

    def __repr__(self):
        return f"<Product({self.product_id}, title='{self.title}', base_price={self.base_price}, rating={self.rating})>"

class PriceHistory(Base):
    """Change of the price of the products"""

    __tablename__ = "price_histories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id", ondelete="CASCADE"), nullable=False)
    price = Column(Float, nullable=False)
    discount_percent = Column(Float, nullable=False)
    price_change_reason = Column(String[50], nullable=False)
    event_name = Column(String[255], ForeignKey("events.event_name", ondelete="CASCADE"), nullable=False)
    
    recorded_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # Relationship
    product = relationship("Product", back_populates="price_histories")
    event = relationship("Event", back_populates="price_histories")

    def __repr__(self):
        return f"<PriceHistory({self.id}, product_id={self.product_id}, price={self.price}, event_name='{self.event_name}')>"
    
class Event(Base):
    """Discount event"""

    __tablename__ = "events"

    event_id = Column(Integer, primary_key=True, autoincrement=True)
    event_name = Column(String[255], nullable=False)

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    min_discount = Column(Float, nullable=False)
    max_discount = Column(Float, nullable=False)

    # relationships
    price_histories = relationship("PriceHistory", back_populates="event", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Event({self.event_id}, event_name='{self.event_name}', dates={self.start_date} to {self.end_date})>"
