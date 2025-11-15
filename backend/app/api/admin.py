"""Admin routes."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.user import User
from app.models.bet import Bet
from app.schemas.user import UserResponse
from app.schemas.bet import BetResponse
from app.api.dependencies import get_current_admin
from app.services.betting import betting_service

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=List[UserResponse])
def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Get all users (admin only).

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        current_admin: Current admin user
        db: Database session

    Returns:
        List of users
    """
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.put("/users/{user_id}/deactivate", response_model=UserResponse)
def deactivate_user(
    user_id: int,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Deactivate a user (admin only).

    Args:
        user_id: User ID to deactivate
        current_admin: Current admin user
        db: Database session

    Returns:
        Updated user
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user.is_active = False
    db.commit()
    db.refresh(user)

    return user


@router.put("/users/{user_id}/activate", response_model=UserResponse)
def activate_user(
    user_id: int,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Activate a user (admin only).

    Args:
        user_id: User ID to activate
        current_admin: Current admin user
        db: Database session

    Returns:
        Updated user
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user.is_active = True
    db.commit()
    db.refresh(user)

    return user


@router.get("/bets", response_model=List[BetResponse])
def get_all_bets(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Get all bets (admin only).

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        current_admin: Current admin user
        db: Database session

    Returns:
        List of bets
    """
    bets = db.query(Bet).order_by(Bet.created_at.desc()).offset(skip).limit(limit).all()
    return bets


@router.put("/bets/{bet_id}/settle")
def settle_bet_admin(
    bet_id: int,
    won: bool,
    current_admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """
    Settle a bet (admin only).

    Args:
        bet_id: Bet ID to settle
        won: Whether the bet was won
        current_admin: Current admin user
        db: Database session

    Returns:
        Settled bet
    """
    bet = betting_service.settle_bet(db, bet_id, won)
    return bet
