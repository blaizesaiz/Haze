"""Bet schemas."""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field

from app.models.bet import BetStatus


class BetCreate(BaseModel):
    """Schema for creating a bet."""
    event_id: int
    odds_id: int
    stake: Decimal = Field(..., gt=0)


class BetResponse(BaseModel):
    """Schema for bet response."""
    id: int
    user_id: int
    event_id: int
    odds_id: int
    stake: Decimal
    odds_value: Decimal
    potential_payout: Decimal
    status: BetStatus
    outcome: Optional[str]
    settled_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class BetListResponse(BaseModel):
    """Schema for bet list response."""
    total: int
    bets: list[BetResponse]


class BetStats(BaseModel):
    """Schema for bet statistics."""
    total_bets: int
    won_bets: int
    lost_bets: int
    pending_bets: int
    total_staked: Decimal
    total_profit: Decimal
    win_rate: Decimal
