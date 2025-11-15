"""Social features schemas."""
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel

from app.schemas.user import UserResponse


class FollowCreate(BaseModel):
    """Schema for creating a follow relationship."""
    followed_id: int


class FollowResponse(BaseModel):
    """Schema for follow response."""
    id: int
    follower_id: int
    followed_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class LeaderboardEntryResponse(BaseModel):
    """Schema for leaderboard entry response."""
    id: int
    user_id: int
    user: UserResponse
    period: str
    total_bets: int
    won_bets: int
    total_staked: Decimal
    total_profit: Decimal
    win_rate: Decimal
    rank: int | None

    class Config:
        from_attributes = True


class LeaderboardResponse(BaseModel):
    """Schema for leaderboard response."""
    period: str
    entries: list[LeaderboardEntryResponse]
