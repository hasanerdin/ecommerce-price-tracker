from datetime import date, timedelta

from backend.ingestion.daily_ingestion import run_daily_ingestion


def seed():
    current_date = date(2026, 1, 1)
    for _ in range(365):
        run_daily_ingestion(current_date)
        current_date += timedelta(days=1)