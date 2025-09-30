"""Price history service for managing cached price data."""

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import yfinance as yf
import logging

from app.database import PriceHistory

logger = logging.getLogger(__name__)


class PriceHistoryService:
    """Service for managing price history data with caching."""
    
    def get_price_history(
        self, 
        db: Session, 
        ticker: str, 
        start_date: str, 
        end_date: str
    ) -> List[Dict[str, any]]:
        """
        Get price history for ticker in date range.
        Checks cache first, fetches missing data from yfinance.
        
        Args:
            db: Database session
            ticker: Ticker symbol
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
        
        Returns:
            List[dict]: [{"date": "2025-01-15", "close": 150.50}, ...]
        """
        ticker = ticker.upper().strip()
        
        # Convert string dates to datetime for comparison
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d')
        
        # Query database for cached data
        cached_prices = db.query(PriceHistory).filter(
            PriceHistory.ticker == ticker,
            PriceHistory.date >= start_date,
            PriceHistory.date <= end_date
        ).order_by(PriceHistory.date).all()
        
        # Convert to dict for easier lookup
        cached_dict = {price.date: price.close_price for price in cached_prices}
        
        # Generate all trading days in range (excluding weekends for now)
        all_dates = []
        current = start_dt
        while current <= end_dt:
            # Skip weekends (Saturday=5, Sunday=6)
            if current.weekday() < 5:
                all_dates.append(current.strftime('%Y-%m-%d'))
            current += timedelta(days=1)
        
        # Check if we have all the data we need
        missing_dates = [date for date in all_dates if date not in cached_dict]
        
        if missing_dates:
            logger.info(f"Missing {len(missing_dates)} price records for {ticker}, fetching from yfinance")
            
            try:
                # Fetch missing data from yfinance
                new_prices = self.fetch_from_yfinance(ticker, start_date, end_date)
                
                if new_prices:
                    # Store new data in database
                    self.store_prices(db, ticker, new_prices)
                    
                    # Update our cached dict
                    for price in new_prices:
                        cached_dict[price['date']] = price['close']
                    
                    logger.info(f"Stored {len(new_prices)} new price records for {ticker}")
            except Exception as e:
                logger.error(f"Error fetching prices for {ticker}: {e}")
                # Continue with whatever cached data we have
        
        # Build result from cached dict (now includes new data)
        result = []
        for date in sorted(cached_dict.keys()):
            if start_date <= date <= end_date:
                result.append({
                    "date": date,
                    "close": round(cached_dict[date], 2)
                })
        
        return result
    
    def fetch_from_yfinance(
        self, 
        ticker: str, 
        start_date: str, 
        end_date: str
    ) -> List[Dict[str, any]]:
        """
        Fetch price data from yfinance API.
        
        Args:
            ticker: Ticker symbol
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
        
        Returns:
            List[dict]: [{"date": "2025-01-15", "close": 150.50}, ...]
        """
        try:
            stock = yf.Ticker(ticker)
            
            # Add one day to end_date because yfinance is exclusive on end date
            end_dt = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
            end_date_inclusive = end_dt.strftime('%Y-%m-%d')
            
            # Fetch historical data
            hist = stock.history(start=start_date, end=end_date_inclusive)
            
            if hist.empty:
                logger.warning(f"No price data returned for {ticker}")
                return []
            
            # Convert to list of dicts
            prices = []
            for date, row in hist.iterrows():
                # Only get Close price
                if 'Close' in row and row['Close'] > 0:
                    prices.append({
                        "date": date.strftime('%Y-%m-%d'),
                        "close": float(row['Close'])
                    })
            
            logger.info(f"Fetched {len(prices)} price records for {ticker} from yfinance")
            return prices
            
        except Exception as e:
            logger.error(f"Error fetching from yfinance for {ticker}: {e}")
            return []
    
    def store_prices(
        self, 
        db: Session, 
        ticker: str, 
        prices: List[Dict[str, any]]
    ) -> None:
        """
        Store price data in database.
        Uses INSERT OR IGNORE to handle duplicates gracefully.
        
        Args:
            db: Database session
            ticker: Ticker symbol
            prices: List of price dicts [{"date": "2025-01-15", "close": 150.50}, ...]
        """
        ticker = ticker.upper().strip()
        
        for price in prices:
            # Check if already exists to avoid UniqueConstraint error
            existing = db.query(PriceHistory).filter(
                PriceHistory.ticker == ticker,
                PriceHistory.date == price['date']
            ).first()
            
            if not existing:
                price_record = PriceHistory(
                    ticker=ticker,
                    date=price['date'],
                    close_price=price['close']
                )
                db.add(price_record)
        
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            logger.error(f"Error storing prices for {ticker}: {e}")
            raise
