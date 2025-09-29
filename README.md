# Finsite - Investment Intelligence with Grit

A pragmatic financial information web application built with FastAPI and yfinance, designed to support daily investing decisions with a weathered, resilient aesthetic.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-green)
![yfinance](https://img.shields.io/badge/yfinance-latest-orange)
![License](https://img.shields.io/badge/license-MIT-brightgreen)

## 🎯 Features

- **Ticker Management**: Add, remove, and manage a watchlist of stock ticker symbols
- **Real-time Data**: Fetch current stock information using yfinance API
- **Company Information**: Display comprehensive financial metrics and company details
- **Robust Validation**: Ultra-robust ticker symbol validation with multi-point verification
- **Optimistic Grit Design**: Unique visual style with weathered, pragmatic aesthetics

## 🎨 Design Philosophy

**Optimistic Grit** - A visual style that embodies pragmatic resilience:
- Deep Navy (`#1C3D5A`) - Primary backgrounds
- Muted Crimson (`#8B3A3A`) - Alerts and important actions  
- Warm Ochre (`#D08C34`) - Highlights and CTAs
- Soft Gray (`#A9A9A9`) - Secondary text
- Off-White (`#F2E8DC`) - Card backgrounds
- Accent Teal (`#2E8B8B`) - Interactive elements

Typography: Source Sans Pro (headers) + Merriweather (body) for confident, weathered readability.

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Windows OS (scripts provided for Windows, easily adaptable for Linux/Mac)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/Finsite.git
   cd Finsite
   ```

2. **Run the setup script**
   ```cmd
   setup.bat
   ```
   This will:
   - Create a virtual environment
   - Install all dependencies
   - Set up the database

3. **Start the server**
   ```cmd
   start_server.bat
   ```

4. **Open your browser**
   Navigate to `http://localhost:8000`

## 📁 Project Structure

```
Finsite/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── models.py               # Pydantic models
│   ├── database.py             # SQLite database setup
│   └── ticker_service.py       # yfinance integration
├── static/
│   ├── css/
│   │   └── style.css          # Optimistic Grit styling
│   └── js/
│       └── main.js            # Frontend JavaScript
├── templates/
│   └── index.html             # Main application page
├── data/
│   └── finsite.db             # SQLite database (auto-created)
├── requirements.txt           # Python dependencies
├── setup.bat                  # Setup script (Windows)
├── start_server.bat          # Server startup script (Windows)
├── debug_yfinance.py         # Debugging tool for ticker validation
└── README.md                 # This file
```

## 🛠️ API Endpoints

### Main Application
- `GET /` - Main web interface

### Ticker Management
- `GET /api/tickers` - List all watchlist tickers
- `POST /api/tickers` - Add new ticker to watchlist
- `DELETE /api/tickers/{symbol}` - Remove ticker from watchlist

### Information Retrieval
- `GET /api/ticker-info/{symbol}` - Get detailed ticker information
- `POST /api/validate-ticker` - Validate ticker symbol and get company name

### Debugging (Development)
- `GET /api/debug-ticker/{symbol}` - Debug ticker validation
- `GET /api/test-symbols` - Test common symbols
- `GET /health` - Health check with yfinance connectivity test

## 🔍 Features in Detail

### Ticker Validation
The application uses an ultra-robust validation system with:
- 6-point validation scoring
- Blacklist filtering for problematic symbols
- Exchange verification
- Price data validation
- Market cap verification
- Trading history checks

### Financial Metrics Displayed
- Current price and daily change
- Market capitalization
- P/E ratio
- 52-week high/low
- Volume (current and average)
- Sector and industry
- Dividend yield
- Beta coefficient
- Next earnings date
- Company description

## 🐛 Debugging Tools

### Symbol Validation Debugger
```cmd
run_debug.bat
```
Comprehensive testing tool that:
- Tests multiple validation methods
- Compares results across different symbols
- Generates detailed validation reports
- Provides colored terminal output

### Symbol Investigation Tool
```cmd
run_investigation.bat
```
Deep investigation of specific symbols to understand validation edge cases.

## 🔧 Configuration

### Environment Variables
Currently, all configuration is handled through the application. Future versions may support:
- `DATABASE_URL` - Custom database location
- `PORT` - Server port (default: 8000)
- `HOST` - Server host (default: 127.0.0.1)

## 📦 Dependencies

Main dependencies:
- **FastAPI** (0.115.0) - Web framework
- **uvicorn** (0.32.0) - ASGI server
- **yfinance** (latest) - Yahoo Finance API
- **SQLAlchemy** (2.0.35) - Database ORM
- **Jinja2** (3.1.4) - Template engine

See `requirements.txt` for complete list.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Financial data from [yfinance](https://github.com/ranaroussi/yfinance)
- Design philosophy inspired by pragmatic resilience
- Created for investors who appreciate weathered, functional tools

## 📧 Contact

Your Name - [@yourusername](https://twitter.com/yourusername)

Project Link: [https://github.com/yourusername/Finsite](https://github.com/yourusername/Finsite)

---

*Built with pragmatic resilience - Investment Intelligence with Grit*
