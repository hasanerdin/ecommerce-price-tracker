"""Event Informations"""
from typing import Tuple
from datetime import date
from dataclasses import dataclass

@dataclass(frozen=True)
class EventRule:
    event_id: int
    name: str 
    start_date: date 
    end_date: date
    pre_event_days: int = 7
    pre_event_uplift_range: Tuple[float, float] = (0.0, 0.0)
    discount_range: Tuple[float, float] = (0.0, 0.0)
    noise_enabled: bool = False

EVENT_RULES = [
    EventRule(
        event_id=1,
        name="Valentines Day",
        start_date=date(2026, 2, 14),
        end_date=date(2026, 2, 14),
        pre_event_days=7,
        pre_event_uplift_range=(0.02, 0.05),
        discount_range=(0.15, 0.25),
        noise_enabled=False,
    ),

    EventRule(
        event_id=2,
        name="Easter Sale",
        start_date=date(2026, 4, 3),
        end_date=date(2026, 4, 6),
        pre_event_days=5,
        pre_event_uplift_range=(0.01, 0.03),
        discount_range=(0.10, 0.20),
        noise_enabled=False,
    ),

    EventRule(
        event_id=3,
        name="Back to School",
        start_date=date(2026, 8, 15),
        end_date=date(2026, 8, 31),
        pre_event_days=10,
        pre_event_uplift_range=(0.03, 0.06),
        discount_range=(0.15, 0.30),
        noise_enabled=True,
    ),

    EventRule(
        event_id=4,
        name="Black Friday",
        start_date=date(2026, 11, 27),
        end_date=date(2026, 11, 27),
        pre_event_days=14,
        pre_event_uplift_range=(0.05, 0.10),
        discount_range=(0.30, 0.50),
        noise_enabled=False,
    ),

    EventRule(
        event_id=5,
        name="Christmas Sale",
        start_date=date(2026, 12, 20),
        end_date=date(2026, 12, 26),
        pre_event_days=10,
        pre_event_uplift_range=(0.02, 0.05),
        discount_range=(0.20, 0.35),
        noise_enabled=False,
    ),
]