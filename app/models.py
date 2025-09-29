"""Pydantic models for request/response validation."""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TickerBase(BaseModel):
    """Base ticker model."""
    symbol: str = Field(..., description="Ticker symbol (e.g., AAPL)")
    name: str = Field(..., description="Company name")


class TickerCreate(TickerBase):
    """Model for creating a new ticker."""
    pass


class TickerResponse(TickerBase):
    """Model for ticker response."""
    id: int
    added_date: datetime
    
    class Config:
        from_attributes = True


class TickerInfo(BaseModel):
    """Model for detailed ticker information from yfinance."""
    symbol: str
    name: str
    current_price: Optional[float] = None
    previous_close: Optional[float] = None
    change: Optional[float] = None
    change_percent: Optional[float] = None
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    week_52_high: Optional[float] = None
    week_52_low: Optional[float] = None
    volume: Optional[int] = None
    avg_volume: Optional[int] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    description: Optional[str] = None
    dividend_yield: Optional[float] = None
    beta: Optional[float] = None
    earnings_date: Optional[str] = None
    exchange: Optional[str] = None
    currency: Optional[str] = None
    website: Optional[str] = None
    error: Optional[str] = None
