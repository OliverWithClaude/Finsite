# Implementation Briefing: Trading Positions Management

## Project: Finsite - Investment Workbench
**Date:** 2025-09-30  
**Feature:** Buy/Sell Trade Tracking and Position Management

---

## Overview
Extend Finsite to track buy/sell trades and manage open/closed investment positions with profit/loss calculation.

## Requirements

### 1. Data Model

#### Positions Table
```sql
positions:
- id (INTEGER PRIMARY KEY)
- ticker (TEXT)
- status (TEXT: 'OPEN' or 'CLOSED')
- entry_date (TEXT)
- entry_value_eur (REAL) - total amount invested including fees
- entry_price_per_share (REAL) - price per share at entry (EUR or USD)
- entry_currency (TEXT) - 'EUR' or 'USD'
- exit_date (TEXT, NULL if open)
- exit_value_eur (REAL, NULL if open)
- exit_price_per_share (REAL, NULL if open)
- exit_currency (TEXT, NULL if open)
```

#### Trades Table
```sql
trades:
- id (INTEGER PRIMARY KEY)
- position_id (INTEGER, FOREIGN KEY)
- ticker (TEXT)
- trade_type (TEXT: 'BUY' or 'SELL')
- trade_date (TEXT)
- amount_eur (REAL) - total value
- price_per_share (REAL)
- currency (TEXT) - 'EUR' or 'USD'
```

### 2. Business Logic

- **Multiple positions per ticker**: User can have multiple open/closed positions for the same ticker
- **No share quantity tracking**: Only track total amounts and price per share
- **Currency**: Prices per share can be EUR or USD, but all position values stored in EUR
- **No currency conversion**: Ignore FX effects for current value calculation
- **Simple cost basis**: Entry value includes all transaction costs

### 3. Calculations

**Current Value of Open Position:**
```
current_value = (entry_value_eur / entry_price_per_share) * current_market_price
```

**Profit/Loss on Closed Position:**
```
profit_eur = exit_value_eur - entry_value_eur
profit_percentage = (profit_eur / entry_value_eur) * 100
```

**Holding Period:**
```
holding_period_days = exit_date - entry_date (in days)
```

### 4. API Endpoints

#### New Endpoints
- `POST /api/positions/open` - Create buy trade and open position
  - Body: `{ticker, entry_date, entry_value_eur, entry_price_per_share, entry_currency}`
- `POST /api/positions/{id}/close` - Create sell trade and close position
  - Body: `{exit_date, exit_value_eur, exit_price_per_share, exit_currency}`
- `GET /api/positions/open` - List all open positions with current values
- `GET /api/positions/closed` - List all closed positions with P&L
- `GET /api/positions/{id}` - Get single position details

### 5. Frontend Components

#### Navigation
- Add "Open Positions" menu item
- Add "Closed Positions" menu item

#### Watchlist Enhancement
- Add "Buy" button next to each ticker in watchlist
- Buy button opens modal/form with fields:
  - Entry Date (date picker)
  - Entry Value EUR (number)
  - Entry Price per Share (number)
  - Currency (dropdown: EUR/USD)

#### Open Positions View
Display table with columns:
- Ticker (link to ticker detail)
- Entry Date
- Entry Value (EUR)
- Entry Price per Share (with currency)
- Current Price per Share (from yfinance)
- Current Value (EUR, calculated)
- Unrealized P&L (EUR and %)
- Action: "Close Position" button

#### Close Position Form
Pre-filled reference data:
- Ticker (read-only)
- Entry Date (read-only)
- Entry Value (read-only)
- Entry Price per Share (read-only)

Input fields:
- Exit Date (date picker)
- Exit Value EUR (number)
- Exit Price per Share (number)
- Currency (dropdown: EUR/USD)

#### Closed Positions View
Display table with columns:
- Ticker
- Entry Date
- Entry Value (EUR)
- Exit Date
- Exit Value (EUR)
- Profit/Loss (EUR)
- Profit/Loss (%)
- Holding Period (days)

### 6. Technical Stack
- **Backend**: FastAPI, SQLite
- **Frontend**: HTML, JavaScript, CSS (existing style)
- **Market Data**: yfinance for current prices
- **Database**: Extend existing SQLite schema

### 7. Implementation Steps

1. **Database Migration**
   - Create positions table
   - Create trades table
   - Add migration script

2. **Backend Implementation**
   - Create Position and Trade models
   - Implement position service layer
   - Add API endpoints
   - Integrate yfinance for current prices

3. **Frontend Implementation**
   - Add navigation items
   - Create Buy button in watchlist
   - Build Open Positions page
   - Build Closed Positions page
   - Create trade forms (buy/sell)
   - Add CSS for new components

4. **Testing**
   - Test position lifecycle (open → close)
   - Test multiple positions per ticker
   - Verify calculations (current value, P&L, holding period)
   - Test edge cases (same-day trades, etc.)

### 8. Non-Requirements (Out of Scope)
- ❌ Share quantity tracking
- ❌ Separate transaction cost tracking
- ❌ Currency conversion/FX rates
- ❌ Partial position closing
- ❌ Dividend tracking
- ❌ Tax calculations

---

## Success Criteria
✅ User can open position from watchlist  
✅ User can view all open positions with live current values  
✅ User can close open positions  
✅ User can view closed positions with P&L and holding period  
✅ Multiple positions per ticker supported  
✅ Consistent with existing Finsite UI/UX style
