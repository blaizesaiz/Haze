"""Betting service."""
from decimal import Decimal
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.models.bet import Bet, BetStatus
from app.models.sport import Event, Odds
from app.models.wallet import Wallet, Transaction, TransactionType, TransactionStatus
from app.schemas.bet import BetCreate


class BettingService:
    """Service for betting operations."""

    @staticmethod
    def place_bet(db: Session, user: User, bet_data: BetCreate) -> Bet:
        """
        Place a bet.

        Args:
            db: Database session
            user: User placing the bet
            bet_data: Bet data

        Returns:
            Created bet

        Raises:
            HTTPException: If bet cannot be placed
        """
        # Get event
        event = db.query(Event).filter(Event.id == bet_data.event_id).first()
        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )

        # Check if event is still open
        if event.is_completed:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Event has already completed"
            )

        # Get odds
        odds = db.query(Odds).filter(Odds.id == bet_data.odds_id).first()
        if not odds or not odds.is_active:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Odds not found or inactive"
            )

        # Get user wallet
        wallet = db.query(Wallet).filter(Wallet.user_id == user.id).first()
        if not wallet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Wallet not found"
            )

        # Check balance
        if wallet.balance < bet_data.stake:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient balance"
            )

        # Calculate potential payout
        potential_payout = bet_data.stake * Decimal(str(odds.price))

        # Create bet
        bet = Bet(
            user_id=user.id,
            event_id=event.id,
            odds_id=odds.id,
            stake=bet_data.stake,
            odds_value=odds.price,
            potential_payout=potential_payout,
            status=BetStatus.PENDING
        )

        db.add(bet)
        db.flush()  # Get bet ID

        # Deduct from wallet
        wallet.balance -= bet_data.stake

        # Create transaction
        transaction = Transaction(
            wallet_id=wallet.id,
            type=TransactionType.BET_PLACED,
            amount=bet_data.stake,
            status=TransactionStatus.COMPLETED,
            description=f"Bet placed on {event.home_team} vs {event.away_team}",
            bet_id=bet.id
        )

        db.add(transaction)
        db.commit()
        db.refresh(bet)

        return bet

    @staticmethod
    def settle_bet(db: Session, bet_id: int, won: bool) -> Bet:
        """
        Settle a bet.

        Args:
            db: Database session
            bet_id: Bet ID
            won: Whether the bet was won

        Returns:
            Settled bet

        Raises:
            HTTPException: If bet cannot be settled
        """
        bet = db.query(Bet).filter(Bet.id == bet_id).first()
        if not bet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Bet not found"
            )

        if bet.status != BetStatus.PENDING:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Bet has already been settled"
            )

        # Update bet status
        bet.status = BetStatus.WON if won else BetStatus.LOST
        bet.settled_at = db.query(Event).filter(Event.id == bet.event_id).first().updated_at

        # If won, credit wallet
        if won:
            wallet = db.query(Wallet).filter(Wallet.user_id == bet.user_id).first()
            wallet.balance += bet.potential_payout

            # Create transaction
            transaction = Transaction(
                wallet_id=wallet.id,
                type=TransactionType.BET_WON,
                amount=bet.potential_payout,
                status=TransactionStatus.COMPLETED,
                description=f"Bet won - payout",
                bet_id=bet.id
            )
            db.add(transaction)

        db.commit()
        db.refresh(bet)

        return bet

    @staticmethod
    def get_user_bets(db: Session, user_id: int, skip: int = 0, limit: int = 100):
        """
        Get user's bets.

        Args:
            db: Database session
            user_id: User ID
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of bets
        """
        bets = db.query(Bet).filter(Bet.user_id == user_id).order_by(Bet.created_at.desc()).offset(skip).limit(limit).all()
        total = db.query(Bet).filter(Bet.user_id == user_id).count()
        return {"bets": bets, "total": total}


betting_service = BettingService()
