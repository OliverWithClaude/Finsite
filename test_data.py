"""
Quick test data generator for Finsite positions.
Run this to populate some test positions for development/testing.

Usage: python test_data.py
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000/api"

def create_test_position(ticker, days_ago, entry_value, entry_price, currency="USD"):
    """Create a test position."""
    entry_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
    
    position_data = {
        "ticker": ticker,
        "entry_date": entry_date,
        "entry_value_eur": entry_value,
        "entry_price_per_share": entry_price,
        "entry_currency": currency
    }
    
    try:
        response = requests.post(f"{BASE_URL}/positions/open", json=position_data)
        if response.status_code == 200:
            print(f"✓ Created open position for {ticker}")
            return response.json()
        else:
            print(f"✗ Failed to create position for {ticker}: {response.text}")
            return None
    except Exception as e:
        print(f"✗ Error creating position for {ticker}: {e}")
        return None

def close_test_position(position_id, ticker, days_ago, exit_value, exit_price, currency="USD"):
    """Close a test position."""
    exit_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
    
    close_data = {
        "exit_date": exit_date,
        "exit_value_eur": exit_value,
        "exit_price_per_share": exit_price,
        "exit_currency": currency
    }
    
    try:
        response = requests.post(f"{BASE_URL}/positions/{position_id}/close", json=close_data)
        if response.status_code == 200:
            print(f"✓ Closed position for {ticker}")
            return response.json()
        else:
            print(f"✗ Failed to close position for {ticker}: {response.text}")
            return None
    except Exception as e:
        print(f"✗ Error closing position for {ticker}: {e}")
        return None

def add_ticker_if_missing(symbol, name):
    """Add ticker to watchlist if not present."""
    try:
        # Check if exists
        response = requests.get(f"{BASE_URL}/tickers")
        if response.status_code == 200:
            tickers = response.json()
            if any(t['symbol'] == symbol for t in tickers):
                print(f"  {symbol} already in watchlist")
                return True
        
        # Add ticker
        ticker_data = {"symbol": symbol, "name": name}
        response = requests.post(f"{BASE_URL}/tickers", json=ticker_data)
        if response.status_code == 200:
            print(f"✓ Added {symbol} to watchlist")
            return True
        else:
            print(f"✗ Failed to add {symbol}: {response.text}")
            return False
    except Exception as e:
        print(f"✗ Error adding {symbol}: {e}")
        return False

def main():
    print("=" * 60)
    print("Finsite Test Data Generator")
    print("=" * 60)
    print()
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/../health")
        if response.status_code != 200:
            print("✗ Server not responding. Make sure it's running!")
            print("  Run: start_server.bat")
            return
        print("✓ Server is running")
        print()
    except Exception as e:
        print("✗ Cannot connect to server. Make sure it's running!")
        print(f"  Error: {e}")
        print("  Run: start_server.bat")
        return
    
    # Test data scenarios
    test_scenarios = [
        # (ticker, name, days_held_start, entry_value, entry_price, currency)
        ("AAPL", "Apple Inc.", 30, 3001, 150.50, "USD"),
        ("MSFT", "Microsoft Corporation", 45, 5000, 250.00, "USD"),
        ("GOOGL", "Alphabet Inc.", 15, 2500, 125.00, "USD"),
    ]
    
    print("Adding tickers to watchlist...")
    for ticker, name, _, _, _, _ in test_scenarios:
        add_ticker_if_missing(ticker, name)
    
    print()
    print("Creating open positions...")
    
    # Create open positions
    open_positions = []
    for ticker, name, days_ago, entry_value, entry_price, currency in test_scenarios:
        position = create_test_position(ticker, days_ago, entry_value, entry_price, currency)
        if position:
            open_positions.append((position['id'], ticker, days_ago, entry_value, entry_price, currency))
    
    print()
    print("Creating some closed positions (winners and losers)...")
    
    # Close some positions with profit/loss
    if len(open_positions) >= 2:
        # Close first position with profit
        pos_id, ticker, days_ago, entry_value, entry_price, currency = open_positions[0]
        exit_value = entry_value * 1.05  # 5% profit
        exit_price = entry_price * 1.05
        close_test_position(pos_id, ticker, days_ago // 2, exit_value, exit_price, currency)
        
        # Close second position with loss
        pos_id, ticker, days_ago, entry_value, entry_price, currency = open_positions[1]
        exit_value = entry_value * 0.97  # 3% loss
        exit_price = entry_price * 0.97
        close_test_position(pos_id, ticker, days_ago // 3, exit_value, exit_price, currency)
    
    print()
    print("=" * 60)
    print("Test data generation complete!")
    print("=" * 60)
    print()
    print("You should now have:")
    print("  - 1 open position (GOOGL)")
    print("  - 2 closed positions (AAPL with profit, MSFT with loss)")
    print()
    print("Go to http://127.0.0.1:8000 to view them!")

if __name__ == "__main__":
    main()
