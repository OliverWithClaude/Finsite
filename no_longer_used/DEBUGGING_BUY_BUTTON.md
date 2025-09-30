# Debugging Guide - Buy Button Not Visible

## Issue
The "Buy" button is not appearing next to tickers in the watchlist.

## Solution Applied
Made the `openBuyModal`, `deleteTicker`, and `openSellModal` functions globally accessible by attaching them to the `window` object.

## How to Verify the Fix

### 1. Check if Server is Running
```bash
cd C:\Claude\Finsite
start_server.bat
```

### 2. Open Browser Console (F12)
Navigate to http://127.0.0.1:8000 and open Developer Tools (F12)

### 3. Check for JavaScript Errors
Look in the Console tab for any red error messages.

### 4. Verify Functions are Global
In the Console tab, type:
```javascript
typeof window.openBuyModal
```
Should return: `"function"`

### 5. Manually Test the Buy Modal
In the Console tab, type:
```javascript
window.openBuyModal('AAPL')
```
The buy modal should open.

### 6. Check if Tickers are Loading
In the Console tab, type:
```javascript
currentTickers
```
Should show an array of your tickers.

### 7. Inspect the HTML
- Right-click on the watchlist area
- Select "Inspect Element"
- Look for ticker items with class `ticker-item`
- Each should have a "Buy" button inside `ticker-actions`

## Common Issues and Fixes

### Issue: "openBuyModal is not defined"
**Cause**: Functions not in global scope
**Fix**: Already applied - functions are now attached to `window` object

### Issue: Buy button not visible but exists in HTML
**Cause**: CSS issue
**Fix**: Check if `.btn-success` class is defined in style.css (already added)

### Issue: Tickers not loading
**Cause**: API connection issue
**Fix**: 
1. Check server is running
2. Check network tab in DevTools for 404 errors
3. Verify database exists at `C:\Claude\Finsite\data\finsite.db`

### Issue: Modal doesn't open when button clicked
**Cause**: Event not firing
**Fix**: Check browser console for errors

## Quick Test Script

Paste this into your browser console to test everything:

```javascript
// Test 1: Check if functions exist
console.log('openBuyModal exists:', typeof window.openBuyModal === 'function');
console.log('deleteTicker exists:', typeof window.deleteTicker === 'function');
console.log('openSellModal exists:', typeof window.openSellModal === 'function');

// Test 2: Check if elements exist
console.log('buyModal exists:', document.getElementById('buyModal') !== null);
console.log('tickerList exists:', document.getElementById('tickerList') !== null);

// Test 3: Check if tickers loaded
fetch('/api/tickers')
    .then(r => r.json())
    .then(data => console.log('Tickers:', data))
    .catch(err => console.error('Error loading tickers:', err));

// Test 4: Try opening modal
setTimeout(() => {
    console.log('Attempting to open buy modal...');
    window.openBuyModal('TEST');
}, 2000);
```

## Expected Result

After loading the page with tickers in your watchlist, you should see:

```
┌─────────────────────────────────────┐
│ Watchlist                  [+ Add]  │
├─────────────────────────────────────┤
│ AAPL                    [Buy] [Remove]
│ Apple Inc.                          │
├─────────────────────────────────────┤
│ MSFT                    [Buy] [Remove]
│ Microsoft Corp.                     │
└─────────────────────────────────────┘
```

The [Buy] button should be teal/cyan colored.

## If Still Not Working

1. **Hard refresh** the page: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
2. **Clear browser cache**: Settings > Privacy > Clear browsing data
3. **Check file was saved**: Open `C:\Claude\Finsite\static\js\main.js` and verify it contains `window.openBuyModal`
4. **Restart the server**: Close and reopen `start_server.bat`

## Manual Verification

1. Add a ticker to your watchlist (e.g., "AAPL")
2. You should see:
   - Ticker symbol (AAPL) in bold
   - Company name below it
   - Two buttons on the right: "Buy" (teal) and "Remove" (red)
3. Click the "Buy" button
4. Modal should open with title "Open Position - AAPL"
5. Fill in the form and submit

## Contact Points

If issue persists after all checks:
- Check server logs for errors
- Verify all files were saved correctly
- Try restarting your computer (sometimes caching issues)
