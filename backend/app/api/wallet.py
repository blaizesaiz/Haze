"""Wallet routes."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.schemas.wallet import WalletResponse, TransactionResponse, DepositRequest, WithdrawalRequest
from app.models.user import User
from app.api.dependencies import get_current_user
from app.services.wallet import wallet_service

router = APIRouter(prefix="/wallet", tags=["wallet"])


@router.get("", response_model=WalletResponse)
def get_wallet(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's wallet.

    Args:
        current_user: Current authenticated user
        db: Database session

    Returns:
        User's wallet
    """
    wallet = wallet_service.get_wallet(db, current_user.id)
    return wallet


@router.post("/deposit", response_model=TransactionResponse)
async def deposit(
    deposit_data: DepositRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Deposit funds into wallet.

    Args:
        deposit_data: Deposit request data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Transaction record
    """
    transaction = await wallet_service.deposit(
        db,
        current_user.id,
        deposit_data.amount,
        deposit_data.payment_method
    )
    return transaction


@router.post("/withdraw", response_model=TransactionResponse)
def withdraw(
    withdrawal_data: WithdrawalRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Withdraw funds from wallet.

    Args:
        withdrawal_data: Withdrawal request data
        current_user: Current authenticated user
        db: Database session

    Returns:
        Transaction record
    """
    transaction = wallet_service.withdraw(db, current_user.id, withdrawal_data.amount)
    return transaction


@router.get("/transactions", response_model=List[TransactionResponse])
def get_transactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get wallet transaction history.

    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        current_user: Current authenticated user
        db: Database session

    Returns:
        List of transactions
    """
    transactions = wallet_service.get_transactions(db, current_user.id, skip, limit)
    return transactions
