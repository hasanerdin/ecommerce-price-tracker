from sqlalchemy.orm import Session

from backend.schemas import EventCreate
from backend.api.events import crud as event_crud
from backend.ingestion.seed_data import seed_events


def seed_single_event(db: Session, event_data: EventCreate) -> bool:
    """
    Seed a single event into database.

    Args:
        db: Database session
        event_data: EventCreate schema

    Returns:
        True if event is created, False if already exists
    """
    existing_event = event_crud.get_event_by_name(db, event_data.event_name)

    if existing_event is not None:
        return False

    event_crud.create_event(db, event_data)
    return True

def run_seed_events(db: Session) -> None:
    """
    Seed predefined events into database.
    Idempotent: can be run multiple times safely.
    """
    created_count = 0
    skipped_count = 0

    for event_data in seed_events:
        created = seed_single_event(db, event_data)

        if created:
            created_count += 1
        else:
            skipped_count += 1

    print(
        f"[SEED EVENTS] Created: {created_count}, Skipped: {skipped_count}"
    )