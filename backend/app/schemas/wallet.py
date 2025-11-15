"""Wallet and transaction schemas."""
from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, Field

from app.models.wallet import TransactionType, TransactionStatus


class WalletBase(BaseModel):
    """Base wallet schema."""
    balance: Decimal = Field(default=Decimal("0.00"), ge=0)
    currency: str = "USD"


class WalletResponse(WalletBase):
    """Schema for wallet response."""
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TransactionCreate(BaseModel):
    """Schema for creating a transaction."""
    type: TransactionType
    amount: Decimal = Field(..., gt=0)
    description: Optional[str] = None
    reference_id: Optional[str] = None


class TransactionResponse(BaseModel):
    """Schema for transaction response."""
    id: int
    wallet_id: int
    type: TransactionType
    amount: Decimal
    status: TransactionStatus
    description: Optional[str]
    reference_id: Optional[str]
    bet_id: Optional[int]
    created_at: datetime

    class Config:
        from_attributes = True


class DepositRequest(BaseModel):
    """Schema for deposit request."""
    amount: Decimal = Field(..., gt=0, le=10000)
    payment_method: str = "stripe"


class WithdrawalRequest(BaseModel):
    """Schema for withdrawal request."""
    amount: Decimal = Field(..., gt=0)
