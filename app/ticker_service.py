"""Service for fetching ticker information using yfinance - ULTRA ROBUST VERSION."""

import yfinance as yf
from typing import Optional, Dict, Any
from app.models import TickerInfo
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Configure logging for better debugging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Known problematic symbols that yfinance might incorrectly validate
BLACKLISTED_SYMBOLS = {
    'TEST', 'TESTS', 'TESTING', 'DEMO', 'DUMMY', 'FAKE', 'SAMPLE',
    'EXAMPLE', 'XXX', 'ABC', 'XYZ', 'TEMP', 'TMP', 'NULL', 'NONE'
}

class TickerService:
    """Service for fetching stock information with ultra-robust validation."""
    
    @staticmethod
    def validate_symbol(symbol: str) -> bool:
        """
        Validate if a ticker symbol exists - ULTRA ROBUST VERSION
        Uses multiple validation methods and filters out false positives
        """
        if not symbol or not symbol.strip():
            logger.warning("Empty symbol provided")
            return False
        
        symbol = symbol.upper().strip()
        
        # Check against blacklist first
        if symbol in BLACKLISTED_SYMBOLS:
            logger.info(f"Symbol {symbol}: Blacklisted")
            return False
        
        # Check for obviously invalid patterns
        if symbol.isdigit() or len(symbol) > 10:
            logger.info(f"Symbol {symbol}: Invalid pattern")
            return False
        
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Check 1: If info dict is essentially empty
            if not info or len(info) <= 1:
                logger.debug(f"Symbol {symbol}: Empty info dict")
                return False
            
            # Check 2: Look for actual trading data
            has_real_price = False
            price_value = None
            
            # Check multiple price fields
            for price_field in ['currentPrice', 'regularMarketPrice', 'previousClose', 'ask', 'bid']:
                price = info.get(price_field)
                if price and isinstance(price, (int, float)) and price > 0:
                    has_real_price = True
                    price_value = price
                    break
            
            # Check 3: Verify it's a real exchange
            exchange = info.get('exchange')
            valid_exchanges = {
                'NMS', 'NGM', 'NCM', 'NYQ', 'NYSE', 'NASDAQ', 'AMEX', 'BATS',
                'LSE', 'TSE', 'TSX', 'FRA', 'ETR', 'PAR', 'AMS', 'SWX',
                'HKG', 'SGX', 'NSE', 'BSE', 'ASX', 'NZE', 'JSE'
            }
            
            has_valid_exchange = exchange and any(ex in str(exchange).upper() for ex in valid_exchanges)
            
            # Check 4: Has actual company information
            has_company_info = any([
                info.get('shortName'),
                info.get('longName'),
                info.get('sector'),
                info.get('industry')
            ])
            
            # Check 5: Has market cap or enterprise value (real companies have these)
            has_valuation = any([
                info.get('marketCap') and info.get('marketCap') > 0,
                info.get('enterpriseValue') and info.get('enterpriseValue') > 0
            ])
            
            # Check 6: Quote type should be EQUITY, ETF, MUTUALFUND, or other valid types
            quote_type = info.get('quoteType')
            valid_quote_types = {'EQUITY', 'ETF', 'MUTUALFUND', 'INDEX', 'CURRENCY', 'CRYPTOCURRENCY'}
            has_valid_quote_type = quote_type in valid_quote_types
            
            # Scoring system: Count how many validation criteria are met
            validation_score = sum([
                has_real_price,
                has_valid_exchange,
                has_company_info,
                has_valuation,
                has_valid_quote_type,
                len(info) > 20  # Substantial data
            ])
            
            # Need at least 3 out of 6 criteria for validation
            is_valid = validation_score >= 3
            
            # Additional check: Try to get recent history as final validation
            if is_valid:
                try:
                    history = ticker.history(period="5d")
                    if history.empty:
                        logger.debug(f"Symbol {symbol}: No recent history, might be delisted")
                        # Still valid if other criteria are strong
                        is_valid = validation_score >= 4
                except:
                    pass
            
            if is_valid:
                logger.info(f"Symbol {symbol}: VALID (score: {validation_score}/6, price: {price_value})")
            else:
                logger.info(f"Symbol {symbol}: INVALID (score: {validation_score}/6)")
            
            return is_valid
            
        except Exception as e:
            logger.error(f"Error validating symbol {symbol}: {e}")
            return False
    
    @staticmethod
    def get_company_name(symbol: str) -> Optional[str]:
        """
        Get the company name for a symbol.
        Used when validating to auto-fill the name field.
        """
        try:
            ticker = yf.Ticker(symbol.upper())
            info = ticker.info
            
            # Try different name fields in order of preference
            name = (
                info.get('longName') or 
                info.get('shortName') or 
                info.get('name') or
                None
            )
            
            # If no name found but symbol is valid, return symbol itself
            if not name and TickerService.validate_symbol(symbol):
                name = symbol.upper()
            
            return name
            
        except Exception as e:
            logger.error(f"Error getting company name for {symbol}: {e}")
            return None
    
    @staticmethod
    def get_ticker_info(symbol: str) -> TickerInfo:
        """Fetch detailed information about a ticker with improved error handling."""
        symbol = symbol.upper().strip()
        
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # If info is empty or minimal, return error
            if not info or len(info) <= 1:
                logger.warning(f"No data available for {symbol}")
                return TickerInfo(
                    symbol=symbol,
                    name=symbol,
                    error="No data available for this ticker"
                )
            
            # Get price information with multiple fallback options
            current_price = None
            for price_field in ['currentPrice', 'regularMarketPrice', 'price', 'ask', 'bid']:
                price = info.get(price_field)
                if price and isinstance(price, (int, float)) and price > 0:
                    current_price = price
                    break
            
            previous_close = (
                info.get('previousClose') or
                info.get('regularMarketPreviousClose') or
                None
            )
            
            # Validate prices are reasonable
            if previous_close and isinstance(previous_close, (int, float)):
                if previous_close <= 0 or previous_close > 1000000:
                    previous_close = None
            
            # Calculate price change
            change = None
            change_percent = None
            if current_price and previous_close:
                try:
                    change = round(current_price - previous_close, 2)
                    change_percent = round((change / previous_close) * 100, 2)
                except (TypeError, ZeroDivisionError):
                    pass
            
            # Get company name with fallbacks
            company_name = (
                info.get('longName') or
                info.get('shortName') or
                info.get('name') or
                symbol
            )
            
            # Format earnings date if available
            earnings_date = None
            earnings_dates = info.get('earningsDate') or info.get('earningsTimestamp')
            if earnings_dates:
                try:
                    if isinstance(earnings_dates, list) and len(earnings_dates) > 0:
                        earnings_date = datetime.fromtimestamp(earnings_dates[0]).strftime('%Y-%m-%d')
                    elif isinstance(earnings_dates, (int, float)):
                        earnings_date = datetime.fromtimestamp(earnings_dates).strftime('%Y-%m-%d')
                except Exception as e:
                    logger.debug(f"Error parsing earnings date: {e}")
            
            # Get 52-week range with validation
            week_52_high = info.get('fiftyTwoWeekHigh') or info.get('yearHigh')
            week_52_low = info.get('fiftyTwoWeekLow') or info.get('yearLow')
            
            # Validate 52-week values
            if week_52_high and isinstance(week_52_high, (int, float)):
                if week_52_high <= 0 or week_52_high > 1000000:
                    week_52_high = None
            
            if week_52_low and isinstance(week_52_low, (int, float)):
                if week_52_low <= 0 or week_52_low > 1000000:
                    week_52_low = None
            
            # Get volume with validation
            volume = info.get('volume') or info.get('regularMarketVolume')
            if volume and isinstance(volume, (int, float)):
                if volume < 0:
                    volume = None
            
            avg_volume = info.get('averageVolume') or info.get('averageVolume10days')
            if avg_volume and isinstance(avg_volume, (int, float)):
                if avg_volume < 0:
                    avg_volume = None
            
            # Build response
            return TickerInfo(
                symbol=symbol,
                name=company_name,
                current_price=current_price,
                previous_close=previous_close,
                change=change,
                change_percent=change_percent,
                market_cap=info.get('marketCap') if info.get('marketCap') and info.get('marketCap') > 0 else None,
                pe_ratio=info.get('trailingPE') or info.get('forwardPE'),
                week_52_high=week_52_high,
                week_52_low=week_52_low,
                volume=volume,
                avg_volume=avg_volume,
                sector=info.get('sector'),
                industry=info.get('industry'),
                description=info.get('longBusinessSummary') or info.get('description'),
                dividend_yield=info.get('dividendYield') or info.get('trailingAnnualDividendYield'),
                beta=info.get('beta') or info.get('beta3Year'),
                earnings_date=earnings_date,
                exchange=info.get('exchange') or info.get('fullExchangeName'),
                currency=info.get('currency') or info.get('financialCurrency') or 'USD',
                website=info.get('website')
            )
            
        except Exception as e:
            logger.error(f"Error fetching info for {symbol}: {str(e)}")
            return TickerInfo(
                symbol=symbol,
                name=symbol,
                error=f"Unable to fetch data: {str(e)}"
            )
    
    @staticmethod
    def search_ticker(query: str) -> Optional[Dict[str, Any]]:
        """
        Search for a ticker symbol by company name.
        Note: yfinance doesn't have built-in search, so this validates the query as a symbol
        """
        if not query:
            return None
            
        query = query.upper().strip()
        
        try:
            # Try to validate as a direct symbol
            if TickerService.validate_symbol(query):
                name = TickerService.get_company_name(query)
                if name:
                    return {
                        'symbol': query,
                        'name': name
                    }
            
            return None
            
        except Exception as e:
            logger.error(f"Error searching for {query}: {e}")
            return None
    
    @staticmethod
    def test_symbol(symbol: str) -> Dict[str, Any]:
        """
        Test function for debugging symbol validation issues.
        Returns detailed information about validation attempts.
        """
        result = {
            'symbol': symbol,
            'is_valid': False,
            'is_blacklisted': symbol.upper() in BLACKLISTED_SYMBOLS,
            'validation_score': 0,
            'company_name': None,
            'data_points': 0,
            'has_price': False,
            'has_valid_exchange': False,
            'has_company_info': False,
            'has_valuation': False,
            'has_valid_quote_type': False,
            'has_history': False,
            'errors': []
        }
        
        if result['is_blacklisted']:
            result['errors'].append('Symbol is blacklisted')
            return result
        
        try:
            ticker = yf.Ticker(symbol.upper())
            info = ticker.info
            
            result['data_points'] = len(info) if info else 0
            
            if info:
                # Check each validation criterion
                # Price check
                for price_field in ['currentPrice', 'regularMarketPrice', 'previousClose']:
                    price = info.get(price_field)
                    if price and isinstance(price, (int, float)) and price > 0:
                        result['has_price'] = True
                        break
                
                # Exchange check
                exchange = info.get('exchange')
                if exchange:
                    valid_exchanges = {'NMS', 'NGM', 'NCM', 'NYQ', 'NYSE', 'NASDAQ', 'AMEX'}
                    result['has_valid_exchange'] = any(ex in str(exchange).upper() for ex in valid_exchanges)
                
                # Company info check
                result['has_company_info'] = any([
                    info.get('shortName'),
                    info.get('longName'),
                    info.get('sector')
                ])
                
                # Valuation check
                result['has_valuation'] = bool(info.get('marketCap') and info.get('marketCap') > 0)
                
                # Quote type check
                quote_type = info.get('quoteType')
                result['has_valid_quote_type'] = quote_type in {'EQUITY', 'ETF', 'MUTUALFUND', 'INDEX'}
                
                # History check
                try:
                    history = ticker.history(period="5d")
                    result['has_history'] = not history.empty
                except:
                    result['has_history'] = False
                
                # Calculate validation score
                result['validation_score'] = sum([
                    result['has_price'],
                    result['has_valid_exchange'],
                    result['has_company_info'],
                    result['has_valuation'],
                    result['has_valid_quote_type'],
                    result['data_points'] > 20
                ])
                
                # Get company name
                result['company_name'] = (
                    info.get('longName') or
                    info.get('shortName') or
                    info.get('symbol')
                )
            
            result['is_valid'] = TickerService.validate_symbol(symbol)
            
        except Exception as e:
            result['errors'].append(str(e))
        
        return result
