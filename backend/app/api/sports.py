"""Sports and events routes."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.sport import SportResponse, EventResponse, EventListResponse
from app.models.sport import Sport, Event, Market, Odds as OddsModel
from app.services.odds_api import odds_api_service

router = APIRouter(prefix="/sports", tags=["sports"])


@router.get("", response_model=List[SportResponse])
async def get_sports(db: Session = Depends(get_db)):
    """
    Get all available sports.

    Args:
        db: Database session

    Returns:
        List of sports
    """
    sports = db.query(Sport).filter(Sport.is_active == True).all()
    return sports


@router.post("/sync", status_code=status.HTTP_200_OK)
async def sync_sports(db: Session = Depends(get_db)):
    """
    Sync sports from The Odds API.

    Args:
        db: Database session

    Returns:
        Success message
    """
    from datetime import datetime

    sports_data = await odds_api_service.get_sports()

    for sport_data in sports_data:
        sport = db.query(Sport).filter(Sport.key == sport_data["key"]).first()

        if not sport:
            sport = Sport(
                key=sport_data["key"],
                name=sport_data["title"],
                is_active=sport_data.get("active", True)
            )
            db.add(sport)
        else:
            sport.name = sport_data["title"]
            sport.is_active = sport_data.get("active", True)
            sport.updated_at = datetime.utcnow()

    db.commit()
    return {"message": "Sports synced successfully"}


@router.get("/{sport_key}/events", response_model=EventListResponse)
async def get_events(
    sport_key: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    Get events for a sport.

    Args:
        sport_key: Sport key
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session

    Returns:
        List of events
    """
    sport = db.query(Sport).filter(Sport.key == sport_key).first()
    if not sport:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sport not found"
        )

    events = db.query(Event).filter(
        Event.sport_id == sport.id,
        Event.is_completed == False
    ).order_by(Event.commence_time).offset(skip).limit(limit).all()

    total = db.query(Event).filter(
        Event.sport_id == sport.id,
        Event.is_completed == False
    ).count()

    return {"events": events, "total": total}


@router.post("/{sport_key}/sync-odds", status_code=status.HTTP_200_OK)
async def sync_odds(sport_key: str, db: Session = Depends(get_db)):
    """
    Sync odds for a sport from The Odds API.

    Args:
        sport_key: Sport key
        db: Database session

    Returns:
        Success message
    """
    from datetime import datetime
    from decimal import Decimal

    sport = db.query(Sport).filter(Sport.key == sport_key).first()
    if not sport:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sport not found"
        )

    odds_data = await odds_api_service.get_odds(sport_key)

    for event_data in odds_data:
        # Create or update event
        event = db.query(Event).filter(Event.external_id == event_data["id"]).first()

        if not event:
            event = Event(
                sport_id=sport.id,
                external_id=event_data["id"],
                home_team=event_data["home_team"],
                away_team=event_data["away_team"],
                commence_time=datetime.fromisoformat(event_data["commence_time"].replace("Z", "+00:00"))
            )
            db.add(event)
            db.flush()
        else:
            event.home_team = event_data["home_team"]
            event.away_team = event_data["away_team"]
            event.commence_time = datetime.fromisoformat(event_data["commence_time"].replace("Z", "+00:00"))

        # Process bookmakers and odds
        for bookmaker_data in event_data.get("bookmakers", []):
            for market_data in bookmaker_data.get("markets", []):
                # Create or get market
                market = db.query(Market).filter(
                    Market.event_id == event.id,
                    Market.key == market_data["key"]
                ).first()

                if not market:
                    market = Market(
                        event_id=event.id,
                        key=market_data["key"],
                        name=market_data["key"]
                    )
                    db.add(market)
                    db.flush()

                # Create or update odds
                for outcome_data in market_data.get("outcomes", []):
                    odds = db.query(OddsModel).filter(
                        OddsModel.market_id == market.id,
                        OddsModel.bookmaker == bookmaker_data["key"],
                        OddsModel.outcome == outcome_data["name"]
                    ).first()

                    if not odds:
                        odds = OddsModel(
                            market_id=market.id,
                            bookmaker=bookmaker_data["key"],
                            outcome=outcome_data["name"],
                            price=Decimal(str(outcome_data["price"])),
                            point=Decimal(str(outcome_data["point"])) if "point" in outcome_data else None
                        )
                        db.add(odds)
                    else:
                        odds.price = Decimal(str(outcome_data["price"]))
                        odds.point = Decimal(str(outcome_data["point"])) if "point" in outcome_data else None
                        odds.updated_at = datetime.utcnow()

    db.commit()
    return {"message": f"Odds synced successfully for {sport_key}"}


@router.get("/events/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    """
    Get event details with odds.

    Args:
        event_id: Event ID
        db: Database session

    Returns:
        Event details
    """
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    return event
