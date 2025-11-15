"""Wallet service."""
from decimal import Decimal
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
import stripe

from app.models.wallet import Wallet, Transaction, TransactionType, TransactionStatus
from app.core.config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


class WalletService:
    """Service for wallet operations."""

    @staticmethod
    def get_wallet(db: Session, user_id: int) -> Wallet:
        """
        Get user's wallet.

        Args:
            db: Database session
            user_id: User ID

        Returns:
            User's wallet

        Raises:
            HTTPException: If wallet not found
        """
        wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
        if not wallet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wallet not found"
            )
        return wallet

    @staticmethod
    async def deposit(db: Session, user_id: int, amount: Decimal, payment_method: str = "stripe") -> Transaction:
        """
        Deposit funds into wallet.

        Args:
            db: Database session
            user_id: User ID
            amount: Amount to deposit
            payment_method: Payment method (stripe, paypal)

        Returns:
            Transaction record

        Raises:
            HTTPException: If deposit fails
        """
        wallet = WalletService.get_wallet(db, user_id)

        # Create pending transaction
        transaction = Transaction(
            wallet_id=wallet.id,
            type=TransactionType.DEPOSIT,
            amount=amount,
            status=TransactionStatus.PENDING,
            description=f"Deposit via {payment_method}"
        )
        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        try:
            if payment_method == "stripe":
                # Create Stripe payment intent
                payment_intent = stripe.PaymentIntent.create(
                    amount=int(amount * 100),  # Convert to cents
                    currency=wallet.currency.lower(),
                    metadata={"transaction_id": transaction.id}
                )
                transaction.reference_id = payment_intent.id

            # Update wallet balance
            wallet.balance += amount
            transaction.status = TransactionStatus.COMPLETED

            db.commit()
            db.refresh(transaction)

        except Exception as e:
            transaction.status = TransactionStatus.FAILED
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Deposit failed: {str(e)}"
            )

        return transaction

    @staticmethod
    def withdraw(db: Session, user_id: int, amount: Decimal) -> Transaction:
        """
        Withdraw funds from wallet.

        Args:
            db: Database session
            user_id: User ID
            amount: Amount to withdraw

        Returns:
            Transaction record

        Raises:
            HTTPException: If withdrawal fails
        """
        wallet = WalletService.get_wallet(db, user_id)

        # Check balance
        if wallet.balance < amount:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient balance"
            )

        # Create transaction
        transaction = Transaction(
            wallet_id=wallet.id,
            type=TransactionType.WITHDRAWAL,
            amount=amount,
            status=TransactionStatus.PENDING,
            description="Withdrawal request"
        )

        # Update wallet balance
        wallet.balance -= amount

        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        return transaction

    @staticmethod
    def get_transactions(db: Session, user_id: int, skip: int = 0, limit: int = 100):
        """
        Get wallet transactions.

        Args:
            db: Database session
            user_id: User ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of transactions
        """
        wallet = WalletService.get_wallet(db, user_id)
        transactions = db.query(Transaction).filter(
            Transaction.wallet_id == wallet.id
        ).order_by(Transaction.created_at.desc()).offset(skip).limit(limit).all()

        return transactions


wallet_service = WalletService()
