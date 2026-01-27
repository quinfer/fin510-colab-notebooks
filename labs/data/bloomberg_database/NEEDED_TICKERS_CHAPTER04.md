# Bloomberg Terminal Commands for Chapter 04 Data

## Missing ETF Tickers

Run these commands in Bloomberg Terminal to extract data:

### 1. TLT US Equity (iShares 20+ Year Treasury Bond ETF)
```
TLT US Equity <EQUITY> <GO>
BDH TLT US Equity PX_LAST 20180101 20241231 DAILY <GO>
```
Export to CSV, save as `tlt_temp.csv`

### 2. GLD US Equity (SPDR Gold Trust)
```
GLD US Equity <EQUITY> <GO>
BDH GLD US Equity PX_LAST 20180101 20241231 DAILY <GO>
```
Export to CSV, save as `gld_temp.csv`

### 3. VNQ US Equity (Vanguard Real Estate ETF)
```
VNQ US Equity <EQUITY> <GO>
BDH VNQ US Equity PX_LAST 20180101 20241231 DAILY <GO>
```
Export to CSV, save as `vnq_temp.csv`

### 4. IWM US Equity (iShares Russell 2000 ETF - Small Cap)
```
IWM US Equity <EQUITY> <GO>
BDH IWM US Equity PX_LAST 20180101 20241231 DAILY <GO>
```
Export to CSV, save as `iwm_temp.csv`

### 5. EFA US Equity (iShares MSCI EAFE ETF - International Developed)
```
EFA US Equity <EQUITY> <GO>
BDH EFA US Equity PX_LAST 20180101 20241231 DAILY <GO>
```
Export to CSV, save as `efa_temp.csv`

### 6. BND US Equity (Vanguard Total Bond Market ETF)
```
BND US Equity <EQUITY> <GO>
BDH BND US Equity PX_LAST 20180101 20241231 DAILY <GO>
```
Export to CSV, save as `bnd_temp.csv`

### 7. QQQ US Equity (Invesco QQQ Trust - Nasdaq 100)
```
QQQ US Equity <EQUITY> <GO>
BDH QQQ US Equity PX_LAST 20180101 20241231 DAILY <GO>
```
Export to CSV, save as `qqq_temp.csv`

---

## After Export

Place all CSV files in: `/Users/quinference/GitHub/financial-data-science/data/bloomberg_database/`

Then run the update script:
```bash
cd /Users/quinference/GitHub/financial-data-science
python scripts/utilities/organize_bloomberg_database.py
```

This will merge them into the main `bloomberg_database.parquet` file.

---

## Alternative: Bulk Export (Faster)

```
XBDH <GO>
Tickers: TLT US Equity, GLD US Equity, VNQ US Equity, IWM US Equity, EFA US Equity, BND US Equity, QQQ US Equity
Fields: PX_LAST
Start: 01/01/2018
End: 12/31/2024
Frequency: DAILY
Export to Excel → Convert to CSV → Run organize script
```

---

## ETF Details (for reference)

| Ticker | Name | Asset Class | Why Needed |
|--------|------|-------------|------------|
| TLT | iShares 20+ Year Treasury | Long-term Bonds | Low correlation with equities |
| GLD | SPDR Gold Trust | Gold/Commodities | Inflation hedge |
| VNQ | Vanguard Real Estate | Real Estate | Alternative asset class |
| IWM | iShares Russell 2000 | Small Cap Equities | Size factor exposure |
| EFA | iShares MSCI EAFE | International Equities | Geographic diversification |
| BND | Vanguard Total Bond | Aggregate Bonds | Core bond exposure |
| QQQ | Invesco QQQ | Tech/Growth Equities | Growth factor exposure |

---

## Current Database Status

✅ **Already in database**: SPY, AAPL, GOOGL, MSFT, NVDA, BTCUSD, VIX, MOVE, USGG10YR  
❌ **Missing (needed for Ch 04)**: TLT, GLD, VNQ, IWM, EFA, BND, QQQ
