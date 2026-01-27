"""Generate Synthetic price according to events"""
from datetime import date, timedelta
from typing import Optional, Tuple
import random

from shared.constants import PriceType, DAILY_PRICE_NOISE
from shared.event_rules import EventRule, EVENT_RULES

# --------------------------------------------------
#   EVENT LOOKUP
# --------------------------------------------------

def get_event_for_date(date: date) -> Optional[EventRule]:
    """
    Returns the event rule applicable for the given date, if any.
    """
    for event_rule in EVENT_RULES:
        if event_rule.start_date - timedelta(days=event_rule.pre_event_days) <= date <= event_rule.end_date:
            return event_rule
    
    return None

def is_pre_event_day(current_date: date, event: EventRule) -> bool:
    """
    Checks whether the current date falls into the pre-event uplift window.
    """
    days_to_event = (event.start_date - current_date).days
    return 0 < days_to_event <= event.pre_event_days

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
# Main entry point
# --------------------------------------------------

def generate_daily_price(
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
        "price_source": pricing_mode,
        "event_id": None,
        "event_name": None,
        "adjustment_reason": "base_price",
    }

    # Real pricing mode
    if pricing_mode == PriceType.Real:
        return round(price, 2), metadata
    
    # Synthetic pricing mode
    event = get_event_for_date(current_date)

    if event:
        metadata["event_id"] = event.event_id
        metadata["event_name"] = event.name

        # Pre-event uplift
        if is_pre_event_day(current_date, event):
            price = apply_pre_event_uplift(price, event.pre_event_uplift_range)
            metadata["adjustment_reason"] = "pre_event_uplift" 
        # Event day discount
        elif event.start_date <= current_date <= event.end_date:
            price = apply_event_discount(price, event.discount_range)
            metadata["adjustment_reason"] = "event_discount"

            if event.noise_enabled:
                # Normal daily noise
                price = apply_daily_noise(price)
                metadata["adjustment_reason"] += "+noise"
    else:
        # Normal daily noise
        price = apply_daily_noise(price)
        metadata["adjustment_reason"] += "+noise"

    return round(price, 2), metadata