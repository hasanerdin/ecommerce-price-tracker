from datetime import date

from backend.ingestion.daily_ingestion import run_daily_ingestion
from backend.models import PriceHistory

def test_daily_ingestion_idempotent(db_session):
    
    run_daily_ingestion(db_session, snapshot_date=date(2026, 1, 10))
    first_count = db_session.query(PriceHistory).count()

    run_daily_ingestion(db_session, snapshot_date=date(2026, 1, 10))
    second_count = db_session.query(PriceHistory).count()
    
    assert first_count == second_count
