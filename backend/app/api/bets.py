"""Betting routes."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.bet import BetCreate, BetResponse, BetListResponse, BetStats
from app.models.user import User
from app.models.bet import BetStatus
from app.api.dependencies import get_current_user
from app.services.betting import betting_service

router = APIRouter(prefix="/bets", tags=["bets"])


@router.post("", response_model=BetResponse, status_code=201)
def place_bet(
    bet_data: BetCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Place a new bet.

    Args:
        bet_data: Bet data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Created bet
    """
    bet = betting_service.place_bet(db, current_user, bet_data)
    return bet


@router.get("", response_model=BetListResponse)
def get_my_bets(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's bets.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        current_user: Current authenticated user
        db: Database session

    Returns:
        List of bets
    """
    result = betting_service.get_user_bets(db, current_user.id, skip, limit)
    return result


@router.get("/stats", response_model=BetStats)
def get_bet_stats(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get betting statistics for current user.

    Args:
        current_user: Current authenticated user
        db: Database session

    Returns:
        Bet statistics
    """
    from sqlalchemy import func
    from app.models.bet import Bet
    from decimal import Decimal

    # Get bet counts
    total_bets = db.query(func.count(Bet.id)).filter(Bet.user_id == current_user.id).scalar()
    won_bets = db.query(func.count(Bet.id)).filter(
        Bet.user_id == current_user.id,
        Bet.status == BetStatus.WON
    ).scalar()
    lost_bets = db.query(func.count(Bet.id)).filter(
        Bet.user_id == current_user.id,
        Bet.status == BetStatus.LOST
    ).scalar()
    pending_bets = db.query(func.count(Bet.id)).filter(
        Bet.user_id == current_user.id,
        Bet.status == BetStatus.PENDING
    ).scalar()

    # Get financial stats
    total_staked = db.query(func.sum(Bet.stake)).filter(Bet.user_id == current_user.id).scalar() or Decimal("0.00")
    total_won = db.query(func.sum(Bet.potential_payout)).filter(
        Bet.user_id == current_user.id,
        Bet.status == BetStatus.WON
    ).scalar() or Decimal("0.00")
    total_profit = total_won - total_staked

    # Calculate win rate
    win_rate = (won_bets / total_bets * 100) if total_bets > 0 else Decimal("0.00")

    return {
        "total_bets": total_bets,
        "won_bets": won_bets,
        "lost_bets": lost_bets,
        "pending_bets": pending_bets,
        "total_staked": total_staked,
        "total_profit": total_profit,
        "win_rate": round(win_rate, 2)
    }


@router.get("/{bet_id}", response_model=BetResponse)
def get_bet(
    bet_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get bet details.

    Args:
        bet_id: Bet ID
        current_user: Current authenticated user
        db: Database session

    Returns:
        Bet details
    """
    from fastapi import HTTPException, status
    from app.models.bet import Bet

    bet = db.query(Bet).filter(
        Bet.id == bet_id,
        Bet.user_id == current_user.id
    ).first()

    if not bet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bet not found"
        )

    return bet
