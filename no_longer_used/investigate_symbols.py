"""
Investigation script for unexpected valid symbols like TEST
"""

import yfinance as yf
import json

def investigate_symbol(symbol):
    """Deep dive into what yfinance returns for a symbol"""
    print(f"\n{'='*60}")
    print(f"INVESTIGATING: {symbol}")
    print('='*60)
    
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        print(f"\n1. INFO DICTIONARY SIZE: {len(info)} fields")
        
        if info:
            # Check key fields
            important_fields = {
                'symbol': info.get('symbol'),
                'shortName': info.get('shortName'),
                'longName': info.get('longName'),
                'exchange': info.get('exchange'),
                'quoteType': info.get('quoteType'),
                'market': info.get('market'),
                'currentPrice': info.get('currentPrice'),
                'regularMarketPrice': info.get('regularMarketPrice'),
                'marketCap': info.get('marketCap'),
                'currency': info.get('currency')
            }
            
            print("\n2. KEY FIELDS:")
            for field, value in important_fields.items():
                if value is not None:
                    print(f"   {field}: {value}")
            
            # Check if it's actually tradeable
            print("\n3. TRADING STATUS:")
            print(f"   Has Price: {any([info.get('currentPrice'), info.get('regularMarketPrice')])}")
            print(f"   Has Market Cap: {info.get('marketCap') is not None}")
            print(f"   Quote Type: {info.get('quoteType')}")
            print(f"   Market State: {info.get('marketState')}")
            
            # Try to get history
            print("\n4. HISTORICAL DATA CHECK:")
            try:
                history = ticker.history(period="5d")
                if not history.empty:
                    print(f"   ✓ Has history: {len(history)} days")
                    print(f"   Latest close: {history['Close'].iloc[-1] if not history.empty else 'N/A'}")
                else:
                    print("   ✗ No historical data")
            except Exception as e:
                print(f"   ✗ Error getting history: {e}")
            
            # Check for suspicious patterns
            print("\n5. VALIDATION ASSESSMENT:")
            
            # Is this a real tradeable security?
            is_real = all([
                info.get('exchange') is not None,
                any([info.get('currentPrice'), info.get('regularMarketPrice')]),
                info.get('currency') is not None
            ])
            
            print(f"   Appears to be real security: {is_real}")
            
            # Save full info for review
            filename = f"investigation_{symbol}.json"
            with open(filename, 'w') as f:
                # Convert to serializable format
                serializable_info = {k: str(v) if v is not None else None for k, v in info.items()}
                json.dump(serializable_info, f, indent=2)
            print(f"\n   Full data saved to: {filename}")
            
    except Exception as e:
        print(f"\nERROR investigating {symbol}: {e}")

# Investigate suspicious symbols
suspicious_symbols = ["TEST", "INVALID", "ABC", "XYZ", "FAKE", "DUMMY"]

print("SYMBOL INVESTIGATION REPORT")
print("="*60)

for symbol in suspicious_symbols:
    investigate_symbol(symbol)

print("\n" + "="*60)
print("INVESTIGATION COMPLETE")
print("="*60)

# Also test some definitely valid ones for comparison
print("\n\nCOMPARISON WITH KNOWN VALID SYMBOLS:")
investigate_symbol("AAPL")
