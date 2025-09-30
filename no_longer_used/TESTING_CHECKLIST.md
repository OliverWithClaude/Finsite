# Testing Checklist for Position Management

## Prerequisites
- [ ] Server is running (`start_server.bat`)
- [ ] Browser is open at http://127.0.0.1:8000

## Test 1: Open a Position

### Steps:
1. [ ] Navigate to Watchlist view (should be default)
2. [ ] Add ticker "AAPL" if not present
3. [ ] Click "Buy" button next to AAPL
4. [ ] Verify buy modal opens with "Open Position - AAPL" title
5. [ ] Fill in form:
   - Entry Date: 2025-09-01
   - Entry Value: 3001
   - Entry Price per Share: 150.50
   - Currency: USD
6. [ ] Click "Open Position"
7. [ ] Verify success message appears
8. [ ] Verify modal closes

### Expected Results:
- ✓ Position created in database
- ✓ No errors in browser console
- ✓ Success toast appears

## Test 2: View Open Positions

### Steps:
1. [ ] Click "Open Positions" in navigation
2. [ ] Verify table displays with AAPL position
3. [ ] Check all columns are populated:
   - [ ] Ticker shows "AAPL"
   - [ ] Entry Date shows "2025-09-01"
   - [ ] Entry Value shows "€3,001.00"
   - [ ] Entry Price shows "150.5 USD"
   - [ ] Current Price shows a value (from yfinance)
   - [ ] Current Value is calculated
   - [ ] Unrealized P/L shows value and percentage
4. [ ] Verify profit/loss is color-coded (green or red)

### Expected Results:
- ✓ Table renders correctly
- ✓ Current price fetched from yfinance
- ✓ Calculations are correct
- ✓ Colors indicate profit (green) or loss (red)

## Test 3: Close a Position

### Steps:
1. [ ] From Open Positions view, click "Close" button on AAPL
2. [ ] Verify sell modal opens with "Close Position - AAPL" title
3. [ ] Verify reference section shows:
   - [ ] Entry Date: 2025-09-01
   - [ ] Entry Value: €3,001.00
   - [ ] Entry Price per Share: 150.5 USD
4. [ ] Fill in form:
   - Exit Date: 2025-09-30
   - Exit Value: 3011
   - Exit Price per Share: 151.00
   - Currency: USD (should be pre-selected)
5. [ ] Click "Close Position"
6. [ ] Verify success message appears
7. [ ] Verify modal closes
8. [ ] Verify position disappears from Open Positions table

### Expected Results:
- ✓ Position closed in database
- ✓ Reference data displays correctly
- ✓ Form submits successfully
- ✓ Position removed from open list

## Test 4: View Closed Positions

### Steps:
1. [ ] Click "Closed Positions" in navigation
2. [ ] Verify table displays with AAPL position
3. [ ] Check all columns are populated:
   - [ ] Ticker shows "AAPL"
   - [ ] Entry Date shows "2025-09-01"
   - [ ] Entry Value shows "€3,001.00"
   - [ ] Exit Date shows "2025-09-30"
   - [ ] Exit Value shows "€3,011.00"
   - [ ] Profit/Loss shows "€10.00" (green)
   - [ ] P/L % shows "0.33%" (green)
   - [ ] Days Held shows "29"

### Expected Results:
- ✓ Table renders correctly
- ✓ Profit calculation is correct (€10)
- ✓ Percentage is correct (0.33%)
- ✓ Holding period is correct (29 days)
- ✓ Green color for profit

## Test 5: Multiple Positions

### Steps:
1. [ ] Go back to Watchlist
2. [ ] Open another position (e.g., MSFT)
3. [ ] Navigate to Open Positions
4. [ ] Verify both positions are listed
5. [ ] Close one position
6. [ ] Verify it moves to Closed Positions
7. [ ] Verify other position remains in Open Positions

### Expected Results:
- ✓ Multiple positions per ticker work
- ✓ Each position tracked independently
- ✓ Status updates correctly

## Test 6: Navigation

### Steps:
1. [ ] Click each navigation tab (Watchlist, Open Positions, Closed Positions)
2. [ ] Verify active tab is highlighted
3. [ ] Verify correct view is displayed
4. [ ] Verify views switch smoothly

### Expected Results:
- ✓ Navigation works smoothly
- ✓ Active state displays correctly
- ✓ No console errors

## Test 7: Edge Cases

### Empty States:
1. [ ] View Open Positions with no open positions
   - Should show: "No open positions yet..."
2. [ ] View Closed Positions with no closed positions
   - Should show: "No closed positions yet."

### Modal Cancel:
1. [ ] Open buy modal and click Cancel
   - Should close without creating position
2. [ ] Open sell modal and click Cancel
   - Should close without closing position
3. [ ] Click outside modal (on overlay)
   - Should close modal

### Form Validation:
1. [ ] Try to submit buy form with empty fields
   - Should show HTML5 validation errors
2. [ ] Try to enter negative values
   - Should show validation error

### Expected Results:
- ✓ Empty states display correctly
- ✓ Cancel works properly
- ✓ Form validation prevents bad data

## Test 8: Current Price Fetching

### Steps:
1. [ ] Open position with real ticker (AAPL)
2. [ ] View in Open Positions
3. [ ] Wait for current price to load
4. [ ] Verify current value calculation is reasonable
5. [ ] Try with invalid ticker
   - Current price should show "N/A"

### Expected Results:
- ✓ yfinance integration works
- ✓ Graceful handling of price fetch failures
- ✓ Calculations use live prices

## Issues Found

Record any issues here:

1. Issue: 
   Fix: 

2. Issue:
   Fix:

## Overall Assessment

- [ ] All tests passed
- [ ] Ready for production use
- [ ] Documentation is complete
- [ ] Code is committed to git

## Notes

Add any additional observations or suggestions here:
