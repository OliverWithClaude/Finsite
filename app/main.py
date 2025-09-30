"""Main FastAPI application for Finsite - with improved validation."""

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List
import logging
import os

from app.database import get_db, Ticker, Position, Trade
from app.models import (
    TickerCreate, TickerResponse, TickerInfo,
    PositionCreate, PositionClose, PositionResponse,
    OpenPositionDetail, ClosedPositionDetail
)
from app.ticker_service import TickerService
from app.position_service import PositionService
from app.version import __version__, __codename__

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Finsite",
    description="Investment Intelligence with Grit - Personal Investment Workbench",
    version=__version__
)

# Setup templates and static files
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")

# Initialize services
ticker_service = TickerService()
position_service = PositionService()


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Serve the main application page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/tickers", response_model=List[TickerResponse])
async def get_tickers(db: Session = Depends(get_db)):
    """Get all tracked ticker symbols."""
    try:
        tickers = db.query(Ticker).order_by(Ticker.symbol).all()
        return tickers
    except Exception as e:
        logger.error(f"Error fetching tickers: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch tickers")


@app.post("/api/tickers", response_model=TickerResponse)
async def create_ticker(ticker_data: TickerCreate, db: Session = Depends(get_db)):
    """Add a new ticker to track."""
    symbol = ticker_data.symbol.upper().strip()
    
    # Check if ticker already exists
    existing = db.query(Ticker).filter(
        Ticker.symbol == symbol
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Ticker already exists in your watchlist")
    
    # Validate ticker symbol with improved validation
    logger.info(f"Validating ticker symbol: {symbol}")
    
    if not ticker_service.validate_symbol(symbol):
        logger.warning(f"Invalid ticker symbol: {symbol}")
        raise HTTPException(
            status_code=400, 
            detail=f"'{symbol}' is not a valid ticker symbol or cannot fetch data from Yahoo Finance"
        )
    
    # Create new ticker
    new_ticker = Ticker(
        symbol=symbol,
        name=ticker_data.name or symbol  # Use symbol as fallback if no name provided
    )
    
    try:
        db.add(new_ticker)
        db.commit()
        db.refresh(new_ticker)
        logger.info(f"Successfully added ticker: {symbol}")
        return new_ticker
    except Exception as e:
        db.rollback()
        logger.error(f"Database error adding ticker {symbol}: {e}")
        raise HTTPException(status_code=500, detail="Failed to save ticker")


@app.delete("/api/tickers/{symbol}")
async def delete_ticker(symbol: str, db: Session = Depends(get_db)):
    """Remove a ticker from the watchlist."""
    symbol = symbol.upper().strip()
    
    ticker = db.query(Ticker).filter(
        Ticker.symbol == symbol
    ).first()
    
    if not ticker:
        raise HTTPException(status_code=404, detail=f"Ticker '{symbol}' not found in watchlist")
    
    try:
        db.delete(ticker)
        db.commit()
        logger.info(f"Successfully deleted ticker: {symbol}")
        return {"message": f"Ticker {symbol} deleted successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Database error deleting ticker {symbol}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete ticker")


@app.get("/api/ticker-info/{symbol}", response_model=TickerInfo)
async def get_ticker_info(symbol: str):
    """Get detailed information about a ticker."""
    symbol = symbol.upper().strip()
    logger.info(f"Fetching info for ticker: {symbol}")
    
    info = ticker_service.get_ticker_info(symbol)
    
    if info.error:
        logger.warning(f"Error fetching info for {symbol}: {info.error}")
        raise HTTPException(status_code=400, detail=info.error)
    
    return info


@app.post("/api/validate-ticker")
async def validate_ticker(ticker_data: dict):
    """Validate a ticker symbol and get its name - IMPROVED VERSION."""
    symbol = ticker_data.get("symbol", "").strip().upper()
    
    if not symbol:
        raise HTTPException(status_code=400, detail="Symbol is required")
    
    logger.info(f"Validating ticker: {symbol}")
    
    # First, check if it's a valid symbol
    if not ticker_service.validate_symbol(symbol):
        logger.warning(f"Invalid symbol: {symbol}")
        raise HTTPException(
            status_code=400, 
            detail=f"'{symbol}' is not a valid ticker symbol. Please check the symbol and try again."
        )
    
    # Get company name
    company_name = ticker_service.get_company_name(symbol)
    
    if not company_name:
        # If we can't get a name but symbol is valid, use symbol itself
        company_name = symbol
    
    logger.info(f"Validation successful for {symbol}: {company_name}")
    
    return {
        "symbol": symbol,
        "name": company_name,
        "valid": True
    }


@app.get("/api/debug-ticker/{symbol}")
async def debug_ticker(symbol: str):
    """Debug endpoint to test ticker validation - useful for troubleshooting."""
    symbol = symbol.upper().strip()
    
    result = ticker_service.test_symbol(symbol)
    
    # Also try to get full info to see what's available
    info = ticker_service.get_ticker_info(symbol)
    
    return {
        "debug_info": result,
        "ticker_info": {
            "has_error": info.error is not None,
            "error": info.error,
            "has_price": info.current_price is not None,
            "has_name": info.name != symbol,
            "field_count": sum(1 for field in [
                info.current_price, info.market_cap, info.pe_ratio,
                info.sector, info.industry, info.description
            ] if field is not None)
        }
    }


# Position Management Endpoints

@app.post("/api/positions/open")
async def open_position(position_data: PositionCreate, db: Session = Depends(get_db)):
    """Create a new open position with buy trade."""
    try:
        position = position_service.create_position(
            db=db,
            ticker=position_data.ticker,
            entry_date=position_data.entry_date,
            entry_value_eur=position_data.entry_value_eur,
            entry_price_per_share=position_data.entry_price_per_share,
            entry_currency=position_data.entry_currency
        )
        return position.to_dict()
    except ValueError as e:
        logger.error(f"Validation error opening position: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error opening position: {e}")
        raise HTTPException(status_code=500, detail="Failed to open position")


@app.post("/api/positions/{position_id}/close")
async def close_position(position_id: int, close_data: PositionClose, db: Session = Depends(get_db)):
    """Close an existing position with sell trade."""
    try:
        position = position_service.close_position(
            db=db,
            position_id=position_id,
            exit_date=close_data.exit_date,
            exit_value_eur=close_data.exit_value_eur,
            exit_currency=close_data.exit_currency
        )
        return position.to_dict()
    except ValueError as e:
        logger.error(f"Validation error closing position: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error closing position: {e}")
        raise HTTPException(status_code=500, detail="Failed to close position")


@app.get("/api/positions/open", response_model=List[OpenPositionDetail])
async def get_open_positions(db: Session = Depends(get_db)):
    """Get all open positions with current valuations."""
    try:
        positions = position_service.get_open_positions(db)
        return positions
    except Exception as e:
        logger.error(f"Error fetching open positions: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch open positions")


@app.get("/api/positions/closed", response_model=List[ClosedPositionDetail])
async def get_closed_positions(db: Session = Depends(get_db)):
    """Get all closed positions with P&L."""
    try:
        positions = position_service.get_closed_positions(db)
        return positions
    except Exception as e:
        logger.error(f"Error fetching closed positions: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch closed positions")


@app.get("/api/positions/{position_id}")
async def get_position(position_id: int, db: Session = Depends(get_db)):
    """Get a single position by ID."""
    position = position_service.get_position(db, position_id)
    
    if not position:
        raise HTTPException(status_code=404, detail=f"Position {position_id} not found")
    
    return position.to_dict()


@app.delete("/api/positions/{position_id}")
async def delete_position(position_id: int, db: Session = Depends(get_db)):
    """Delete a closed position."""
    position = position_service.get_position(db, position_id)
    
    if not position:
        raise HTTPException(status_code=404, detail=f"Position {position_id} not found")
    
    if position.status != 'CLOSED':
        raise HTTPException(status_code=400, detail="Can only delete closed positions")
    
    try:
        db.delete(position)
        db.commit()
        logger.info(f"Deleted closed position {position_id} for {position.ticker}")
        return {"message": f"Position {position_id} deleted successfully"}
    except Exception as e:
        db.rollback()
        logger.error(f"Error deleting position {position_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete position")


@app.get("/api/positions/{position_id}/chart-data")
async def get_position_chart_data(
    position_id: int, 
    db: Session = Depends(get_db)
):
    """Get chart data for a closed position.
    
    Returns price history with entry/exit markers.
    """
    try:
        chart_data = position_service.get_chart_data(db, position_id)
        return chart_data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error fetching chart data: {e}")
        return {
            "error": "Unable to load chart data. Please try again later."
        }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    # Test yfinance connectivity
    test_result = ticker_service.validate_symbol("AAPL")
    
    return {
        "status": "healthy",
        "service": "Finsite",
        "version": __version__,
        "codename": __codename__,
        "yfinance_connection": "ok" if test_result else "error"
    }


@app.get("/api/test-symbols")
async def test_common_symbols():
    """Test endpoint to validate common symbols - useful for debugging."""
    test_symbols = ["AAPL", "MSFT", "GOOGL", "INVALID123", "SPY", "BRK-B"]
    results = {}
    
    for symbol in test_symbols:
        results[symbol] = {
            "is_valid": ticker_service.validate_symbol(symbol),
            "name": ticker_service.get_company_name(symbol)
        }
    
    return results


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Finsite application...")
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
