from datetime import date

from backend.schemas import EventCreate
from backend.database import SessionLocal
from backend.api.events import crud as event_crud

events = [
            EventCreate(
                event_name="Valentines Day",
                start_date=date(2026, 2, 14),
                end_date=date(2026, 2, 14),
                pre_event_days=7,
                pre_event_uplift_min=0.02,
                pre_event_uplift_max=0.05,
                discount_min=0.15,
                discount_max=0.25,
                noise_enabled=False
            ),
            EventCreate(
                event_name="Black Friday",
                start_date=date(2026, 11, 27),
                end_date=date(2026, 11, 27),
                pre_event_days=14,
                pre_event_uplift_min=0.05,
                pre_event_uplift_max=0.1,
                discount_min=0.3,
                discount_max=0.5,
                noise_enabled=False
            ),
            EventCreate(
                event_name="Christmas Sale",
                start_date=date(2026, 12, 20),
                end_date=date(2026, 12, 26),
                pre_event_days=10,
                pre_event_uplift_min=0.02,
                pre_event_uplift_max=0.05,
                discount_min=0.2,
                discount_max=0.35,
                noise_enabled=False
            ),
            EventCreate(
                event_name="Back to School",
                start_date=date(2026, 8, 15),
                end_date=date(2026, 8, 31),
                pre_event_days=10,
                pre_event_uplift_min=0.03,
                pre_event_uplift_max=0.06,
                discount_min=0.15,
                discount_max=0.3,
                noise_enabled=True
            )
        ]

def seed():
    """
    Seed predefined events into database.
    Idempotent: can be run multiple times safely.
    """
    db = SessionLocal()
    created_count = 0
    skipped_count = 0

    for event_data in events:
        existing_event = event_crud.get_event_by_name(db, event_data.event_name)

        if existing_event is not None:
            skipped_count += 1
            continue
        
        event_crud.create_event(db, event_data)
        created_count += 1

    print(
        f"[SEED EVENTS] Created: {created_count}, Skipped: {skipped_count}"
    )
