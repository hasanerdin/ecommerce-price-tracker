"""Event Informations"""
from typing import Tuple
from datetime import date
from dataclasses import dataclass

@dataclass(frozen=True)
class EventRule:
    name: str 
    start_date: date 
    end_date: date
    pre_event_days: int = 7
    pre_event_uplift_range: Tuple[float, float] = (0.0, 0.0)
    discount_range: Tuple[float, float] = (0.0, 0.0)
    noise_enable: bool = False

EVENT_RULES = [
    EventRule(
        name="Valentines Day",
        start_date=date(2026, 2, 14),
        end_date=date(2026, 2, 14),
        pre_event_days=7,
        pre_event_uplift_range=(0.02, 0.05),
        discount_range=(0.15, 0.25),
        noise_enabled=False,
    ),

    EventRule(
        name="Easter Sale",
        start_date=date(2026, 4, 3),
        end_date=date(2026, 4, 6),
        pre_event_days=5,
        pre_event_uplift_range=(0.01, 0.03),
        discount_range=(0.10, 0.20),
        noise_enabled=False,
    ),

    EventRule(
        name="Back to School",
        start_date=date(2026, 8, 15),
        end_date=date(2026, 8, 31),
        pre_event_days=10,
        pre_event_uplift_range=(0.03, 0.06),
        discount_range=(0.15, 0.30),
        noise_enabled=True,
    ),

    EventRule(
        name="Black Friday",
        start_date=date(2026, 11, 27),
        end_date=date(2026, 11, 27),
        pre_event_days=14,
        pre_event_uplift_range=(0.05, 0.10),
        discount_range=(0.30, 0.50),
        noise_enabled=False,
    ),

    EventRule(
        name="Christmas Sale",
        start_date=date(2026, 12, 20),
        end_date=date(2026, 12, 26),
        pre_event_days=10,
        pre_event_uplift_range=(0.02, 0.05),
        discount_range=(0.20, 0.35),
        noise_enabled=False,
    ),
]