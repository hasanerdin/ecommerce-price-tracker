from backend.api.events import crud as event_crud


def test_events_table_not_empty(db_session):
    count = event_crud.count_events(db_session)
    assert count > 0

def test_seeded_events_exist(db_session):
    event_names = [
        "Valentines Day",
        "Black Friday",
    ]

    for name in event_names:
        event = event_crud.get_event_by_name(db_session, name)
        assert event is not None

def test_valentines_day_fields(db_session):
    event = event_crud.get_event_by_name(db_session, "Valentines Day")

    assert event.pre_event_days > 0
    assert event.discount_min < event.discount_max
