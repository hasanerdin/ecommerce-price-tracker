"""CRUD operations for events"""
from typing import Optional, List
from datetime import date, timedelta
from sqlalchemy.orm import Session

from backend.models import Event
from backend.schemas import EventCreate, EventUpdate


def get_event(db: Session, event_id: int) -> Optional[Event]:
    """
    Get a event by ID
    """
    return db.query(Event).filter(Event.event_id == event_id).first()

def get_event_by_name(db: Session, event_name: str) -> Optional[Event]:
    """
    Get a event by Name
    """
    return db.query(Event).filter(Event.event_name == event_name).first()

def get_all_events(db: Session, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[Event]:
    """
    Get list of all events
    """
    return db.query(Event).filter(
        Event.start_date <= end_date,
        Event.end_date >= start_date
    ).order_by(
        Event.start_date,
        Event.end_date
    )

def count_events(db: Session) -> int:
    """
    Count events
    """
    return db.query(Event).count()

def create_event(db: Session, event_data: EventCreate) -> Event:
    """
    Create a new event
    """
    event = Event(
        event_name=event_data.event_name,
        start_date=event_data.start_date,
        end_date=event_data.end_date,
        pre_event_days=event_data.pre_event_days,
        pre_event_uplift_min=event_data.pre_event_uplift_min,
        pre_event_uplift_max=event_data.pre_event_uplift_max,
        discount_min=event_data.discount_min,
        discount_max=event_data.discount_max,
        noise_enabled=event_data.noise_enabled
    )

    db.add(event)
    db.commit()
    db.refresh(event)
    return event

def update_event(db: Session, event_id: int, event_data: EventUpdate) -> Optional[Event]:
    """
    Update created event
    """
    event = get_event(db, event_id)
    if event is None:
        return None

    for key, value in event_data.model_dump(exclude_unset=True):
        setattr(event, key, value)

    db.commit()
    db.refresh(event)
    return event

def delete_event(db: Session, event_id: int) -> bool:
    """
    Delete a event
    """
    event = get_event(db, event_id)
    if not event:
        return False
    
    db.delete(event)
    db.commit()
    return True

def get_active_event(db: Session, current_date: date) -> Optional[Event]:
    """
    Returns active event for given date if exist
    """
    return db.query(Event).filter(
        Event.start_date <= current_date,
        Event.end_date >= current_date
    ).order_by(Event.start_date).first()

def get_pre_event(db: Session, current_date: date) -> Optional[Event]:
    """
    Returns pre-event if current_date is within pre-event window
    """
    events = db.query(Event).all()

    for event in events:
        if event.pre_event_days and event.pre_event_days > 0:
            pre_event_start = event.start_date - timedelta(days=event.pre_event_days)

            if pre_event_start <= current_date < event.start_date:
                return event
            
    return None