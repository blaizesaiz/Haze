"""Authentication service."""
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.models.wallet import Wallet
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token


class AuthService:
    """Service for authentication operations."""

    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """
        Create a new user with a wallet.

        Args:
            db: Database session
            user_data: User creation data

        Returns:
            Created user

        Raises:
            HTTPException: If user already exists
        """
        # Check if user exists
        existing_user = db.query(User).filter(
            (User.email == user_data.email) | (User.username == user_data.username)
        ).first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email or username already exists"
            )

        # Create user
        user = User(
            email=user_data.email,
            username=user_data.username,
            full_name=user_data.full_name,
            hashed_password=get_password_hash(user_data.password)
        )

        db.add(user)
        db.flush()  # Get user ID

        # Create wallet for user
        wallet = Wallet(user_id=user.id, balance=0.00)
        db.add(wallet)

        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> User:
        """
        Authenticate a user.

        Args:
            db: Database session
            username: Username
            password: Password

        Returns:
            Authenticated user

        Raises:
            HTTPException: If credentials are invalid
        """
        user = db.query(User).filter(User.username == username).first()

        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )

        # Update last login
        user.last_login = datetime.utcnow()
        db.commit()

        return user

    @staticmethod
    def create_tokens(user_id: int) -> dict:
        """
        Create access and refresh tokens for a user.

        Args:
            user_id: User ID

        Returns:
            Dictionary with access and refresh tokens
        """
        access_token = create_access_token(data={"sub": str(user_id)})
        refresh_token = create_refresh_token(data={"sub": str(user_id)})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }


auth_service = AuthService()
