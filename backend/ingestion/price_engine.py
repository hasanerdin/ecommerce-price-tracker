"""Generate Synthetic price according to events"""
from datetime import date, timedelta
from typing import Optional, Tuple
import random
from sqlalchemy.orm import Session

from shared.constants import PriceType, DAILY_PRICE_NOISE
from backend.api.events import crud as event_crud
from backend.models import Event


# --------------------------------------------------
# Price adjustments
# --------------------------------------------------

def apply_pre_event_uplift(price: float, uplift_range: Tuple[float, float]) -> float:
    """
    Applies a small uplift before special events.
    """
    uplift = random.uniform(*uplift_range)
    return price * (1 + uplift)


def apply_event_discount(price: float, discount_range: Tuple[float, float]) -> float:
    """
    Applies discount during the event.
    """
    discount = random.uniform(*discount_range)
    return price * (1 - discount)


def apply_daily_noise(price: float, noise_range: Tuple[float, float] = DAILY_PRICE_NOISE) -> float:
    """
    Applies small daily random fluctuation.
    """
    noise = random.uniform(*noise_range)
    return price * (1 + noise)

# --------------------------------------------------
# Event price update
# --------------------------------------------------

def active_event_price_update(base_price: float, active_event: Event, metadata: dict) -> Tuple[float, dict]:
    discount = random.uniform(
        active_event.discount_min,
        active_event.discount_max
    )

    final_price = base_price * (1-discount)

    metadata.update(
        {
            "adjustment_reason": "event_discount",
            "event_id": active_event.event_id,
            "event_name": active_event.event_name
        }
    )

    if active_event.noise_enabled:
        # Normal daily noise
        price = apply_daily_noise(price)
        metadata["adjustment_reason"] += "+noise"

    return round(final_price, 2), metadata

def pre_event_price_update(base_price: float, pre_event: Event, metadata: dict) -> Tuple[float, dict]:
    uplift = random.uniform(
        pre_event.pre_event_uplift_min,
        pre_event.pre_event_uplift_max,
    )

    final_price = base_price * (1 + uplift)

    metadata.update(
        {
            "adjustment_reason": "pre_event_uplift",
            "event_id": pre_event.event_id,
            "event_name": pre_event.event_name,
        }
    )

    if pre_event.noise_enabled:
        # Normal daily noise
        price = apply_daily_noise(price)
        metadata["adjustment_reason"] += "+noise"

    return round(final_price, 2), metadata

# --------------------------------------------------
# Main entry point
# --------------------------------------------------

def generate_daily_price(
    db: Session,
    base_price: float,
    current_date: date,
    pricing_mode: PriceType = PriceType.Synthetic,
) -> Tuple[float, dict]:
    """
    Generates the final daily price and metadata.

    Returns:
        final_price: float
        metadata: dict
    """

    price = base_price
    metadata = {
        "adjustment_reason": "base_price",
        "event_id": None,
        "event_name": None,
        "price_source": pricing_mode,
        "recorded_date": current_date
    }

    # Real pricing mode
    if pricing_mode == PriceType.Real:
        return round(price, 2), metadata
    
    # Synthetic pricing mode

    # Active event
    active_event = event_crud.get_active_event(db, current_date)
    if active_event:
        return active_event_price_update(base_price, active_event, metadata)
    
    # Pre-event
    pre_event = event_crud.get_pre_event(db, current_date)
    if pre_event:
        return pre_event_price_update(base_price, pre_event, metadata)
    
    # Normal day noise
    final_price = apply_daily_noise(base_price)
    metadata["adjustment_reason"] += "+noise"

    return round(final_price, 2), metadata