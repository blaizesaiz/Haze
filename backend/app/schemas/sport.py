"""Sport, event, and odds schemas."""
from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Dict, Any
from pydantic import BaseModel


class SportBase(BaseModel):
    """Base sport schema."""
    key: str
    name: str


class SportResponse(SportBase):
    """Schema for sport response."""
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class OddsBase(BaseModel):
    """Base odds schema."""
    bookmaker: str
    outcome: str
    price: Decimal
    point: Optional[Decimal] = None


class OddsResponse(OddsBase):
    """Schema for odds response."""
    id: int
    market_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MarketBase(BaseModel):
    """Base market schema."""
    key: str
    name: str


class MarketResponse(MarketBase):
    """Schema for market response."""
    id: int
    event_id: int
    odds: List[OddsResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True


class EventBase(BaseModel):
    """Base event schema."""
    home_team: str
    away_team: str
    commence_time: datetime


class EventCreate(EventBase):
    """Schema for creating an event."""
    sport_id: int
    external_id: str
    metadata: Optional[Dict[str, Any]] = None


class EventResponse(EventBase):
    """Schema for event response."""
    id: int
    sport_id: int
    external_id: str
    is_live: bool
    is_completed: bool
    home_score: Optional[int]
    away_score: Optional[int]
    markets: List[MarketResponse] = []
    created_at: datetime

    class Config:
        from_attributes = True


class EventListResponse(BaseModel):
    """Schema for event list response."""
    total: int
    events: List[EventResponse]
