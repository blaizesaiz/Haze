"""Social features routes."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.social import FollowCreate, FollowResponse, LeaderboardResponse, LeaderboardEntryResponse
from app.schemas.user import UserResponse
from app.models.user import User
from app.models.social import Following, LeaderboardEntry
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/social", tags=["social"])


@router.post("/follow", response_model=FollowResponse, status_code=status.HTTP_201_CREATED)
def follow_user(
    follow_data: FollowCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Follow a user.

    Args:
        follow_data: Follow data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Follow relationship
    """
    # Check if user exists
    user_to_follow = db.query(User).filter(User.id == follow_data.followed_id).first()
    if not user_to_follow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Check if already following
    existing_follow = db.query(Following).filter(
        Following.follower_id == current_user.id,
        Following.followed_id == follow_data.followed_id
    ).first()

    if existing_follow:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Already following this user"
        )

    # Create follow relationship
    follow = Following(
        follower_id=current_user.id,
        followed_id=follow_data.followed_id
    )

    db.add(follow)
    db.commit()
    db.refresh(follow)

    return follow


@router.delete("/unfollow/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def unfollow_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Unfollow a user.

    Args:
        user_id: User ID to unfollow
        current_user: Current authenticated user
        db: Database session
    """
    follow = db.query(Following).filter(
        Following.follower_id == current_user.id,
        Following.followed_id == user_id
    ).first()

    if not follow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not following this user"
        )

    db.delete(follow)
    db.commit()


@router.get("/following", response_model=List[UserResponse])
def get_following(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get users that current user is following.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        current_user: Current authenticated user
        db: Database session

    Returns:
        List of users
    """
    follows = db.query(Following).filter(
        Following.follower_id == current_user.id
    ).offset(skip).limit(limit).all()

    user_ids = [f.followed_id for f in follows]
    users = db.query(User).filter(User.id.in_(user_ids)).all()

    return users


@router.get("/followers", response_model=List[UserResponse])
def get_followers(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's followers.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        current_user: Current authenticated user
        db: Database session

    Returns:
        List of users
    """
    follows = db.query(Following).filter(
        Following.followed_id == current_user.id
    ).offset(skip).limit(limit).all()

    user_ids = [f.follower_id for f in follows]
    users = db.query(User).filter(User.id.in_(user_ids)).all()

    return users


@router.get("/leaderboard", response_model=LeaderboardResponse)
def get_leaderboard(
    period: str = Query("all_time", regex="^(daily|weekly|monthly|all_time)$"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    Get leaderboard.

    Args:
        period: Time period (daily, weekly, monthly, all_time)
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session

    Returns:
        Leaderboard entries
    """
    entries = db.query(LeaderboardEntry).filter(
        LeaderboardEntry.period == period
    ).order_by(LeaderboardEntry.rank).offset(skip).limit(limit).all()

    return {"period": period, "entries": entries}


@router.post("/leaderboard/update", status_code=status.HTTP_200_OK)
async def update_leaderboard(db: Session = Depends(get_db)):
    """
    Update leaderboard rankings.

    Args:
        db: Database session

    Returns:
        Success message
    """
    from sqlalchemy import func
    from app.models.bet import Bet, BetStatus
    from decimal import Decimal

    periods = ["daily", "weekly", "monthly", "all_time"]

    for period in periods:
        # Get all users with bets
        user_stats = db.query(
            Bet.user_id,
            func.count(Bet.id).label("total_bets"),
            func.sum(func.case((Bet.status == BetStatus.WON, 1), else_=0)).label("won_bets"),
            func.sum(Bet.stake).label("total_staked"),
            func.sum(func.case((Bet.status == BetStatus.WON, Bet.potential_payout), else_=0)).label("total_won")
        ).group_by(Bet.user_id).all()

        for idx, stats in enumerate(user_stats, start=1):
            total_profit = (stats.total_won or Decimal("0.00")) - (stats.total_staked or Decimal("0.00"))
            win_rate = (stats.won_bets / stats.total_bets * 100) if stats.total_bets > 0 else Decimal("0.00")

            entry = db.query(LeaderboardEntry).filter(
                LeaderboardEntry.user_id == stats.user_id,
                LeaderboardEntry.period == period
            ).first()

            if not entry:
                entry = LeaderboardEntry(
                    user_id=stats.user_id,
                    period=period
                )
                db.add(entry)

            entry.total_bets = stats.total_bets
            entry.won_bets = stats.won_bets
            entry.total_staked = stats.total_staked or Decimal("0.00")
            entry.total_profit = total_profit
            entry.win_rate = round(win_rate, 2)
            entry.rank = idx

    db.commit()
    return {"message": "Leaderboard updated successfully"}
