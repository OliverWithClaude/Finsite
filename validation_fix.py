
# IMPROVED VALIDATION FOR app/ticker_service.py
# Replace the validate_symbol method with this version:

@staticmethod
def validate_symbol(symbol: str) -> bool:
    """Validate if a ticker symbol exists - IMPROVED VERSION"""
    if not symbol or not symbol.strip():
        return False
        
    try:
        ticker = yf.Ticker(symbol.upper())
        info = ticker.info
        
        # Check 1: If info dict is essentially empty or just has an error
        if not info or len(info) <= 1:
            logger.debug(f"Symbol {symbol}: Empty info dict")
            return False
        
        # Check 2: Look for error patterns in the response
        # yfinance returns minimal data for invalid symbols
        if len(info) <= 5 and not any([
            info.get('symbol'),
            info.get('shortName'),
            info.get('longName')
        ]):
            logger.debug(f"Symbol {symbol}: Minimal data, likely invalid")
            return False
        
        # Check 3: Look for key identifying fields
        has_identity = any([
            info.get('symbol'),
            info.get('shortName'),
            info.get('longName'),
            info.get('exchange'),
            info.get('quoteType')
        ])
        
        # Check 4: Look for price data as additional validation
        has_price = any([
            info.get('currentPrice'),
            info.get('regularMarketPrice'),
            info.get('previousClose'),
            info.get('bid'),
            info.get('ask')
        ])
        
        # Valid if we have identity fields OR substantial data with price
        is_valid = has_identity or (len(info) > 10 and has_price)
        
        if is_valid:
            logger.info(f"Symbol {symbol}: Valid (fields: {len(info)})")
        else:
            logger.info(f"Symbol {symbol}: Invalid")
            
        return is_valid
        
    except Exception as e:
        logger.error(f"Error validating symbol {symbol}: {e}")
        return False
