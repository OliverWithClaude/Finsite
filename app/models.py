"""Pydantic models for request/response validation."""

from pydantic import BaseModel, Field
from typing import Optional, List
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


class PositionCreate(BaseModel):
    """Model for creating a new position (buy trade)."""
    ticker: str = Field(..., description="Ticker symbol")
    entry_date: str = Field(..., description="Entry date (YYYY-MM-DD)")
    entry_value_eur: float = Field(..., gt=0, description="Total entry value in EUR")
    entry_price_per_share: float = Field(..., gt=0, description="Price per share at entry")
    entry_currency: str = Field(..., description="Currency of entry price (EUR or USD)")


class PositionClose(BaseModel):
    """Model for closing a position (sell trade)."""
    exit_date: str = Field(..., description="Exit date (YYYY-MM-DD)")
    exit_value_eur: float = Field(..., gt=0, description="Total exit value in EUR")
    exit_currency: str = Field(..., description="Currency of exit price (EUR or USD)")


class PositionResponse(BaseModel):
    """Model for position response."""
    id: int
    ticker: str
    status: str
    entry_date: str
    entry_value_eur: float
    entry_price_per_share: float
    entry_currency: str
    exit_date: Optional[str] = None
    exit_value_eur: Optional[float] = None
    exit_currency: Optional[str] = None
    created_at: str
    
    class Config:
        from_attributes = True


class OpenPositionDetail(PositionResponse):
    """Model for open position with current valuation."""
    current_price_per_share: Optional[float] = None
    current_value_eur: Optional[float] = None
    unrealized_profit_eur: Optional[float] = None
    unrealized_profit_percent: Optional[float] = None


class ClosedPositionDetail(PositionResponse):
    """Model for closed position with P&L."""
    profit_eur: float
    profit_percent: float
    holding_period_days: int


class ChartDataPoint(BaseModel):
    """Single price data point."""
    date: str
    close: float


class PositionChartData(BaseModel):
    """Chart data for a position."""
    ticker: str
    entry_date: str
    exit_date: str
    entry_price: float
    exit_price: float
    entry_currency: str
    start_date: str
    end_date: str
    prices: List[ChartDataPoint]
    error: Optional[str] = None
