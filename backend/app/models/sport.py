"""Sport, event, and odds models."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Numeric, JSON
from sqlalchemy.orm import relationship

from app.core.database import Base


class Sport(Base):
    """Sport model."""

    __tablename__ = "sports"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True, nullable=False)  # From The Odds API
    name = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    events = relationship("Event", back_populates="sport", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Sport {self.name}>"


class Event(Base):
    """Event/Game model."""

    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    sport_id = Column(Integer, ForeignKey("sports.id", ondelete="CASCADE"), nullable=False)
    external_id = Column(String, unique=True, index=True, nullable=False)  # From The Odds API
    home_team = Column(String, nullable=False)
    away_team = Column(String, nullable=False)
    commence_time = Column(DateTime, nullable=False)
    is_live = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)
    home_score = Column(Integer, nullable=True)
    away_score = Column(Integer, nullable=True)
    metadata = Column(JSON, nullable=True)  # Additional data from API
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    sport = relationship("Sport", back_populates="events")
    markets = relationship("Market", back_populates="event", cascade="all, delete-orphan")
    bets = relationship("Bet", back_populates="event", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Event {self.home_team} vs {self.away_team}>"


class Market(Base):
    """Betting market model (e.g., h2h, spreads, totals)."""

    __tablename__ = "markets"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False)
    key = Column(String, nullable=False)  # h2h, spreads, totals
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    event = relationship("Event", back_populates="markets")
    odds = relationship("Odds", back_populates="market", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Market {self.key}>"


class Odds(Base):
    """Odds model."""

    __tablename__ = "odds"

    id = Column(Integer, primary_key=True, index=True)
    market_id = Column(Integer, ForeignKey("markets.id", ondelete="CASCADE"), nullable=False)
    bookmaker = Column(String, nullable=False)
    outcome = Column(String, nullable=False)  # Team name or Over/Under
    price = Column(Numeric(10, 2), nullable=False)  # Decimal odds
    point = Column(Numeric(10, 2), nullable=True)  # Spread/total points
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    market = relationship("Market", back_populates="odds")
    bets = relationship("Bet", back_populates="odds")

    def __repr__(self):
        return f"<Odds {self.outcome} @ {self.price}>"
