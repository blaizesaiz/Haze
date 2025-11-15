"""Bet model."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum

from app.core.database import Base


class BetStatus(str, enum.Enum):
    """Bet status enumeration."""
    PENDING = "pending"
    WON = "won"
    LOST = "lost"
    VOID = "void"
    CASHED_OUT = "cashed_out"


class Bet(Base):
    """Bet model."""

    __tablename__ = "bets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    odds_id = Column(Integer, ForeignKey("odds.id", ondelete="CASCADE"), nullable=False)
    stake = Column(Numeric(10, 2), nullable=False)
    odds_value = Column(Numeric(10, 2), nullable=False)  # Snapshot of odds at bet time
    potential_payout = Column(Numeric(10, 2), nullable=False)
    status = Column(SQLEnum(BetStatus), default=BetStatus.PENDING, nullable=False)
    outcome = Column(String, nullable=True)  # Final outcome
    settled_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="bets")
    event = relationship("Event", back_populates="bets")
    odds = relationship("Odds", back_populates="bets")

    def __repr__(self):
        return f"<Bet user_id={self.user_id} stake={self.stake} status={self.status}>"
