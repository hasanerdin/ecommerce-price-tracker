"""Product-related API endpoints"""
from typing import List, Optional
from datetime import date
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from backend.schemas import EventResponse, EventCreate, EventUpdate
from backend.database import get_db
from backend.api.events import crud

router = APIRouter(prefix="/events", tags=["events"])

@router.get("/", response_model=List[EventResponse])
def list_events(start_date: Optional[date] = None, end_date: Optional[date] = None, db: Session = Depends(get_db)):
    """
    List event

    Args:
        db: Database session

    Returns:
        List of event
    """

    events = crud.get_all_events(db, start_date, end_date)
    return events

@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    """
    Get a event by ID

    Args:
        event_id: Event ID
        db: Database session

    Returns:
        Event Details
    
    Raises:
        HTTPException if event not found
    """
    event = crud.get_event(db, event_id)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id {event_id} not found."
        )
    return event

@router.get("/{event_name}", response_model=EventResponse)
def get_event_by_name(event_name: str, db: Session = Depends(get_db)):
    """
    Get a event by Name

    Args:
        event_name: Event Name
        db: Database session

    Returns:
        Event Details
    
    Raises:
        HTTPException if event not found
    """
    event = crud.get_event_by_name(db, event_name)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with name {event_name} not found."
        )
    return event

@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
def create_event(event_data: EventCreate, db: Session = Depends(get_db)):
    """
    Create a new event

    Args:
        event_date: Event creation data
        db: Database session

    Returns:
        Created event
    """

    event = crud.create_event(db, event_data)
    return event

@router.put("/{event_id}", response_model=EventResponse)
def update_event(event_id: int, event_data: EventUpdate, db: Session = Depends(get_db)):
    """
    Update a event

    Args:
        event_id: Event ID
        event_data: Update event data
        db: Database session

    Returns:
        Updated event

    Raises:
        HTTPException: If event not found
    """
    event = crud.update_event(db, event_id, event_data)
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id {event_id} not found"
        )
    return event

@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    """
    Delete a event

    Args:
        event_id: Event ID
        db: Database session

    Raises:
        HTTPException: If event not found
    """
    success = crud.delete_event(db, event_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event with id {event_id} not found"
        )