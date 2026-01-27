from shared.event_rules import EVENT_RULES


def test_event_rules_not_empty():
    assert len(EVENT_RULES) > 0


def test_valentines_day_exists():
    assert "Valentines Day" in [e.name for e in EVENT_RULES]
    assert "Black Friday" in [e.name for e in EVENT_RULES]
