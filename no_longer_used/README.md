# Finsite - Investment Intelligence with Grit

**Version 1.0** | Personal Investment Workbench

A pragmatic financial tracking application built with FastAPI and yfinance, designed to support personal investing decisions with minimal friction and maximum insight.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-green)
![Version](https://img.shields.io/badge/version-1.0.0-brightgreen)
![License](https://img.shields.io/badge/license-MIT-brightgreen)

## 🎯 What is Finsite?

Finsite is a personal investment workbench that helps you:
- **Track Watchlists**: Monitor stocks you're interested in
- **Manage Open Positions**: Track active investments with live valuations
- **Analyze Closed Positions**: Review historical performance with detailed P&L metrics
- **Make Informed Decisions**: Access real-time market data and company information

**Philosophy**: Built with pragmatic resilience - tools that are functional, fast, and focused on what matters.

## ✨ Key Features

### 📊 Watchlist Management
- Add stock ticker symbols with automatic validation
- View detailed company information (price, market cap, P/E ratio, sector, etc.)
- Real-time price updates from Yahoo Finance
- One-click removal from watchlist

### 💰 Position Tracking
- **Open Positions**: 
  - Track active investments with entry date, value, and price per share
  - Live current price and valuation updates
  - Calculated unrealized P&L (EUR and %)
  - Quick close functionality
  
- **Close Positions**: 
  - Simple exit workflow (date, exit value, currency)
  - Automatic exit price calculation
  - Instant P&L computation

- **Closed Positions**:
  - Historical performance review
  - Realized profit/loss tracking (EUR and %)
  - Holding period in days
  - Delete completed positions

### 🎨 Clean Design
- **Optimistic Grit** aesthetic: Professional yet approachable
- Responsive layout works on desktop and mobile
- Intuitive navigation between views
- Color-coded profit/loss indicators

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Windows OS (or adapt batch scripts for Linux/Mac)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/finsite.git
   cd finsite
   ```

2. **Run setup**
   ```bash
   setup.bat
   ```
   Creates virtual environment and installs dependencies.

3. **Start the server**
   ```bash
   start_server.bat
   ```

4. **Open browser**
   Navigate to http://127.0.0.1:8000

### First Use

1. **Add Tickers**: Click "+ Add Ticker", enter symbol (e.g., AAPL), validate, and save
2. **Open Position**: Click "Buy" next to any ticker, fill in entry details
3. **View Positions**: Navigate to "Open Positions" to see live valuations
4. **Close Position**: Click "Close" on any open position, enter exit details
5. **Review History**: Check "Closed Positions" for P&L analysis

## 📁 Project Structure

```
Finsite/
├── app/
│   ├── main.py                 # FastAPI application & API endpoints
│   ├── models.py               # Pydantic models for validation
│   ├── database.py             # SQLAlchemy models & database setup
│   ├── ticker_service.py       # Yahoo Finance integration
│   └── position_service.py     # Position management logic
├── static/
│   ├── css/
│   │   └── style.css          # Application styling
│   └── js/
│       └── main.js            # Frontend JavaScript
├── templates/
│   └── index.html             # Main application page
├── data/
│   └── finsite.db             # SQLite database (auto-created)
├── requirements.txt           # Python dependencies
├── RELEASE_NOTES_v1.0.md      # Release notes
└── README.md                  # This file
```

## 🔌 API Endpoints

### Tickers
- `GET /api/tickers` - List all watchlist tickers
- `POST /api/tickers` - Add ticker to watchlist
- `DELETE /api/tickers/{symbol}` - Remove ticker from watchlist
- `GET /api/ticker-info/{symbol}` - Get detailed ticker information
- `POST /api/validate-ticker` - Validate ticker symbol

### Positions
- `POST /api/positions/open` - Open new position
- `POST /api/positions/{id}/close` - Close position
- `GET /api/positions/open` - List open positions with live valuations
- `GET /api/positions/closed` - List closed positions with P&L
- `GET /api/positions/{id}` - Get single position details
- `DELETE /api/positions/{id}` - Delete closed position

### System
- `GET /health` - Health check endpoint
- `GET /api/test-symbols` - Test ticker validation

## 💾 Data Storage

### Database
- **Type**: SQLite (local file-based)
- **Location**: `data/finsite.db`
- **Tables**: tickers, positions, trades
- **Auto-created**: On first run

### Privacy
- All data stored locally on your machine
- No cloud sync or external data sharing
- No user accounts or authentication needed
- Complete control over your trading history

## 🎨 Design Philosophy

**Optimistic Grit** - A visual style that embodies pragmatic resilience:

**Colors:**
- Deep Navy (#1C3D5A) - Primary backgrounds
- Muted Crimson (#8B3A3A) - Alerts and warnings
- Warm Ochre (#D08C34) - Highlights and CTAs
- Soft Gray (#A9A9A9) - Secondary text
- Off-White (#F2E8DC) - Card backgrounds
- Accent Teal (#2E8B8B) - Positive indicators

**Typography:**
- Source Sans 3 - Headers (confident, clean)
- Merriweather - Body text (readable, weathered)

## 📊 Financial Metrics

### Displayed for Each Ticker
- Current price and daily change
- Market capitalization
- P/E ratio
- 52-week high/low
- Volume (current and average)
- Dividend yield
- Beta coefficient
- Sector and industry
- Company description
- Next earnings date

### Calculated for Positions
- Current valuation (live)
- Unrealized P/L (EUR and %)
- Realized P/L (EUR and %)
- Holding period (days)
- Entry/exit metrics

## 🔧 Configuration

### Default Settings
- **Host**: 127.0.0.1 (localhost)
- **Port**: 8000
- **Database**: SQLite at `data/finsite.db`
- **Auto-reload**: Enabled in development

### Customization
Edit `app/main.py` for server settings or `static/css/style.css` for styling.

## 📦 Dependencies

**Core:**
- FastAPI - Modern Python web framework
- yfinance - Yahoo Finance market data
- SQLAlchemy - Database ORM
- Uvicorn - ASGI web server

**Full list**: See `requirements.txt`

## 🐛 Troubleshooting

### Common Issues

**Server won't start:**
- Ensure Python 3.8+ installed: `python --version`
- Check port 8000 is available
- Verify virtual environment: `venv\Scripts\activate`

**Ticker validation fails:**
- Check internet connection
- Verify ticker symbol exists on Yahoo Finance
- Try the `/api/debug-ticker/{symbol}` endpoint

**Positions not displaying:**
- Check browser console (F12) for errors
- Verify database created: `data/finsite.db` should exist
- Check server logs for errors

**Database errors:**
- Delete `data/finsite.db` to reset (WARNING: loses all data)
- Check file permissions on data folder

### Debug Mode
See `DEBUGGING_BUY_BUTTON.md` for detailed troubleshooting steps.

## 📝 Development

### Running Tests
```bash
# Test ticker validation
python debug_yfinance.py

# Test API endpoints
curl http://127.0.0.1:8000/health
```

### Adding Features
1. Backend: Add endpoints in `app/main.py`
2. Services: Add logic in `app/*_service.py`
3. Frontend: Update `static/js/main.js` and `templates/index.html`
4. Styles: Modify `static/css/style.css`

## 🚧 Known Limitations

- No currency conversion (FX effects ignored by design)
- Current prices may be delayed 15 minutes (Yahoo Finance limitation)
- No support for options, futures, or derivatives
- No handling of stock splits or dividends
- Single-user application (no multi-user support)
- No real-time alerts or notifications

## 🎯 Design Decisions

### Why These Choices?

**Total Values, Not Share Quantities**
- Simpler data entry
- Less chance of errors
- Easier mental math
- Price per share tracked for consistency

**No Currency Conversion**
- Short holding periods minimize FX impact
- Keeps calculations simple
- User can handle conversions if needed

**Local SQLite Database**
- No server required
- Fast and reliable
- Complete data ownership
- Easy backup (just copy the .db file)

**Minimal Dependencies**
- Faster installation
- Fewer breaking changes
- Easier maintenance

## 🔮 Future Enhancements

**Not in 1.0, but possible:**
- CSV export functionality
- Charts and visualizations  
- Portfolio dashboard
- Price alerts
- Partial position closing
- Position editing
- Tax reporting
- Mobile app

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

This is a personal project, but you're welcome to fork and modify it!

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📚 Documentation

- `RELEASE_NOTES_v1.0.md` - Version 1.0 release notes
- `IMPLEMENTATION_BRIEFING_POSITIONS.md` - Technical implementation details
- `TESTING_CHECKLIST.md` - Testing procedures
- `DEBUGGING_BUY_BUTTON.md` - Troubleshooting guide

## 🙏 Acknowledgments

- **FastAPI** - Modern Python web framework
- **yfinance** - Yahoo Finance API wrapper
- **SQLAlchemy** - Database ORM
- Built for investors who value pragmatic, functional tools

## 📞 Support

For issues or questions:
- Check documentation in repository
- Review troubleshooting guides
- Open an issue on GitHub

---

**Finsite v1.0** - Built with pragmatic resilience  
*Investment Intelligence with Grit* 📈
