"""Social features models."""
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base


class Following(Base):
    """Following/follower relationship model."""

    __tablename__ = "followings"

    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    followed_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    follower = relationship("User", foreign_keys=[follower_id], back_populates="following")
    followed = relationship("User", foreign_keys=[followed_id], back_populates="followers")

    # Ensure unique follower-followed pairs
    __table_args__ = (
        UniqueConstraint('follower_id', 'followed_id', name='unique_follow'),
    )

    def __repr__(self):
        return f"<Following follower={self.follower_id} followed={self.followed_id}>"


class LeaderboardEntry(Base):
    """Leaderboard entry model."""

    __tablename__ = "leaderboard_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    period = Column(String, nullable=False)  # daily, weekly, monthly, all_time
    total_bets = Column(Integer, default=0)
    won_bets = Column(Integer, default=0)
    total_staked = Column(Numeric(10, 2), default=0.00)
    total_profit = Column(Numeric(10, 2), default=0.00)
    win_rate = Column(Numeric(5, 2), default=0.00)  # Percentage
    rank = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="leaderboard_entries")

    # Ensure unique user-period pairs
    __table_args__ = (
        UniqueConstraint('user_id', 'period', name='unique_user_period'),
    )

    def __repr__(self):
        return f"<LeaderboardEntry user={self.user_id} period={self.period} rank={self.rank}>"
