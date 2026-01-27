import pytest

from backend.database import init_db, SessionLocal


@pytest.fixture
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """
    Create all tables before any tests run.
    """
    init_db()