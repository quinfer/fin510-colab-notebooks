# Lab 7 - Bloomberg Crypto Data

## Overview

This folder contains **institutional-quality cryptocurrency data from Bloomberg Terminal** for use in Lab 7.

**Data file**: `crypto_bloomberg.csv`

---

## Data Details

**Source**: Bloomberg Terminal (XBTUSD Curncy)  
**Period**: January 2018 - November 2025 (2,052 trading days)  
**Frequency**: Daily  
**Fields**:
- `date`: Trading date
- `security`: Bloomberg ticker (XBTUSD Curncy)
- `price`: Last Price (PX_LAST) - closing price in USD
- `volume`: Trading volume (PX_VOLUME)

**Price range**: $3,157 (2018 low) to $125,261 (2025 high)

---

## How Students Access This Data

### Default: Google Colab / Remote (Recommended)
Lab 7 automatically loads from GitHub - **just run the lab, no setup needed!**

```python
btc_data = load_bloomberg_crypto()
# ✅ Loads from GitHub automatically
# 📥 Loading Bloomberg data from GitHub...
# ✅ Loaded Bloomberg data: 2,052 rows
#    Source: GitHub (quinfer/financial-data-science)
```

### Alternative: Manual GitHub Load
If you want to load directly:

```python
url = "https://raw.githubusercontent.com/quinfer/financial-data-science/main/data/chapter07/crypto_bloomberg.csv"
df = pd.read_csv(url, parse_dates=['date'])
df = df.set_index('date')
```

### Alternative: Local (On Campus with Repo)
If running locally with full course repository:

```python
df = pd.read_csv('data/chapter07/crypto_bloomberg.csv', parse_dates=['date'])
df = df.set_index('date')
```

**Lab 7 tries GitHub first**, then falls back to local if GitHub unavailable.

---

## Data Quality

✅ **Institutional-grade pricing** from Bloomberg Terminal  
✅ **Validated by Bloomberg** - no wash trading or fake volumes  
✅ **Corporate actions handled** - splits, forks properly adjusted  
✅ **Continuous time series** - no gaps or missing data  
✅ **7+ years of history** - covers multiple market cycles (bull/bear)

**Why Bloomberg > Free APIs**:
- Free APIs (CoinGecko, yfinance) often have data gaps, wash trading, and inconsistent pricing
- Bloomberg validates all prices against multiple exchanges
- Used by hedge funds and institutions for actual trading decisions

---

## How This Was Created

### Step 1: Bloomberg Terminal Export
1. Open Bloomberg Terminal
2. Type: `XBTUSD Curncy<GO>`
3. Type: `HP<GO>` (Historical Prices)
4. Select: Start Date = 01/01/2018, End Date = Today
5. Export to Excel → Save as `data/crypto.xlsx`

### Step 2: Convert to Student-Friendly CSV
```bash
python scripts/convert_bloomberg_to_csv.py
# Output: data/chapter07/crypto_bloomberg.csv
```

### Step 3: Commit to Git
```bash
git add data/chapter07/crypto_bloomberg.csv
git commit -m "Add Bloomberg crypto data for Lab 7"
git push origin main
```

### Step 4: Students Access via GitHub
Once pushed, students can load directly from:
```
https://raw.githubusercontent.com/quinfer/financial-data-science/main/data/chapter07/crypto_bloomberg.csv
```

---

## Updating the Data

To refresh with latest prices:

```bash
# 1. Re-export from Bloomberg Terminal (HP<GO>)
# 2. Run conversion script
python scripts/convert_bloomberg_to_csv.py

# 3. Check the new data
head -5 data/chapter07/crypto_bloomberg.csv

# 4. Commit and push
git add data/chapter07/crypto_bloomberg.csv
git commit -m "Update Bitcoin data to $(date +%Y-%m-%d)"
git push origin main
```

Students' labs will automatically use the updated data next time they run.

---

## Alternative Data Sources (If Bloomberg Unavailable)

If Bloomberg Terminal is not available:

1. **Yahoo Finance** (free, decent quality):
   ```python
   import yfinance as yf
   btc = yf.download('BTC-USD', period='2y')
   ```

2. **CoinGecko Pro** (paid, good quality):
   ```python
   # Requires API key
   url = f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
   ```

3. **Historical CSV archives** (for teaching):
   - Kaggle has crypto datasets
   - CryptoDataDownload.com provides free historical data

**For production/research**: Always use Bloomberg or equivalent institutional source.

---

## File Structure

```
data/chapter07/
├── crypto_bloomberg.csv      # Clean CSV for students (69 KB)
├── README.md                 # This file
└── bloomberg/                # Raw Bloomberg exports (optional)
    └── cryptocurrencies.csv  # If using Python API export
```

---

## License & Attribution

**Data Source**: Bloomberg L.P.  
**License**: For educational use only (Ulster University FIN510/FIN720)  
**Do not redistribute** Bloomberg data outside course context.

For research/publication, cite as:
> Bitcoin price data obtained from Bloomberg Terminal (XBTUSD Curncy), accessed [date].

---

## Questions?

**Professor Barry Quinn** (b.quinn1@ulster.ac.uk)

For technical issues with data loading, see Lab 7 or contact during office hours.
