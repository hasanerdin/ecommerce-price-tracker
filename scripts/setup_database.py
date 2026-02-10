"""
Database setup script.

- Creates all database tables
- Seeds predefined events

Safe to run multiple times (idempotent).
"""
from sqlalchemy.orm import Session

from backend.schemas import EventCreate
from backend.api.events import crud as event_crud
from backend.ingestion.seed_data import seed_events
from backend.database import SessionLocal, init_db


def run_seed_events(db: Session) -> None:
    """
    Seed predefined events into database.
    Idempotent: can be run multiple times safely.
    """
    created_count = 0
    skipped_count = 0

    for event_data in seed_events:
        existing_event = event_crud.get_event_by_name(db, event_data.event_name)

        if existing_event is not None:
            skipped_count += 1
            continue
        
        event_crud.create_event(db, event_data)
        created_count += 1

    print(
        f"[SEED EVENTS] Created: {created_count}, Skipped: {skipped_count}"
    )

def setup_database() -> None:
    print("[SETUP] Creating database tables...")
    init_db()
    print("[SETUP] Tables created.")

    db = SessionLocal()
    try:
        print("[SETUP] Seeding events...")
        run_seed_events(db)
        print("[SETUP] Event seeding completed.")
    finally:
        db.close()


if __name__ == "__main__":
    setup_database()
