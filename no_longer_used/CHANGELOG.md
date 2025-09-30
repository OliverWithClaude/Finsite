# Changelog

All notable changes to Finsite will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-09-30

### Added
- **Watchlist Management**: Add, remove, and track stock ticker symbols
- **Ticker Validation**: Robust validation via Yahoo Finance API
- **Company Information Display**: Comprehensive financial metrics and company details
- **Position Tracking System**: Complete buy/sell trade tracking
- **Open Positions View**: Track active investments with live valuations
  - Entry date, value, and price per share
  - Live current price from Yahoo Finance
  - Calculated current value
  - Unrealized P/L in EUR and percentage
- **Close Position Workflow**: Simple exit process
  - Entry date, exit value, and currency input
  - Automatic exit price calculation
  - Instant P/L computation
- **Closed Positions View**: Historical performance tracking
  - Entry and exit dates and values
  - Realized profit/loss (EUR and %)
  - Holding period in days
- **Delete Functionality**: Remove closed positions from history
- **SQLite Database**: Local data storage
  - Tables: tickers, positions, trades
  - Automatic schema creation
- **RESTful API**: Complete API for all operations
  - Ticker management endpoints
  - Position management endpoints
  - Health check and debugging endpoints
- **Responsive UI**: Clean, modern interface
  - Navigation between Watchlist, Open Positions, Closed Positions
  - Modal dialogs for data entry
  - Color-coded profit/loss indicators
  - Optimistic Grit design aesthetic
- **Documentation**: Comprehensive guides
  - README with quick start
  - Release notes
  - GitHub release guide
  - Testing checklist
  - Debugging guides

### Technical Details
- FastAPI backend with Pydantic validation
- SQLAlchemy ORM for database operations
- yfinance for market data integration
- Vanilla JavaScript frontend (no framework)
- Windows batch scripts for setup and startup

### Design Decisions
- Total position values instead of share quantities for simplicity
- No currency conversion (FX effects ignored for short holding periods)
- Local-only data storage (no cloud sync)
- Single-user application focus
- Automatic calculations where possible

### Known Limitations
- No currency conversion
- Current prices may be delayed 15 minutes (Yahoo Finance API)
- No support for options, futures, or other derivatives
- No handling of stock splits or dividends
- Single-user only (no multi-user support)
- Windows-focused batch scripts

---

## [Unreleased]

### Planned Features
- CSV export functionality
- Charts and visualizations
- Portfolio dashboard
- Price alerts
- Partial position closing
- Position editing capability
- Tax reporting features
- Mobile application

---

## Release Types

- **MAJOR** version: Incompatible API changes
- **MINOR** version: New features, backward compatible
- **PATCH** version: Bug fixes, backward compatible

---

[1.0.0]: https://github.com/yourusername/finsite/releases/tag/v1.0.0
