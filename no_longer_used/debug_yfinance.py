"""
Finsite - yfinance Debugging Script
Tests and debugs the yfinance integration for symbol validation issues
"""

import yfinance as yf
import json
from datetime import datetime
import sys
import time
from typing import Dict, Any, List

# Test configuration
TEST_SYMBOLS = [
    # Valid symbols
    "AAPL",    # Apple
    "MSFT",    # Microsoft
    "GOOGL",   # Google
    "TSLA",    # Tesla
    "AMZN",    # Amazon
    "META",    # Meta/Facebook
    "NVDA",    # NVIDIA
    "BRK-B",   # Berkshire Hathaway Class B (with hyphen)
    "JPM",     # JPMorgan Chase
    "V",       # Visa
    
    # International symbols
    "NESN.SW", # Nestle (Swiss)
    "MC.PA",   # LVMH (Paris)
    "ASML",    # ASML (Amsterdam)
    "TSM",     # Taiwan Semiconductor
    "BABA",    # Alibaba
    "NVO",     # Novo Nordisk
    
    # ETFs
    "SPY",     # SPDR S&P 500
    "QQQ",     # Invesco QQQ
    "VTI",     # Vanguard Total Stock Market
    
    # Invalid/Test symbols
    "INVALID123",
    "XXXXXX",
    "TEST",
    "",         # Empty
    "123",      # Numbers only
]

class Colors:
    """Terminal colors for better output readability"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(text: str):
    """Print a formatted header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")

def print_success(text: str):
    """Print success message"""
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text: str):
    """Print error message"""
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_warning(text: str):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def print_info(text: str):
    """Print info message"""
    print(f"{Colors.CYAN}ℹ {text}{Colors.END}")

def test_yfinance_version():
    """Check yfinance version and dependencies"""
    print_header("yfinance Version Check")
    
    try:
        print(f"yfinance version: {yf.__version__}")
        
        # Check for required attributes
        required_attrs = ['Ticker', 'download', 'Tickers']
        for attr in required_attrs:
            if hasattr(yf, attr):
                print_success(f"yfinance.{attr} available")
            else:
                print_error(f"yfinance.{attr} not found")
        
        return True
    except Exception as e:
        print_error(f"Error checking yfinance: {e}")
        return False

def debug_ticker_validation(symbol: str) -> Dict[str, Any]:
    """
    Detailed debugging of a single ticker symbol
    Returns detailed information about the validation attempt
    """
    result = {
        'symbol': symbol,
        'valid': False,
        'method_results': {},
        'data': {},
        'errors': []
    }
    
    print(f"\n{Colors.BOLD}Testing: {symbol}{Colors.END}")
    print("-" * 40)
    
    try:
        ticker = yf.Ticker(symbol)
        
        # Method 1: Check info dictionary
        print_info("Method 1: Checking ticker.info...")
        try:
            info = ticker.info
            result['data']['info'] = info
            
            # Check various fields that indicate validity
            validation_fields = {
                'symbol': info.get('symbol'),
                'shortName': info.get('shortName'),
                'longName': info.get('longName'),
                'currency': info.get('currency'),
                'exchange': info.get('exchange'),
                'quoteType': info.get('quoteType'),
                'marketState': info.get('marketState')
            }
            
            # Remove None values for cleaner output
            validation_fields = {k: v for k, v in validation_fields.items() if v is not None}
            
            if validation_fields:
                print_success(f"Found {len(validation_fields)} validation fields:")
                for field, value in validation_fields.items():
                    print(f"  • {field}: {value}")
                result['method_results']['info'] = True
                result['valid'] = True
            else:
                print_warning("No validation fields found in info")
                result['method_results']['info'] = False
                
        except Exception as e:
            print_error(f"Error getting info: {e}")
            result['errors'].append(f"Info error: {e}")
            result['method_results']['info'] = False
        
        # Method 2: Check history
        print_info("Method 2: Checking ticker.history...")
        try:
            history = ticker.history(period="1d")
            
            if not history.empty:
                print_success(f"History data available: {len(history)} rows")
                print(f"  • Latest date: {history.index[-1] if len(history) > 0 else 'N/A'}")
                print(f"  • Columns: {', '.join(history.columns.tolist())}")
                result['method_results']['history'] = True
                result['valid'] = True
                result['data']['history_shape'] = history.shape
            else:
                print_warning("History is empty")
                result['method_results']['history'] = False
                
        except Exception as e:
            print_error(f"Error getting history: {e}")
            result['errors'].append(f"History error: {e}")
            result['method_results']['history'] = False
        
        # Method 3: Check fast_info
        print_info("Method 3: Checking ticker.fast_info...")
        try:
            if hasattr(ticker, 'fast_info'):
                fast_info = ticker.fast_info
                if fast_info:
                    fast_info_data = {}
                    # Try to get attributes from fast_info
                    for attr in ['currency', 'exchange', 'last_price', 'market_cap']:
                        if hasattr(fast_info, attr):
                            value = getattr(fast_info, attr)
                            if value is not None:
                                fast_info_data[attr] = value
                    
                    if fast_info_data:
                        print_success(f"Fast info available with {len(fast_info_data)} fields:")
                        for field, value in fast_info_data.items():
                            print(f"  • {field}: {value}")
                        result['method_results']['fast_info'] = True
                        result['valid'] = True
                    else:
                        print_warning("Fast info has no data")
                        result['method_results']['fast_info'] = False
                else:
                    print_warning("Fast info is None")
                    result['method_results']['fast_info'] = False
            else:
                print_warning("No fast_info attribute")
                result['method_results']['fast_info'] = False
                
        except Exception as e:
            print_error(f"Error getting fast_info: {e}")
            result['errors'].append(f"Fast info error: {e}")
            result['method_results']['fast_info'] = False
        
        # Method 4: Check if we can get current price
        print_info("Method 4: Checking current price...")
        try:
            info = ticker.info
            price_fields = ['currentPrice', 'regularMarketPrice', 'price', 'ask', 'bid', 'previousClose']
            found_price = None
            
            for field in price_fields:
                if field in info and info[field] is not None:
                    found_price = field
                    print_success(f"Found price in '{field}': {info[field]}")
                    result['method_results']['price'] = True
                    result['valid'] = True
                    break
            
            if not found_price:
                print_warning("No price information found")
                result['method_results']['price'] = False
                
        except Exception as e:
            print_error(f"Error checking price: {e}")
            result['errors'].append(f"Price error: {e}")
            result['method_results']['price'] = False
        
        # Summary for this symbol
        if result['valid']:
            print(f"\n{Colors.GREEN}{Colors.BOLD}✓ {symbol} is VALID{Colors.END}")
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}✗ {symbol} is INVALID{Colors.END}")
            
    except Exception as e:
        print_error(f"Fatal error testing {symbol}: {e}")
        result['errors'].append(f"Fatal error: {e}")
        result['valid'] = False
    
    return result

def test_validation_methods():
    """Test different validation methods to find the most reliable"""
    print_header("Testing Validation Methods")
    
    # Test a known good symbol
    good_symbol = "AAPL"
    print(f"{Colors.BOLD}Testing with known good symbol: {good_symbol}{Colors.END}\n")
    
    ticker = yf.Ticker(good_symbol)
    
    # Method comparison
    methods = {}
    
    # Method A: Check if symbol exists in info
    try:
        info = ticker.info
        methods['info_symbol'] = info.get('symbol') is not None
        print_success(f"Method A (info.symbol): {methods['info_symbol']}")
    except:
        methods['info_symbol'] = False
        print_error(f"Method A (info.symbol): {methods['info_symbol']}")
    
    # Method B: Check if any name field exists
    try:
        info = ticker.info
        methods['any_name'] = any([
            info.get('shortName'),
            info.get('longName'),
            info.get('symbol')
        ])
        print_success(f"Method B (any name): {methods['any_name']}")
    except:
        methods['any_name'] = False
        print_error(f"Method B (any name): {methods['any_name']}")
    
    # Method C: Check if we can get history
    try:
        history = ticker.history(period="1d")
        methods['has_history'] = not history.empty
        print_success(f"Method C (has history): {methods['has_history']}")
    except:
        methods['has_history'] = False
        print_error(f"Method C (has history): {methods['has_history']}")
    
    # Method D: Check if info dict has substantial data
    try:
        info = ticker.info
        methods['info_substantial'] = len(info) > 5
        print_success(f"Method D (info > 5 fields): {methods['info_substantial']} ({len(info)} fields)")
    except:
        methods['info_substantial'] = False
        print_error(f"Method D (info > 5 fields): {methods['info_substantial']}")
    
    # Method E: Check for price data
    try:
        info = ticker.info
        price_fields = ['currentPrice', 'regularMarketPrice', 'previousClose', 'ask', 'bid']
        methods['has_price'] = any(info.get(field) for field in price_fields)
        print_success(f"Method E (has price): {methods['has_price']}")
    except:
        methods['has_price'] = False
        print_error(f"Method E (has price): {methods['has_price']}")
    
    print(f"\n{Colors.BOLD}Recommended validation logic:{Colors.END}")
    print("Use a combination of methods for robustness:")
    print("1. First check if info dict has substantial data (> 5 fields)")
    print("2. Then verify at least one of: symbol, shortName, or longName exists")
    print("3. For extra confidence, check if history is available")

def improved_validate_symbol(symbol: str) -> tuple[bool, str, dict]:
    """
    Improved validation function for the ticker service
    Returns: (is_valid, company_name, additional_info)
    """
    try:
        ticker = yf.Ticker(symbol.upper())
        info = ticker.info
        
        # Check if we got substantial data back
        if len(info) <= 1:
            return False, "", {"error": "No data returned"}
        
        # Check for error messages in info
        if 'trailingPegRatio' in info and info.get('trailingPegRatio') is None and len(info) <= 5:
            return False, "", {"error": "Likely invalid symbol"}
        
        # Look for key identifying fields
        symbol_found = info.get('symbol')
        short_name = info.get('shortName')
        long_name = info.get('longName')
        
        # Determine if valid
        if symbol_found or short_name or long_name:
            # Get the best name available
            company_name = long_name or short_name or symbol_found or symbol.upper()
            
            # Collect useful validation info
            validation_info = {
                'currency': info.get('currency'),
                'exchange': info.get('exchange'),
                'quoteType': info.get('quoteType'),
                'market': info.get('market'),
                'fields_count': len(info)
            }
            
            return True, company_name, validation_info
        
        # If no clear identification but has lots of data, might still be valid
        if len(info) > 10:
            # Try to get history as additional validation
            try:
                history = ticker.history(period="1d")
                if not history.empty:
                    return True, symbol.upper(), {"fields_count": len(info), "has_history": True}
            except:
                pass
        
        return False, "", {"error": "Unable to validate symbol"}
        
    except Exception as e:
        return False, "", {"error": str(e)}

def test_improved_validation():
    """Test the improved validation function"""
    print_header("Testing Improved Validation Function")
    
    test_cases = [
        ("AAPL", True),
        ("MSFT", True),
        ("INVALID999", False),
        ("SPY", True),
        ("BRK-B", True),
        ("", False),
    ]
    
    passed = 0
    failed = 0
    
    for symbol, expected_valid in test_cases:
        is_valid, name, info = improved_validate_symbol(symbol)
        
        if is_valid == expected_valid:
            print_success(f"{symbol:12} | Expected: {expected_valid:5} | Got: {is_valid:5} | Name: {name}")
            passed += 1
        else:
            print_error(f"{symbol:12} | Expected: {expected_valid:5} | Got: {is_valid:5} | Info: {info}")
            failed += 1
    
    print(f"\n{Colors.BOLD}Results: {passed} passed, {failed} failed{Colors.END}")

def test_batch_symbols():
    """Test all symbols in the test list"""
    print_header("Batch Symbol Testing")
    
    results = {
        'valid': [],
        'invalid': [],
        'errors': []
    }
    
    for symbol in TEST_SYMBOLS:
        result = debug_ticker_validation(symbol)
        
        if result['valid']:
            results['valid'].append(symbol)
        elif result['errors']:
            results['errors'].append(symbol)
        else:
            results['invalid'].append(symbol)
        
        # Small delay to avoid rate limiting
        time.sleep(0.5)
    
    # Print summary
    print_header("Test Summary")
    
    print(f"{Colors.GREEN}Valid symbols ({len(results['valid'])}):{Colors.END}")
    for symbol in results['valid']:
        print(f"  ✓ {symbol}")
    
    print(f"\n{Colors.RED}Invalid symbols ({len(results['invalid'])}):{Colors.END}")
    for symbol in results['invalid']:
        print(f"  ✗ {symbol}")
    
    if results['errors']:
        print(f"\n{Colors.YELLOW}Symbols with errors ({len(results['errors'])}):{Colors.END}")
        for symbol in results['errors']:
            print(f"  ⚠ {symbol}")

def generate_validation_fix():
    """Generate an improved validation function for the ticker service"""
    print_header("Generating Fixed Validation Code")
    
    fix_code = '''
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
'''
    
    print(fix_code)
    
    # Save the fix to a file
    with open("validation_fix.py", "w") as f:
        f.write(fix_code)
    
    print_success("\nFixed validation code saved to: validation_fix.py")
    print_info("Copy this code to replace the validate_symbol method in app/ticker_service.py")

def main():
    """Main debugging routine"""
    print(f"{Colors.BOLD}{Colors.CYAN}")
    print("╔═══════════════════════════════════════════╗")
    print("║     Finsite yfinance Debugging Tool      ║")
    print("║         Symbol Validation Tester         ║")
    print("╚═══════════════════════════════════════════╝")
    print(f"{Colors.END}\n")
    
    # Run all tests
    if test_yfinance_version():
        test_validation_methods()
        test_improved_validation()
        test_batch_symbols()
        generate_validation_fix()
    else:
        print_error("Failed to initialize yfinance. Please check installation.")
        sys.exit(1)
    
    print(f"\n{Colors.BOLD}Debugging complete!{Colors.END}")

if __name__ == "__main__":
    main()
