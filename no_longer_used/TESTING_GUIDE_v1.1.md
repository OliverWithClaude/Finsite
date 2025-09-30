# Testing Guide - Charts Feature (v1.1)

## Pre-Testing Setup

### 1. Ensure You Have Test Data
You need at least one closed position to test the chart feature.

**Option A: Use Existing Data**
- If you already have closed positions, skip to testing

**Option B: Create Test Data**
1. Add a ticker (e.g., AAPL)
2. Open a position (Buy)
3. Close the position (Sell)
4. Now you have a closed position to test with

---

## Manual Testing Checklist

### Basic Functionality Tests

#### Test 1: Open Chart Modal
- [ ] Navigate to "Closed Positions" tab
- [ ] Locate the "Chart" button next to a closed position
- [ ] Click the "Chart" button
- [ ] **Expected**: Modal opens with loading spinner
- [ ] **Expected**: Chart loads within 3-5 seconds
- [ ] **Expected**: Chart displays with price line and markers

#### Test 2: Chart Display
- [ ] Verify chart title shows correct ticker symbol
- [ ] Verify blue line shows price movement
- [ ] Verify teal dot marks entry point
- [ ] Verify orange dot marks exit point
- [ ] Verify "Entry" and "Exit" labels appear above markers
- [ ] **Expected**: All elements visible and properly styled

#### Test 3: Interactive Features
- [ ] Hover over the price line
- [ ] **Expected**: Tooltip shows price value
- [ ] Click and drag to select an area
- [ ] **Expected**: Chart zooms into selected area
- [ ] Try panning the zoomed chart
- [ ] **Expected**: Chart moves as you drag
- [ ] Double-click the chart
- [ ] **Expected**: Zoom resets to original view

#### Test 4: Close Modal
- [ ] Click the X button in modal header
- [ ] **Expected**: Modal closes
- [ ] Open chart again
- [ ] Click outside the modal (on dark overlay)
- [ ] **Expected**: Modal closes

---

### Date Range Tests

#### Test 5: Recent Position (Closed < 3 months ago)
**Setup**: Create/use a position closed within last 90 days

- [ ] Open chart for this position
- [ ] Check the date range on X-axis
- [ ] **Expected**: Chart starts 3 months before entry
- [ ] **Expected**: Chart ends at today's date
- [ ] **Expected**: Date range includes current date

#### Test 6: Old Position (Closed > 3 months ago)
**Setup**: Create/use a position closed more than 90 days ago

- [ ] Open chart for this position
- [ ] Check the date range on X-axis
- [ ] **Expected**: Chart starts 3 months before entry
- [ ] **Expected**: Chart ends 3 months after exit
- [ ] **Expected**: Date range is fixed (doesn't extend to today)

---

### Data Accuracy Tests

#### Test 7: Entry Price Verification
- [ ] Note the entry price from the position table
- [ ] Open the chart
- [ ] Hover over the teal entry marker
- [ ] **Expected**: Entry marker price matches table entry price (within rounding)

#### Test 8: Exit Price Verification
- [ ] Note entry value and exit value from table
- [ ] Calculate expected exit price: exit_value / (entry_value / entry_price)
- [ ] Open the chart
- [ ] Hover over the orange exit marker
- [ ] **Expected**: Exit marker price matches calculated price

#### Test 9: Price Data Accuracy
- [ ] Pick a random date in the chart
- [ ] Note the price shown in chart hover tooltip
- [ ] Go to Yahoo Finance and check historical data for that date
- [ ] **Expected**: Prices match (or very close, accounting for different data sources)

---

### Caching Tests

#### Test 10: First Load Performance
- [ ] Clear browser cache (Ctrl+Shift+Delete)
- [ ] Restart the server
- [ ] Open a chart for the first time
- [ ] **Expected**: Takes 2-5 seconds to load
- [ ] **Expected**: Loading spinner visible during fetch

#### Test 11: Cached Load Performance
- [ ] Close the chart modal
- [ ] Immediately reopen the same chart
- [ ] **Expected**: Loads much faster (< 1 second)
- [ ] **Expected**: No loading spinner (or very brief)

#### Test 12: Database Caching Verification
- [ ] Open a chart for AAPL (or any ticker)
- [ ] Close the modal
- [ ] Close position for different AAPL position (if you have one)
- [ ] Open chart for the second AAPL position
- [ ] **Expected**: Uses cached data, loads fast
- [ ] **Expected**: Same price data reused for overlapping dates

---

### Error Handling Tests

#### Test 13: Invalid Ticker (Manual Test)
**Note**: This requires manually creating a position with an invalid ticker in the database

- [ ] Create a position with ticker "INVALID123"
- [ ] Try to open chart
- [ ] **Expected**: Error message displayed
- [ ] **Expected**: Message says "No price data available" or similar
- [ ] **Expected**: No chart displayed

#### Test 14: Network Error Simulation
**Setup**: Disconnect from internet

- [ ] Disconnect internet
- [ ] Try to open a chart for a ticker not yet cached
- [ ] **Expected**: Error message after timeout
- [ ] **Expected**: Message suggests trying again later
- [ ] Reconnect internet
- [ ] Try again
- [ ] **Expected**: Works normally

#### Test 15: Very Old Position
**Setup**: Create position with entry/exit dates from several years ago

- [ ] Create position from 2020-2021
- [ ] Open chart
- [ ] **Expected**: Chart loads successfully
- [ ] **Expected**: Date range shows 2019-2021 timeframe
- [ ] **Expected**: Historical data displayed correctly

---

### Mobile/Responsive Tests

#### Test 16: Mobile View
- [ ] Open browser developer tools (F12)
- [ ] Toggle device toolbar (mobile view)
- [ ] Set viewport to iPhone/Android size
- [ ] Navigate to closed positions
- [ ] Click "Chart" button
- [ ] **Expected**: Modal fills screen
- [ ] **Expected**: Chart is readable
- [ ] **Expected**: Can interact with chart (zoom/pan)
- [ ] **Expected**: Close button accessible

#### Test 17: Tablet View
- [ ] Set viewport to tablet size (iPad)
- [ ] Test chart opening and closing
- [ ] **Expected**: Modal sized appropriately
- [ ] **Expected**: Chart clearly visible
- [ ] **Expected**: All interactions work

---

### Edge Cases

#### Test 18: Position with 1-Day Holding Period
**Setup**: Create position where entry and exit are same date

- [ ] Open chart
- [ ] **Expected**: Chart still loads
- [ ] **Expected**: Both markers visible (may overlap)
- [ ] **Expected**: Date range spans 6 months

#### Test 19: Position Closed Today
**Setup**: Create and immediately close a position

- [ ] Open chart
- [ ] **Expected**: Chart extends to today
- [ ] **Expected**: Exit marker at end of chart
- [ ] **Expected**: Recent data visible

#### Test 20: Multiple Tickers
- [ ] Open charts for 3-5 different tickers
- [ ] Close and reopen each chart
- [ ] **Expected**: Each chart loads correctly
- [ ] **Expected**: Data doesn't mix between tickers
- [ ] **Expected**: Cached data improves load time

---

## Automated Testing (Optional)

### API Endpoint Test

Test the chart data endpoint directly:

```bash
# Replace {position_id} with actual ID
curl http://localhost:8000/api/positions/{position_id}/chart-data
```

**Expected Response:**
```json
{
  "ticker": "AAPL",
  "entry_date": "2025-01-15",
  "exit_date": "2025-03-20",
  "entry_price": 150.50,
  "exit_price": 155.00,
  "entry_currency": "USD",
  "start_date": "2024-10-15",
  "end_date": "2025-09-30",
  "prices": [
    {"date": "2024-10-15", "close": 145.20},
    ...
  ],
  "error": null
}
```

---

## Performance Benchmarks

### Expected Performance

| Scenario | Expected Time | Status |
|----------|--------------|--------|
| First chart load (no cache) | 2-4 seconds | [ ] |
| Cached chart load | < 1 second | [ ] |
| Multiple chart opens | < 1 second each | [ ] |
| Chart rendering | Instant | [ ] |
| Modal open/close | Instant | [ ] |

### Performance Test
1. Open chart → measure time
2. Close chart
3. Reopen chart → measure time
4. **Expected**: Second load significantly faster

---

## Bug Report Template

If you find issues, document them:

```
**Bug**: [Brief description]

**Steps to Reproduce**:
1. Step one
2. Step two
3. ...

**Expected Behavior**: 
[What should happen]

**Actual Behavior**: 
[What actually happened]

**Browser**: [Chrome/Firefox/etc.]
**Version**: [v1.1.0]
**Position Details**: [Ticker, dates if relevant]

**Screenshots**: [If applicable]
```

---

## Test Results Summary

### Functionality: __ / 20 Tests Passed
- [ ] Basic functionality (Tests 1-4)
- [ ] Date ranges (Tests 5-6)
- [ ] Data accuracy (Tests 7-9)
- [ ] Caching (Tests 10-12)
- [ ] Error handling (Tests 13-15)
- [ ] Mobile responsive (Tests 16-17)
- [ ] Edge cases (Tests 18-20)

### Performance: __ / 5 Benchmarks Met
- [ ] First load < 4 seconds
- [ ] Cached load < 1 second
- [ ] Chart renders instantly
- [ ] Modal opens instantly
- [ ] No lag during interaction

---

## Sign-Off

**Tester**: _________________  
**Date**: _________________  
**Overall Status**: [ ] PASS  [ ] FAIL  [ ] NEEDS REVIEW  

**Notes**:
_____________________________________
_____________________________________
_____________________________________

---

**Testing Complete!** 
If all tests pass, the feature is ready for production use. 🎉
