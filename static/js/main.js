/**
 * Finsite - Main JavaScript Application
 * Investment Intelligence with Grit
 */

// Global state
let currentTickers = [];
let selectedTicker = null;
let isValidated = false;
let currentView = 'watchlist';
let selectedPosition = null;

// API endpoints
const API = {
    tickers: '/api/tickers',
    tickerInfo: '/api/ticker-info',
    validateTicker: '/api/validate-ticker',
    positionsOpen: '/api/positions/open',
    positionsClosed: '/api/positions/closed',
    positionClose: (id) => `/api/positions/${id}/close`
};

// DOM elements
const elements = {
    // Navigation
    navBtns: document.querySelectorAll('.nav-btn'),
    
    // Views
    watchlistView: document.getElementById('watchlistView'),
    openPositionsView: document.getElementById('openPositionsView'),
    closedPositionsView: document.getElementById('closedPositionsView'),
    
    // Watchlist elements
    addTickerBtn: document.getElementById('addTickerBtn'),
    addTickerForm: document.getElementById('addTickerForm'),
    tickerSymbol: document.getElementById('tickerSymbol'),
    tickerName: document.getElementById('tickerName'),
    validateBtn: document.getElementById('validateBtn'),
    saveTickerBtn: document.getElementById('saveTickerBtn'),
    cancelBtn: document.getElementById('cancelBtn'),
    validationMessage: document.getElementById('validationMessage'),
    tickerList: document.getElementById('tickerList'),
    tickerInfo: document.getElementById('tickerInfo'),
    
    // Position lists
    openPositionsList: document.getElementById('openPositionsList'),
    closedPositionsList: document.getElementById('closedPositionsList'),
    
    // Modals
    buyModal: document.getElementById('buyModal'),
    buyModalTicker: document.getElementById('buyModalTicker'),
    buyForm: document.getElementById('buyForm'),
    buyDate: document.getElementById('buyDate'),
    buyValue: document.getElementById('buyValue'),
    buyPrice: document.getElementById('buyPrice'),
    buyCurrency: document.getElementById('buyCurrency'),
    buyModalCancel: document.getElementById('buyModalCancel'),
    
    sellModal: document.getElementById('sellModal'),
    sellModalTicker: document.getElementById('sellModalTicker'),
    sellForm: document.getElementById('sellForm'),
    sellDate: document.getElementById('sellDate'),
    sellValue: document.getElementById('sellValue'),
    sellCurrency: document.getElementById('sellCurrency'),
    sellModalCancel: document.getElementById('sellModalCancel'),
    sellRefEntryDate: document.getElementById('sellRefEntryDate'),
    sellRefEntryValue: document.getElementById('sellRefEntryValue'),
    sellRefEntryPrice: document.getElementById('sellRefEntryPrice'),
    
    // Utility
    loadingOverlay: document.getElementById('loadingOverlay'),
    errorToast: document.getElementById('errorToast'),
    errorMessage: document.getElementById('errorMessage')
};

// Initialize application
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    loadTickers();
});

// Event Listeners
function initializeEventListeners() {
    // Navigation
    elements.navBtns.forEach(btn => {
        btn.addEventListener('click', () => switchView(btn.dataset.view));
    });
    
    // Watchlist
    elements.addTickerBtn.addEventListener('click', showAddTickerForm);
    elements.cancelBtn.addEventListener('click', hideAddTickerForm);
    elements.validateBtn.addEventListener('click', validateTicker);
    elements.saveTickerBtn.addEventListener('click', saveTicker);
    elements.tickerSymbol.addEventListener('input', onSymbolInput);
    elements.tickerSymbol.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') validateTicker();
    });
    
    // Buy Modal
    elements.buyModalCancel.addEventListener('click', closeBuyModal);
    elements.buyForm.addEventListener('submit', handleBuySubmit);
    document.querySelectorAll('#buyModal .modal-close').forEach(btn => {
        btn.addEventListener('click', closeBuyModal);
    });
    elements.buyModal.addEventListener('click', (e) => {
        if (e.target === elements.buyModal) closeBuyModal();
    });
    
    // Sell Modal
    elements.sellModalCancel.addEventListener('click', closeSellModal);
    elements.sellForm.addEventListener('submit', handleSellSubmit);
    document.querySelectorAll('#sellModal .modal-close').forEach(btn => {
        btn.addEventListener('click', closeSellModal);
    });
    elements.sellModal.addEventListener('click', (e) => {
        if (e.target === elements.sellModal) closeSellModal();
    });
    
    // Set default date to today
    const today = new Date().toISOString().split('T')[0];
    elements.buyDate.value = today;
    elements.sellDate.value = today;
}

// Navigation
function switchView(view) {
    currentView = view;
    
    // Update nav buttons
    elements.navBtns.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.view === view);
    });
    
    // Update views
    elements.watchlistView.classList.toggle('active', view === 'watchlist');
    elements.openPositionsView.classList.toggle('active', view === 'open-positions');
    elements.closedPositionsView.classList.toggle('active', view === 'closed-positions');
    
    // Load data for the view
    if (view === 'open-positions') {
        loadOpenPositions();
    } else if (view === 'closed-positions') {
        loadClosedPositions();
    }
}

// Show/Hide Add Ticker Form
function showAddTickerForm() {
    elements.addTickerForm.classList.remove('hidden');
    elements.addTickerBtn.classList.add('hidden');
    elements.tickerSymbol.focus();
}

function hideAddTickerForm() {
    elements.addTickerForm.classList.add('hidden');
    elements.addTickerBtn.classList.remove('hidden');
    resetForm();
}

function resetForm() {
    elements.tickerSymbol.value = '';
    elements.tickerName.value = '';
    elements.validationMessage.textContent = '';
    elements.validationMessage.className = 'validation-message';
    elements.saveTickerBtn.disabled = true;
    isValidated = false;
}

function onSymbolInput() {
    elements.tickerSymbol.value = elements.tickerSymbol.value.toUpperCase();
    if (isValidated) {
        isValidated = false;
        elements.tickerName.value = '';
        elements.saveTickerBtn.disabled = true;
        elements.validationMessage.textContent = '';
        elements.validationMessage.className = 'validation-message';
    }
}

// Validate Ticker Symbol
async function validateTicker() {
    const symbol = elements.tickerSymbol.value.trim();
    
    if (!symbol) {
        showValidationMessage('Please enter a ticker symbol', 'error');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API.validateTicker}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ symbol })
        });
        
        const data = await response.json();
        
        if (response.ok && data.valid) {
            elements.tickerName.value = data.name;
            elements.saveTickerBtn.disabled = false;
            isValidated = true;
            showValidationMessage(`✓ ${data.name} found`, 'success');
        } else {
            showValidationMessage('Invalid ticker symbol', 'error');
            elements.tickerName.value = '';
            elements.saveTickerBtn.disabled = true;
            isValidated = false;
        }
    } catch (error) {
        showError('Failed to validate ticker');
        showValidationMessage('Validation failed', 'error');
    } finally {
        hideLoading();
    }
}

// Save Ticker
async function saveTicker() {
    if (!isValidated) return;
    
    const symbol = elements.tickerSymbol.value.trim();
    const name = elements.tickerName.value.trim();
    
    showLoading();
    
    try {
        const response = await fetch(API.tickers, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ symbol, name })
        });
        
        if (response.ok) {
            await loadTickers();
            hideAddTickerForm();
            showSuccess(`${symbol} added to watchlist`);
        } else {
            const error = await response.json();
            showError(error.detail || 'Failed to add ticker');
        }
    } catch (error) {
        showError('Failed to save ticker');
    } finally {
        hideLoading();
    }
}

// Load Tickers
async function loadTickers() {
    try {
        const response = await fetch(API.tickers);
        const tickers = await response.json();
        currentTickers = tickers;
        renderTickerList(tickers);
    } catch (error) {
        showError('Failed to load tickers');
        renderTickerList([]);
    }
}

// Render Ticker List
function renderTickerList(tickers) {
    if (tickers.length === 0) {
        elements.tickerList.innerHTML = `
            <div class="info-placeholder">
                <p>No tickers in your watchlist yet.</p>
                <p>Click "Add Ticker" to get started.</p>
            </div>
        `;
        return;
    }
    
    elements.tickerList.innerHTML = tickers.map(ticker => `
        <div class="ticker-item" data-symbol="${ticker.symbol}">
            <div class="ticker-details">
                <div class="ticker-symbol">${ticker.symbol}</div>
                <div class="ticker-name">${ticker.name}</div>
            </div>
            <div class="ticker-actions">
                <button class="btn btn-success" onclick="openBuyModal('${ticker.symbol}')">Buy</button>
                <button class="btn btn-danger" onclick="deleteTicker('${ticker.symbol}')">Remove</button>
            </div>
        </div>
    `).join('');
    
    // Add click handlers for ticker selection
    document.querySelectorAll('.ticker-item').forEach(item => {
        item.addEventListener('click', (e) => {
            if (!e.target.classList.contains('btn')) {
                selectTicker(item.dataset.symbol);
            }
        });
    });
}

// Select Ticker
async function selectTicker(symbol) {
    // Update UI to show selection
    document.querySelectorAll('.ticker-item').forEach(item => {
        item.classList.remove('active');
    });
    const tickerItem = document.querySelector(`[data-symbol="${symbol}"]`);
    if (tickerItem) {
        tickerItem.classList.add('active');
    }
    
    selectedTicker = symbol;
    showLoading();
    
    try {
        const response = await fetch(`${API.tickerInfo}/${symbol}`);
        const data = await response.json();
        
        if (response.ok) {
            renderTickerInfo(data);
        } else {
            showError(data.detail || 'Failed to load ticker information');
            renderTickerInfoError();
        }
    } catch (error) {
        showError('Failed to load ticker information');
        renderTickerInfoError();
    } finally {
        hideLoading();
    }
}

// Render Ticker Information
function renderTickerInfo(info) {
    const changeClass = info.change >= 0 ? 'positive' : 'negative';
    const changeSymbol = info.change >= 0 ? '+' : '';
    
    elements.tickerInfo.innerHTML = `
        <div class="company-header">
            <h2 class="company-title">${info.symbol}</h2>
            <p class="company-subtitle">${info.name}</p>
        </div>
        
        <div class="price-section">
            <div class="current-price">
                ${info.currency || '$'}${formatNumber(info.current_price, 2)}
            </div>
            ${info.change !== null ? `
                <div class="price-change ${changeClass}">
                    ${changeSymbol}${formatNumber(info.change, 2)} (${changeSymbol}${formatNumber(info.change_percent, 2)}%)
                </div>
            ` : ''}
        </div>
        
        <div class="info-grid">
            ${renderInfoCard('Market Cap', formatLargeNumber(info.market_cap))}
            ${renderInfoCard('P/E Ratio', formatNumber(info.pe_ratio, 2))}
            ${renderInfoCard('52 Week High', formatCurrency(info.week_52_high))}
            ${renderInfoCard('52 Week Low', formatCurrency(info.week_52_low))}
            ${renderInfoCard('Volume', formatLargeNumber(info.volume))}
            ${renderInfoCard('Avg Volume', formatLargeNumber(info.avg_volume))}
            ${renderInfoCard('Dividend Yield', info.dividend_yield ? `${formatNumber(info.dividend_yield * 100, 2)}%` : 'N/A')}
            ${renderInfoCard('Beta', formatNumber(info.beta, 2))}
            ${renderInfoCard('Sector', info.sector || 'N/A')}
            ${renderInfoCard('Industry', info.industry || 'N/A')}
            ${renderInfoCard('Exchange', info.exchange || 'N/A')}
            ${info.earnings_date ? renderInfoCard('Next Earnings', info.earnings_date) : ''}
        </div>
        
        ${info.description ? `
            <div class="company-description">
                <h3>About ${info.name}</h3>
                <p>${info.description}</p>
            </div>
        ` : ''}
        
        ${info.website ? `
            <div style="margin-top: var(--spacing-lg);">
                <a href="${info.website}" target="_blank" class="btn btn-secondary">
                    Visit Company Website →
                </a>
            </div>
        ` : ''}
    `;
}

function renderInfoCard(label, value) {
    if (!value || value === 'N/A') return '';
    
    return `
        <div class="info-card">
            <div class="info-label">${label}</div>
            <div class="info-value">${value}</div>
        </div>
    `;
}

function renderTickerInfoError() {
    elements.tickerInfo.innerHTML = `
        <div class="info-placeholder">
            <p>Unable to load information for this ticker.</p>
            <p>Please try again later.</p>
        </div>
    `;
}

// Delete Ticker
window.deleteTicker = async function(symbol) {
    if (!confirm(`Remove ${symbol} from your watchlist?`)) {
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API.tickers}/${symbol}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            await loadTickers();
            if (selectedTicker === symbol) {
                selectedTicker = null;
                elements.tickerInfo.innerHTML = `
                    <div class="info-placeholder">
                        <p>Select a ticker from your watchlist to view detailed information</p>
                    </div>
                `;
            }
            showSuccess(`${symbol} removed from watchlist`);
        } else {
            showError('Failed to remove ticker');
        }
    } catch (error) {
        showError('Failed to remove ticker');
    } finally {
        hideLoading();
    }
}

// Buy Modal Functions
window.openBuyModal = function(symbol) {
    selectedTicker = symbol;
    elements.buyModalTicker.textContent = symbol;
    elements.buyForm.reset();
    const today = new Date().toISOString().split('T')[0];
    elements.buyDate.value = today;
    elements.buyModal.classList.remove('hidden');
}

function closeBuyModal() {
    elements.buyModal.classList.add('hidden');
    elements.buyForm.reset();
}

async function handleBuySubmit(e) {
    e.preventDefault();
    
    const positionData = {
        ticker: selectedTicker,
        entry_date: elements.buyDate.value,
        entry_value_eur: parseFloat(elements.buyValue.value),
        entry_price_per_share: parseFloat(elements.buyPrice.value),
        entry_currency: elements.buyCurrency.value
    };
    
    showLoading();
    
    try {
        const response = await fetch(API.positionsOpen, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(positionData)
        });
        
        if (response.ok) {
            closeBuyModal();
            showSuccess(`Position opened for ${selectedTicker}`);
            // Refresh open positions if we're on that view
            if (currentView === 'open-positions') {
                loadOpenPositions();
            }
        } else {
            const error = await response.json();
            showError(error.detail || 'Failed to open position');
        }
    } catch (error) {
        showError('Failed to open position');
    } finally {
        hideLoading();
    }
}

// Load Open Positions
async function loadOpenPositions() {
    showLoading();
    
    try {
        const response = await fetch(API.positionsOpen);
        const positions = await response.json();
        renderOpenPositions(positions);
    } catch (error) {
        showError('Failed to load open positions');
        elements.openPositionsList.innerHTML = `
            <div class="no-positions">Failed to load positions</div>
        `;
    } finally {
        hideLoading();
    }
}

function renderOpenPositions(positions) {
    if (positions.length === 0) {
        elements.openPositionsList.innerHTML = `
            <div class="no-positions">
                No open positions yet. Open a position from your watchlist.
            </div>
        `;
        return;
    }
    
    elements.openPositionsList.innerHTML = `
        <table class="positions-table">
            <thead>
                <tr>
                    <th>Ticker</th>
                    <th>Entry Date</th>
                    <th>Entry Value</th>
                    <th>Entry Price</th>
                    <th>Current Price</th>
                    <th>Current Value</th>
                    <th>Unrealized P/L</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                ${positions.map(pos => `
                    <tr>
                        <td><strong>${pos.ticker}</strong></td>
                        <td>${pos.entry_date}</td>
                        <td>€${formatNumber(pos.entry_value_eur, 2)}</td>
                        <td>${pos.entry_price_per_share} ${pos.entry_currency}</td>
                        <td>${pos.current_price_per_share ? formatNumber(pos.current_price_per_share, 2) + ' ' + pos.entry_currency : 'N/A'}</td>
                        <td>${pos.current_value_eur ? '€' + formatNumber(pos.current_value_eur, 2) : 'N/A'}</td>
                        <td>
                            ${pos.unrealized_profit_eur !== null ? `
                                <span class="${pos.unrealized_profit_eur >= 0 ? 'profit-positive' : 'profit-negative'}">
                                    €${formatNumber(pos.unrealized_profit_eur, 2)} (${formatNumber(pos.unrealized_profit_percent, 2)}%)
                                </span>
                            ` : 'N/A'}
                        </td>
                        <td>
                            <button class="btn btn-primary" onclick="openSellModal(${pos.id}, '${pos.ticker}', '${pos.entry_date}', ${pos.entry_value_eur}, ${pos.entry_price_per_share}, '${pos.entry_currency}')">
                                Close
                            </button>
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
}

// Sell Modal Functions
window.openSellModal = function(positionId, ticker, entryDate, entryValue, entryPrice, entryCurrency) {
    selectedPosition = positionId;
    elements.sellModalTicker.textContent = ticker;
    elements.sellRefEntryDate.textContent = entryDate;
    elements.sellRefEntryValue.textContent = `€${formatNumber(entryValue, 2)}`;
    elements.sellRefEntryPrice.textContent = `${entryPrice} ${entryCurrency}`;
    
    elements.sellForm.reset();
    const today = new Date().toISOString().split('T')[0];
    elements.sellDate.value = today;
    elements.sellCurrency.value = entryCurrency;
    
    elements.sellModal.classList.remove('hidden');
}

function closeSellModal() {
    elements.sellModal.classList.add('hidden');
    elements.sellForm.reset();
    selectedPosition = null;
}

async function handleSellSubmit(e) {
    e.preventDefault();
    
    const closeData = {
        exit_date: elements.sellDate.value,
        exit_value_eur: parseFloat(elements.sellValue.value),
        exit_currency: elements.sellCurrency.value
    };
    
    showLoading();
    
    try {
        const response = await fetch(API.positionClose(selectedPosition), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(closeData)
        });
        
        if (response.ok) {
            closeSellModal();
            showSuccess('Position closed successfully');
            loadOpenPositions();
        } else {
            const error = await response.json();
            showError(error.detail || 'Failed to close position');
        }
    } catch (error) {
        showError('Failed to close position');
    } finally {
        hideLoading();
    }
}

// Load Closed Positions
async function loadClosedPositions() {
    showLoading();
    
    try {
        const response = await fetch(API.positionsClosed);
        const positions = await response.json();
        renderClosedPositions(positions);
    } catch (error) {
        showError('Failed to load closed positions');
        elements.closedPositionsList.innerHTML = `
            <div class="no-positions">Failed to load positions</div>
        `;
    } finally {
        hideLoading();
    }
}

function renderClosedPositions(positions) {
    if (positions.length === 0) {
        elements.closedPositionsList.innerHTML = `
            <div class="no-positions">
                No closed positions yet.
            </div>
        `;
        return;
    }
    
    elements.closedPositionsList.innerHTML = `
        <table class="positions-table">
            <thead>
                <tr>
                    <th>Ticker</th>
                    <th>Entry Date</th>
                    <th>Entry Value</th>
                    <th>Exit Date</th>
                    <th>Exit Value</th>
                    <th>Profit/Loss</th>
                    <th>P/L %</th>
                    <th>Days Held</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                ${positions.map(pos => `
                    <tr>
                        <td><strong>${pos.ticker}</strong></td>
                        <td>${pos.entry_date}</td>
                        <td>€${formatNumber(pos.entry_value_eur, 2)}</td>
                        <td>${pos.exit_date}</td>
                        <td>€${formatNumber(pos.exit_value_eur, 2)}</td>
                        <td>
                            <span class="${pos.profit_eur >= 0 ? 'profit-positive' : 'profit-negative'}">
                                €${formatNumber(pos.profit_eur, 2)}
                            </span>
                        </td>
                        <td>
                            <span class="${pos.profit_percent >= 0 ? 'profit-positive' : 'profit-negative'}">
                                ${formatNumber(pos.profit_percent, 2)}%
                            </span>
                        </td>
                        <td>${pos.holding_period_days}</td>
                        <td>
                            <button class="btn btn-danger" onclick="deleteClosedPosition(${pos.id}, '${pos.ticker}')">
                                Delete
                            </button>
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
}

// Delete Closed Position
window.deleteClosedPosition = async function(positionId, ticker) {
    if (!confirm(`Delete closed position for ${ticker}?`)) {
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`/api/positions/${positionId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            showSuccess(`Position for ${ticker} deleted successfully`);
            loadClosedPositions();
        } else {
            const error = await response.json();
            showError(error.detail || 'Failed to delete position');
        }
    } catch (error) {
        showError('Failed to delete position');
    } finally {
        hideLoading();
    }
}

// Utility Functions
function formatNumber(num, decimals = 0) {
    if (num === null || num === undefined) return 'N/A';
    return Number(num).toLocaleString('en-US', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
    });
}

function formatCurrency(num) {
    if (num === null || num === undefined) return 'N/A';
    return '$' + formatNumber(num, 2);
}

function formatLargeNumber(num) {
    if (num === null || num === undefined) return 'N/A';
    
    if (num >= 1e12) {
        return '$' + (num / 1e12).toFixed(2) + 'T';
    } else if (num >= 1e9) {
        return '$' + (num / 1e9).toFixed(2) + 'B';
    } else if (num >= 1e6) {
        return '$' + (num / 1e6).toFixed(2) + 'M';
    } else if (num >= 1e3) {
        return formatNumber(num, 0);
    }
    return formatNumber(num, 0);
}

function showValidationMessage(message, type) {
    elements.validationMessage.textContent = message;
    elements.validationMessage.className = `validation-message ${type}`;
}

function showLoading() {
    elements.loadingOverlay.classList.remove('hidden');
}

function hideLoading() {
    elements.loadingOverlay.classList.add('hidden');
}

function showError(message) {
    elements.errorMessage.textContent = message;
    elements.errorToast.classList.remove('hidden');
    setTimeout(() => {
        elements.errorToast.classList.add('hidden');
    }, 5000);
}

function showSuccess(message) {
    // Using the error toast styled differently for success
    elements.errorMessage.textContent = '✓ ' + message;
    elements.errorToast.style.background = 'var(--accent-teal)';
    elements.errorToast.classList.remove('hidden');
    setTimeout(() => {
        elements.errorToast.classList.add('hidden');
        elements.errorToast.style.background = '';
    }, 3000);
}
