from datetime import date

from backend.ingestion.price_engine import generate_daily_price
from shared.constants import PriceType

def test_normal_day_price_has_noise():
    price, metadata = generate_daily_price(
        base_price=100.0,
        current_date=date(2026, 1, 10), # There should not be any event
        pricing_mode=PriceType.Synthetic
    )

    assert 97 <= price <= 103
    assert metadata["event_name"] is None
    assert metadata["adjustment_reason"] == "base_price+noise"

def test_event_day_discount_applied():
    price, metadata = generate_daily_price(
        base_price=100.0,
        current_date=date(2026, 2, 14), # Valentines Day,
        pricing_mode=PriceType.Synthetic
    )

    assert price < 100
    assert metadata["event_name"] == "Valentines Day"
    assert "event_discount" in metadata["adjustment_reason"]

def test_pre_event_uplift_applied():
    price, metadata = generate_daily_price(
        base_price=100.0,
        current_date=date(2026, 2, 10), # pre_event day before Valentines Day
        pricing_mode=PriceType.Synthetic
    )

    assert price > 100
    assert metadata["event_name"] == "Valentines Day"
    assert metadata["adjustment_reason"] == "pre_event_uplift"

def test_real_pricing_mode_no_change():
    price, metadata = generate_daily_price(
        base_price=100.0,
        current_date=date(2026, 11, 27), # Black Friday
        pricing_mode=PriceType.Real
    )

    assert price == 100.0
    assert metadata["price_source"] == PriceType.Real
