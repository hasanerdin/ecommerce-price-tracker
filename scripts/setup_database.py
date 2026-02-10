"""
Database setup script.

- Creates all database tables
- Seeds predefined events

Safe to run multiple times (idempotent).
"""
from backend.database import init_db
from backend.ingestion import seed_events
from backend.ingestion import seed_data

def setup_database() -> None:
    print("[SETUP] Creating database tables...")
    init_db()
    print("[SETUP] Tables created.")

    print("[SETUP] Seeding events...")
    seed_events.seed()
    print("[SETUP] Event seeding completed.")

def fill_yearly_price() -> None:
    print("[SETUP] Seeding prices...")
    seed_data.seed()
    print("[SETUP] Price seeding completed.")


if __name__ == "__main__":
    setup_database()
