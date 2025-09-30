"""Database models for Finsite application."""

from sqlalchemy import create_engine, Column, String, DateTime, Float, Integer, ForeignKey, UniqueConstraint, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# Get the absolute path to the data directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'data', 'finsite.db')}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Ticker(Base):
    """Model for storing ticker symbols."""
    __tablename__ = "tickers"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    added_date = Column(DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            "id": self.id,
            "symbol": self.symbol,
            "name": self.name,
            "added_date": self.added_date.isoformat() if self.added_date else None
        }


class Position(Base):
    """Model for storing trading positions."""
    __tablename__ = "positions"
    
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, index=True, nullable=False)
    status = Column(String, nullable=False)  # 'OPEN' or 'CLOSED'
    entry_date = Column(String, nullable=False)
    entry_value_eur = Column(Float, nullable=False)
    entry_price_per_share = Column(Float, nullable=False)
    entry_currency = Column(String, nullable=False)  # 'EUR' or 'USD'
    exit_date = Column(String, nullable=True)
    exit_value_eur = Column(Float, nullable=True)
    exit_currency = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    trades = relationship("Trade", back_populates="position", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            "id": self.id,
            "ticker": self.ticker,
            "status": self.status,
            "entry_date": self.entry_date,
            "entry_value_eur": self.entry_value_eur,
            "entry_price_per_share": self.entry_price_per_share,
            "entry_currency": self.entry_currency,
            "exit_date": self.exit_date,
            "exit_value_eur": self.exit_value_eur,
            "exit_currency": self.exit_currency,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class Trade(Base):
    """Model for storing individual trades."""
    __tablename__ = "trades"
    
    id = Column(Integer, primary_key=True, index=True)
    position_id = Column(Integer, ForeignKey("positions.id"), nullable=False)
    ticker = Column(String, nullable=False)
    trade_type = Column(String, nullable=False)  # 'BUY' or 'SELL'
    trade_date = Column(String, nullable=False)
    amount_eur = Column(Float, nullable=False)
    price_per_share = Column(Float, nullable=False)
    currency = Column(String, nullable=False)  # 'EUR' or 'USD'
    created_at = Column(DateTime, default=datetime.utcnow)
    
    position = relationship("Position", back_populates="trades")
    
    def to_dict(self):
        return {
            "id": self.id,
            "position_id": self.position_id,
            "ticker": self.ticker,
            "trade_type": self.trade_type,
            "trade_date": self.trade_date,
            "amount_eur": self.amount_eur,
            "price_per_share": self.price_per_share,
            "currency": self.currency,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class PriceHistory(Base):
    """Model for storing historical price data (cached from yfinance)."""
    __tablename__ = "price_history"
    
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, nullable=False, index=True)
    date = Column(String, nullable=False)  # Format: YYYY-MM-DD
    close_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        UniqueConstraint('ticker', 'date', name='uix_ticker_date'),
        Index('idx_price_history_ticker_date', 'ticker', 'date'),
    )
    
    def to_dict(self):
        return {
            "id": self.id,
            "ticker": self.ticker,
            "date": self.date,
            "close_price": self.close_price,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


# Create tables
Base.metadata.create_all(bind=engine)


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
