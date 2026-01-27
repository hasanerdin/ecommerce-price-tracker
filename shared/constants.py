"""Constants and Enums"""
from enum import Enum
from typing import Tuple

DAILY_PRICE_NOISE : Tuple[float, float] = (-0.03, 0.03)

class PriceType(Enum):
    Real = "real"
    Synthetic = "synthetic"
