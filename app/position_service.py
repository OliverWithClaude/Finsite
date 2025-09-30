"""Position management service for Finsite application."""

from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
import yfinance as yf
import logging

from app.database import Position, Trade

logger = logging.getLogger(__name__)


class PositionService:
    """Service for managing trading positions."""
    
    def create_position(
        self, 
        db: Session,
        ticker: str,
        entry_date: str,
        entry_value_eur: float,
        entry_price_per_share: float,
        entry_currency: str
    ) -> Position:
        """Create a new open position with buy trade."""
        ticker = ticker.upper().strip()
        
        # Validate currency
        if entry_currency not in ['EUR', 'USD']:
            raise ValueError("Currency must be EUR or USD")
        
        # Create position
        position = Position(
            ticker=ticker,
            status='OPEN',
            entry_date=entry_date,
            entry_value_eur=entry_value_eur,
            entry_price_per_share=entry_price_per_share,
            entry_currency=entry_currency
        )
        
        db.add(position)
        db.flush()  # Get the position ID
        
        # Create buy trade
        trade = Trade(
            position_id=position.id,
            ticker=ticker,
            trade_type='BUY',
            trade_date=entry_date,
            amount_eur=entry_value_eur,
            price_per_share=entry_price_per_share,
            currency=entry_currency
        )
        
        db.add(trade)
        db.commit()
        db.refresh(position)
        
        logger.info(f"Created open position for {ticker} with ID {position.id}")
        return position
    
    def close_position(
        self,
        db: Session,
        position_id: int,
        exit_date: str,
        exit_value_eur: float,
        exit_currency: str
    ) -> Position:
        """Close an existing position with sell trade."""
        position = db.query(Position).filter(Position.id == position_id).first()
        
        if not position:
            raise ValueError(f"Position {position_id} not found")
        
        if position.status != 'OPEN':
            raise ValueError(f"Position {position_id} is already closed")
        
        # Validate currency
        if exit_currency not in ['EUR', 'USD']:
            raise ValueError("Currency must be EUR or USD")
        
        # Calculate exit price per share based on entry ratio
        shares = position.entry_value_eur / position.entry_price_per_share
        exit_price_per_share = exit_value_eur / shares
        
        # Update position
        position.status = 'CLOSED'
        position.exit_date = exit_date
        position.exit_value_eur = exit_value_eur
        position.exit_currency = exit_currency
        
        # Create sell trade
        trade = Trade(
            position_id=position.id,
            ticker=position.ticker,
            trade_type='SELL',
            trade_date=exit_date,
            amount_eur=exit_value_eur,
            price_per_share=exit_price_per_share,
            currency=exit_currency
        )
        
        db.add(trade)
        db.commit()
        db.refresh(position)
        
        logger.info(f"Closed position {position_id} for {position.ticker}")
        return position
    
    def get_open_positions(self, db: Session) -> List[dict]:
        """Get all open positions with current valuations."""
        positions = db.query(Position).filter(Position.status == 'OPEN').all()
        
        result = []
        for pos in positions:
            pos_dict = pos.to_dict()
            
            # Get current price
            current_price = self._get_current_price(pos.ticker, pos.entry_currency)
            
            if current_price:
                # Calculate current value: (entry_value / entry_price) * current_price
                shares = pos.entry_value_eur / pos.entry_price_per_share
                current_value = shares * current_price
                unrealized_profit = current_value - pos.entry_value_eur
                unrealized_profit_pct = (unrealized_profit / pos.entry_value_eur) * 100
                
                pos_dict['current_price_per_share'] = round(current_price, 2)
                pos_dict['current_value_eur'] = round(current_value, 2)
                pos_dict['unrealized_profit_eur'] = round(unrealized_profit, 2)
                pos_dict['unrealized_profit_percent'] = round(unrealized_profit_pct, 2)
            else:
                pos_dict['current_price_per_share'] = None
                pos_dict['current_value_eur'] = None
                pos_dict['unrealized_profit_eur'] = None
                pos_dict['unrealized_profit_percent'] = None
            
            result.append(pos_dict)
        
        return result
    
    def get_closed_positions(self, db: Session) -> List[dict]:
        """Get all closed positions with P&L."""
        positions = db.query(Position).filter(Position.status == 'CLOSED').all()
        
        result = []
        for pos in positions:
            pos_dict = pos.to_dict()
            
            # Calculate profit/loss
            profit = pos.exit_value_eur - pos.entry_value_eur
            profit_pct = (profit / pos.entry_value_eur) * 100
            
            # Calculate holding period in days
            entry = datetime.strptime(pos.entry_date, '%Y-%m-%d')
            exit_dt = datetime.strptime(pos.exit_date, '%Y-%m-%d')
            holding_days = (exit_dt - entry).days
            
            pos_dict['profit_eur'] = round(profit, 2)
            pos_dict['profit_percent'] = round(profit_pct, 2)
            pos_dict['holding_period_days'] = holding_days
            
            result.append(pos_dict)
        
        return result
    
    def get_position(self, db: Session, position_id: int) -> Optional[Position]:
        """Get a single position by ID."""
        return db.query(Position).filter(Position.id == position_id).first()
    
    def _get_current_price(self, ticker: str, currency: str) -> Optional[float]:
        """Get current price for a ticker from yfinance."""
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Try to get current price
            price = info.get('currentPrice') or info.get('regularMarketPrice')
            
            if price and price > 0:
                return float(price)
            
            # Fallback: try getting latest price from history
            hist = stock.history(period='1d')
            if not hist.empty and 'Close' in hist.columns:
                return float(hist['Close'].iloc[-1])
            
            return None
            
        except Exception as e:
            logger.error(f"Error fetching current price for {ticker}: {e}")
            return None
