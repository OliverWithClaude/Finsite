# Implementation Briefing: Position Price Charts (v1.1)

**Version:** 1.1.0  
**Date:** 2025-09-30  
**Status:** APPROVED - Ready for Implementation

---

## Overview

Add interactive price charts to the Closed Positions view, allowing users to visualize stock price movement during their holding period with entry/exit markers.

---

## Requirements Summary

### User Story
As a user viewing my closed positions, I want to click on a position and see a price chart showing the stock's performance during my holding period, so I can visually understand the price movements and validate my entry/exit decisions.

---

## Technical Decisions (Approved)

### 1. Charting Library
**Decision:** Plotly  
**Rationale:** Already available in project, highly interactive, perfect for financial time series

### 2. Display Method
**Decision:** Modal Dialog  
**Rationale:** Keeps user in context, consistent with existing UI patterns (buy/sell modals)

### 3. Date Range Calculation
**Logic:**
```python
holding_period_days = exit_date - entry_date
today = current_date
days_since_exit = today - exit_date

if days_since_exit < 90:  # Less than 3 months ago
    # Recent exit - extend to today
    start_date = entry_date - 90 days
    end_date = today
else:
    # Older exit - fixed window
    start_date = entry_date - 90 days
    end_date = exit_date + 90 days
```

**Examples:**
- **Recent position** (exited 45 days ago): Show from 3 months before entry to today
- **Old position** (exited 7 months ago): Show from 3 months before entry to 3 months after exit

### 4. Exit Price Calculation
**Formula:**
```python
shares = entry_value / entry_price_per_share
exit_price_calculated = exit_value / shares
```

**Example:**
- Entry: €3,000 at $150/share → 20 shares
- Exit: €3,100
- Calculated exit price: €3,100 / 20 = $155/share

### 5. Chart Features (Basic)
- ✅ Line chart with daily closing prices
- ✅ Entry/exit markers (large points)
- ✅ Date axis and price axis
- ✅ Title with ticker symbol
- ✅ Hover tooltip (Plotly default)
- ✅ Zoom/pan (Plotly default)
- ❌ No volume bars
- ❌ No export functionality
- ❌ No custom time period toggles

### 6. Chart Styling
**Colors (Optimistic Grit theme):**
- Line color: Deep Navy (#1C3D5A)
- Entry marker: Accent Teal (#2E8B8B) - Large point (●)
- Exit marker: Warm Ochre (#D08C34) - Large point (●)
- Background: Off-White (#F2E8DC)
- Grid lines: Soft Gray (#A9A9A9) with low opacity

**Labels:**
- Entry marker: "Entry" annotation
- Exit marker: "Exit" annotation

### 7. Data Source & Caching
**Approach:**
- Use yfinance for historical price data (daily closing prices)
- **CRITICAL:** Store fetched price history locally in database
- Implement caching strategy to minimize API calls
- Only refetch if data is missing or stale

**Database Strategy:**
- New table: `price_history`
- Columns: ticker, date, close_price, created_at
- Index on (ticker, date) for fast lookups
- Reuse cached data for overlapping date ranges

### 8. Error Handling
- **No price data available:** Show "Data unavailable" message in chart area
- **yfinance API fails:** Show "Unable to load chart data. Please try again later."
- **Ticker delisted:** Show available data with warning message
- **No error retries:** Single attempt, fail gracefully

### 9. Performance
**Strategy:**
- Lazy load: Only fetch data when chart modal is opened
- Loading spinner: Show while fetching/rendering
- Cache in database: Minimize yfinance API calls
- Reuse cached data: Check database before calling yfinance

### 10. Mobile Support
- Chart renders in modal on mobile devices
- No special mobile adjustments needed
- Plotly handles touch interactions by default

---

## Detailed Technical Implementation

### 1. Database Changes

#### New Table: price_history
```sql
CREATE TABLE price_history (
    id INTEGER PRIMARY KEY,
    ticker TEXT NOT NULL,
    date TEXT NOT NULL,  -- Format: YYYY-MM-DD
    close_price REAL NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(ticker, date)
);

CREATE INDEX idx_price_history_ticker_date ON price_history(ticker, date);
```

**Purpose:** Cache historical price data to minimize yfinance API calls

#### SQLAlchemy Model
```python
class PriceHistory(Base):
    __tablename__ = "price_history"
    
    id = Column(Integer, primary_key=True, index=True)
    ticker = Column(String, nullable=False, index=True)
    date = Column(String, nullable=False)
    close_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        UniqueConstraint('ticker', 'date', name='uix_ticker_date'),
        Index('idx_price_history_ticker_date', 'ticker', 'date'),
    )
```

### 2. Backend Implementation

#### New Service: `price_history_service.py`
```python
class PriceHistoryService:
    """Service for managing price history data with caching."""
    
    def get_price_history(
        self, 
        db: Session, 
        ticker: str, 
        start_date: str, 
        end_date: str
    ) -> List[dict]:
        """
        Get price history for ticker in date range.
        Checks cache first, fetches missing data from yfinance.
        
        Returns:
            List[dict]: [{"date": "2025-01-15", "close": 150.50}, ...]
        """
        # 1. Query database for cached data
        # 2. Identify missing date ranges
        # 3. Fetch missing data from yfinance
        # 4. Store new data in database
        # 5. Return complete dataset
        
    def fetch_from_yfinance(
        self, 
        ticker: str, 
        start_date: str, 
        end_date: str
    ) -> List[dict]:
        """Fetch price data from yfinance API."""
        
    def store_prices(
        self, 
        db: Session, 
        ticker: str, 
        prices: List[dict]
    ) -> None:
        """Store price data in database."""
```

#### Updated Service: `position_service.py`
```python
def get_chart_data(
    self, 
    db: Session, 
    position_id: int
) -> dict:
    """
    Get chart data for a closed position.
    
    Returns:
        {
            "ticker": "AAPL",
            "entry_date": "2025-01-15",
            "exit_date": "2025-02-28",
            "entry_price": 150.50,
            "exit_price": 155.00,
            "entry_currency": "USD",
            "start_date": "2024-11-28",
            "end_date": "2025-05-28",
            "prices": [
                {"date": "2024-11-28", "close": 145.20},
                ...
            ],
            "error": None  # or error message if failed
        }
    """
    # 1. Get position from database
    # 2. Validate position is closed
    # 3. Calculate date range
    # 4. Calculate exit price
    # 5. Get price history (using PriceHistoryService)
    # 6. Return formatted data
```

**Date Range Calculation:**
```python
from datetime import datetime, timedelta

entry_date = datetime.strptime(position.entry_date, '%Y-%m-%d')
exit_date = datetime.strptime(position.exit_date, '%Y-%m-%d')
today = datetime.now()

days_since_exit = (today - exit_date).days

if days_since_exit < 90:
    start_date = (entry_date - timedelta(days=90)).strftime('%Y-%m-%d')
    end_date = today.strftime('%Y-%m-%d')
else:
    start_date = (entry_date - timedelta(days=90)).strftime('%Y-%m-%d')
    end_date = (exit_date + timedelta(days=90)).strftime('%Y-%m-%d')
```

**Exit Price Calculation:**
```python
shares = position.entry_value_eur / position.entry_price_per_share
exit_price = position.exit_value_eur / shares
```

#### New API Endpoint: `main.py`
```python
@app.get("/api/positions/{position_id}/chart-data")
async def get_position_chart_data(
    position_id: int, 
    db: Session = Depends(get_db)
):
    """
    Get chart data for a closed position.
    
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
```

### 3. Frontend Implementation

#### HTML: `templates/index.html`
```html
<!-- Chart Modal -->
<div id="chartModal" class="modal hidden">
    <div class="modal-content chart-modal-content">
        <div class="modal-header">
            <h3>Position Chart - <span id="chartModalTicker"></span></h3>
            <button class="modal-close">&times;</button>
        </div>
        <div class="modal-body">
            <div id="chartLoading" class="chart-loading">
                <div class="spinner"></div>
                <p>Loading chart data...</p>
            </div>
            <div id="chartError" class="chart-error hidden">
                <p id="chartErrorMessage"></p>
            </div>
            <div id="chartContainer" class="chart-container hidden"></div>
        </div>
    </div>
</div>
```

#### JavaScript: `static/js/main.js`

**Add to API endpoints:**
```javascript
const API = {
    // ... existing endpoints
    positionChartData: (id) => `/api/positions/${id}/chart-data`
};
```

**Add to DOM elements:**
```javascript
const elements = {
    // ... existing elements
    chartModal: document.getElementById('chartModal'),
    chartModalTicker: document.getElementById('chartModalTicker'),
    chartLoading: document.getElementById('chartLoading'),
    chartError: document.getElementById('chartError'),
    chartErrorMessage: document.getElementById('chartErrorMessage'),
    chartContainer: document.getElementById('chartContainer'),
};
```

**New function: Open chart modal**
```javascript
window.openChartModal = async function(positionId, ticker) {
    // 1. Open modal
    elements.chartModalTicker.textContent = ticker;
    elements.chartModal.classList.remove('hidden');
    
    // 2. Show loading state
    elements.chartLoading.classList.remove('hidden');
    elements.chartError.classList.add('hidden');
    elements.chartContainer.classList.add('hidden');
    
    try {
        // 3. Fetch chart data
        const response = await fetch(API.positionChartData(positionId));
        const data = await response.json();
        
        // 4. Handle errors
        if (data.error) {
            showChartError(data.error);
            return;
        }
        
        // 5. Render chart
        renderChart(data);
        
    } catch (error) {
        showChartError('Failed to load chart data. Please try again.');
    }
}

function showChartError(message) {
    elements.chartLoading.classList.add('hidden');
    elements.chartError.classList.remove('hidden');
    elements.chartErrorMessage.textContent = message;
}

function renderChart(data) {
    elements.chartLoading.classList.add('hidden');
    elements.chartError.classList.add('hidden');
    elements.chartContainer.classList.remove('hidden');
    
    // Prepare data for Plotly
    const dates = data.prices.map(p => p.date);
    const prices = data.prices.map(p => p.close);
    
    // Main price line
    const priceTrace = {
        x: dates,
        y: prices,
        type: 'scatter',
        mode: 'lines',
        name: 'Price',
        line: {
            color: '#1C3D5A',  // Deep Navy
            width: 2
        }
    };
    
    // Entry marker
    const entryTrace = {
        x: [data.entry_date],
        y: [data.entry_price],
        type: 'scatter',
        mode: 'markers+text',
        name: 'Entry',
        marker: {
            color: '#2E8B8B',  // Accent Teal
            size: 12,
            symbol: 'circle'
        },
        text: ['Entry'],
        textposition: 'top center',
        textfont: {
            size: 12,
            color: '#2E8B8B',
            family: 'Source Sans 3, sans-serif',
            weight: 700
        }
    };
    
    // Exit marker
    const exitTrace = {
        x: [data.exit_date],
        y: [data.exit_price],
        type: 'scatter',
        mode: 'markers+text',
        name: 'Exit',
        marker: {
            color: '#D08C34',  // Warm Ochre
            size: 12,
            symbol: 'circle'
        },
        text: ['Exit'],
        textposition: 'top center',
        textfont: {
            size: 12,
            color: '#D08C34',
            family: 'Source Sans 3, sans-serif',
            weight: 700
        }
    };
    
    const layout = {
        title: {
            text: `${data.ticker} - Price History`,
            font: {
                family: 'Source Sans 3, sans-serif',
                size: 18,
                color: '#1C3D5A',
                weight: 700
            }
        },
        xaxis: {
            title: 'Date',
            gridcolor: 'rgba(169, 169, 169, 0.2)',
            tickfont: {
                family: 'Merriweather, serif',
                size: 11
            }
        },
        yaxis: {
            title: `Price (${data.entry_currency})`,
            gridcolor: 'rgba(169, 169, 169, 0.2)',
            tickfont: {
                family: 'Merriweather, serif',
                size: 11
            }
        },
        plot_bgcolor: '#F2E8DC',  // Off-White
        paper_bgcolor: '#F2E8DC',
        hovermode: 'x unified',
        showlegend: true,
        legend: {
            x: 0,
            y: 1.1,
            orientation: 'h',
            font: {
                family: 'Source Sans 3, sans-serif',
                size: 11
            }
        }
    };
    
    const config = {
        responsive: true,
        displayModeBar: true,
        displaylogo: false,
        modeBarButtonsToRemove: ['lasso2d', 'select2d']
    };
    
    Plotly.newPlot(
        'chartContainer', 
        [priceTrace, entryTrace, exitTrace], 
        layout, 
        config
    );
}

function closeChartModal() {
    elements.chartModal.classList.add('hidden');
    elements.chartContainer.innerHTML = '';  // Clear chart
}
```

**Event listeners:**
```javascript
// Add to initializeEventListeners()
document.querySelectorAll('#chartModal .modal-close').forEach(btn => {
    btn.addEventListener('click', closeChartModal);
});

elements.chartModal.addEventListener('click', (e) => {
    if (e.target === elements.chartModal) closeChartModal();
});
```

**Update renderClosedPositions:**
```javascript
// Change table rows to be clickable
<tr onclick="openChartModal(${pos.id}, '${pos.ticker}')" style="cursor: pointer;">
    <!-- or add a specific button -->
    <td>
        <button class="btn btn-secondary" onclick="event.stopPropagation(); openChartModal(${pos.id}, '${pos.ticker}')">
            Chart
        </button>
        <button class="btn btn-danger" onclick="event.stopPropagation(); deleteClosedPosition(${pos.id}, '${pos.ticker}')">
            Delete
        </button>
    </td>
</tr>
```

#### CSS: `static/css/style.css`
```css
/* Chart Modal */
.chart-modal-content {
    max-width: 900px;
    width: 95%;
}

.chart-container {
    min-height: 500px;
    padding: var(--spacing-lg);
}

.chart-loading {
    text-align: center;
    padding: var(--spacing-xxl);
}

.chart-loading .spinner {
    margin: 0 auto var(--spacing-lg) auto;
}

.chart-loading p {
    color: var(--soft-gray);
    font-family: var(--font-display);
    font-size: 1rem;
}

.chart-error {
    text-align: center;
    padding: var(--spacing-xxl);
    background: rgba(139, 58, 58, 0.1);
    border-radius: var(--border-radius);
    margin: var(--spacing-lg);
}

.chart-error p {
    color: var(--muted-crimson);
    font-family: var(--font-display);
    font-weight: 700;
}

/* Make closed position rows clickable */
.positions-table tbody tr {
    cursor: pointer;
    transition: background-color 0.2s ease;
}

.positions-table tbody tr:hover {
    background: var(--off-white);
}

/* Chart button in table */
.btn-chart {
    background: var(--accent-teal);
    color: var(--off-white);
    border: 1px solid var(--accent-teal);
    padding: var(--spacing-xs) var(--spacing-sm);
    font-size: 0.75rem;
    margin-right: var(--spacing-xs);
}

.btn-chart:hover {
    background: #267575;
}

/* Mobile responsive chart */
@media (max-width: 768px) {
    .chart-modal-content {
        width: 100%;
        max-width: 100%;
        height: 100vh;
        max-height: 100vh;
        margin: 0;
        border-radius: 0;
    }
    
    .chart-container {
        min-height: 400px;
    }
}
```

### 4. Pydantic Models

#### New Models: `app/models.py`
```python
class ChartDataPoint(BaseModel):
    """Single price data point."""
    date: str
    close: float

class PositionChartData(BaseModel):
    """Chart data for a position."""
    ticker: str
    entry_date: str
    exit_date: str
    entry_price: float
    exit_price: float
    entry_currency: str
    start_date: str
    end_date: str
    prices: List[ChartDataPoint]
    error: Optional[str] = None
```

---

## Implementation Flow

### Phase 1: Database & Backend (3-4 hours)
1. Create `price_history` table in database.py
2. Create `PriceHistoryService` in price_history_service.py
3. Add `get_chart_data()` method to PositionService
4. Create API endpoint `/api/positions/{id}/chart-data`
5. Test API endpoint with Postman/curl

### Phase 2: Frontend (3-4 hours)
6. Add chart modal HTML structure
7. Implement `openChartModal()` function
8. Implement `renderChart()` with Plotly
9. Add CSS styling for modal and chart
10. Update closed positions table (add clickable rows or chart button)

### Phase 3: Testing & Polish (1-2 hours)
11. Test with various positions (recent, old, different holding periods)
12. Test error scenarios (no data, API failure)
13. Test on mobile devices
14. Performance testing (multiple chart opens)
15. Code review and cleanup

---

## Testing Checklist

### Functional Tests
- [ ] Click on closed position opens chart modal
- [ ] Chart displays with correct date range (recent position extends to today)
- [ ] Chart displays with correct date range (old position shows 3 months buffer)
- [ ] Entry marker appears at correct date and price
- [ ] Exit marker appears at correct date and calculated price
- [ ] Chart loads with spinner first
- [ ] Chart displays "data unavailable" on error
- [ ] Modal closes on X button click
- [ ] Modal closes on outside click
- [ ] Multiple chart opens work without issues

### Data Accuracy Tests
- [ ] Exit price calculation is correct
- [ ] Date range calculation is correct for recent exits
- [ ] Date range calculation is correct for old exits
- [ ] Price data matches Yahoo Finance
- [ ] Entry/exit prices match position data

### Performance Tests
- [ ] First chart load caches data in database
- [ ] Second chart load for same ticker uses cached data
- [ ] No excessive yfinance API calls
- [ ] Chart renders within 3 seconds
- [ ] No memory leaks on multiple opens

### UI/UX Tests
- [ ] Chart styling matches Finsite theme
- [ ] Chart is readable and professional
- [ ] Hover tooltip shows correct information
- [ ] Zoom/pan work properly
- [ ] Mobile rendering works
- [ ] Loading spinner displays correctly
- [ ] Error messages are clear and helpful

### Edge Cases
- [ ] Position with 1-day holding period
- [ ] Position closed today
- [ ] Position closed years ago
- [ ] Ticker with gaps in price data (weekends, holidays)
- [ ] Delisted ticker
- [ ] Invalid ticker
- [ ] Network timeout
- [ ] Empty price data

---

## Success Criteria

✅ User can click on any closed position and view a price chart  
✅ Chart shows 6-month window including 3 months buffer on each side  
✅ Recent positions (< 3 months) extend chart to today  
✅ Entry and exit points clearly marked with large colored dots  
✅ Exit price correctly calculated from position values  
✅ Chart matches Optimistic Grit design aesthetic  
✅ Price data cached locally to minimize API calls  
✅ Loading spinner shows while fetching data  
✅ Graceful error handling with clear messages  
✅ Works on mobile devices  
✅ Performance: Chart loads in < 3 seconds  
✅ No excessive API calls to yfinance  

---

## Non-Functional Requirements

### Performance
- Chart data fetched in < 3 seconds (with cache)
- yfinance calls minimized through database caching
- Page remains responsive during chart load
- No UI blocking

### Reliability
- Graceful degradation if yfinance unavailable
- Clear error messages for all failure cases
- No crashes or unhandled exceptions

### Maintainability
- Clean separation of concerns (service layer)
- Reusable chart rendering function
- Clear code comments
- Follows existing code style

### Scalability
- Database indexed for fast price lookups
- Caching strategy handles thousands of positions
- No N+1 query problems

---

## Dependencies

### Existing (No new installs)
- ✅ Plotly (already in requirements.txt)
- ✅ yfinance (already in use)
- ✅ SQLAlchemy (already in use)

### No New Dependencies Required

---

## Database Migration

### Migration Script: `migrate_v1.1.py`
```python
"""
Migration script for v1.1 - Add price_history table
"""
from app.database import Base, engine
from sqlalchemy import text

def migrate():
    # Create price_history table
    Base.metadata.create_all(engine)
    print("✓ price_history table created")

if __name__ == "__main__":
    migrate()
```

**Run migration:**
```bash
python migrate_v1.1.py
```

---

## Rollback Plan

If issues arise:
1. Comment out chart button/click handler in frontend
2. Chart modal won't open
3. All other functionality remains intact
4. No database rollback needed (price_history table harmless if unused)

---

## Documentation Updates Needed

### User Documentation
- Update README.md with chart feature
- Add screenshot of chart modal
- Update CHANGELOG.md for v1.1

### Technical Documentation
- Document PriceHistoryService API
- Document caching strategy
- Update API documentation

---

## Future Enhancements (Not in v1.1)

### v1.2 Potential Features
- Charts for open positions (real-time)
- Multiple position comparison overlay
- Export chart as PNG/PDF
- Technical indicators (RSI, MACD, Moving Averages)
- Candlestick chart option
- Volume bars below price chart
- Annotations for significant events
- Custom date range selection
- Intraday price data (hourly)

---

## Risk Assessment

### Low Risk
- ✅ Using proven library (Plotly)
- ✅ Simple caching strategy
- ✅ No breaking changes to existing features

### Medium Risk
- ⚠️ yfinance API reliability (mitigated by caching)
- ⚠️ Large date ranges may slow initial load (mitigated by spinner)

### Mitigation Strategies
- Cache all fetched data permanently
- Show loading indicators
- Graceful error handling
- Lazy loading (only on chart open)

---

## Definition of Done

- [ ] All code implemented and tested
- [ ] Unit tests passing (if applicable)
- [ ] Manual testing completed (all test cases pass)
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] No console errors
- [ ] Performance acceptable
- [ ] Mobile testing completed
- [ ] Merged to main branch
- [ ] Version tagged as v1.1.0

---

## Estimated Timeline

**Total: 8-10 hours**

- Backend implementation: 3-4 hours
- Frontend implementation: 3-4 hours
- Testing & polish: 1-2 hours
- Documentation: 1 hour

**Recommended approach:** Implement and test in phases as outlined above.

---

**Status:** ✅ APPROVED - Ready for Implementation  
**Next Step:** Begin Phase 1 (Database & Backend)  
**Implementation Guide:** Follow phases sequentially, test each phase before proceeding

---

*This briefing is complete and ready to be handed off to a developer or used as a guide for implementation in a fresh context.*
