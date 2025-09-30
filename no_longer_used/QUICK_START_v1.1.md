# Quick Start Guide - Charts Feature (v1.1)

## Installation Steps

### 1. Install New Dependency
Open a command prompt in the Finsite directory and run:

```bash
pip install plotly==5.24.1
```

Or install all dependencies:

```bash
pip install -r requirements.txt
```

### 2. Run Database Migration
This creates the `price_history` table for caching price data:

```bash
python migrate_v1.1.py
```

You should see:
```
Starting migration for v1.1 - Chart feature...
✓ price_history table created

Migration completed successfully!
You can now use the chart feature for closed positions.
```

### 3. Start the Server
```bash
start_server.bat
```

Or manually:
```bash
python -m uvicorn app.main:app --reload
```

### 4. Test the Feature
1. Open your browser to `http://localhost:8000`
2. Navigate to **"Closed Positions"** tab
3. Click the **"Chart"** button on any closed position
4. View the interactive price chart!

---

## What You'll See

### Chart Modal
- **Loading State**: Spinner while fetching price data
- **Interactive Chart**: 
  - Blue line showing price movement
  - Teal dot marking your entry point
  - Orange dot marking your exit point
  - Hover over the line to see prices
  - Zoom and pan to explore the data

### Date Range
- **Recent positions** (closed < 3 months ago): Chart shows from 3 months before entry until today
- **Older positions**: Chart shows from 3 months before entry to 3 months after exit

---

## Troubleshooting

### Issue: Chart button doesn't appear
**Solution**: Hard refresh your browser (Ctrl+F5) to clear cached JavaScript/CSS

### Issue: "Unable to load chart data"
**Possible causes:**
1. No internet connection (yfinance needs internet)
2. Ticker symbol is invalid or delisted
3. Yahoo Finance is temporarily unavailable

**Solution**: Try again later or check if the ticker is valid

### Issue: Chart is slow to load
**Explanation**: First load for a ticker fetches data from Yahoo Finance (2-4 seconds). Subsequent loads use cached data and are much faster (< 1 second).

### Issue: Migration error
**Solution**: Make sure you're in the Finsite directory and the database exists. If issues persist, delete the `data/finsite.db` file and run the app again to recreate the database, then run the migration.

---

## Features to Try

1. **Zoom**: Click and drag on the chart to zoom into a specific time period
2. **Pan**: After zooming, drag the chart to move around
3. **Reset**: Double-click the chart to reset zoom
4. **Hover**: Hover over any point to see the exact price and date
5. **Legend**: Click legend items to show/hide traces

---

## Performance Notes

### First Load
- Fetches historical data from Yahoo Finance
- Stores data in local database
- Takes 2-4 seconds

### Subsequent Loads
- Uses cached data from database
- Much faster (< 1 second)
- No additional API calls to Yahoo Finance

---

## Next Steps

1. **Test with multiple positions**: Try charts for different stocks
2. **Observe caching**: Notice how the second load is much faster
3. **Explore the data**: Use zoom/pan to examine specific periods
4. **Provide feedback**: Let us know what additional features you'd like!

---

## Quick Reference

| Action | Result |
|--------|--------|
| Click "Chart" button | Opens chart modal |
| Click X or outside modal | Closes chart |
| Hover over chart | Shows price tooltip |
| Click and drag | Zoom to selection |
| Double-click | Reset zoom |

---

**Ready to use!** 🎉

Open a closed position chart and explore your trading history visually!
