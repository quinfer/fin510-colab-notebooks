# Bloomberg Financial Database

## Overview

**Created**: 2025-11-26 16:30:39  
**Purpose**: Real-world demonstration of signal-to-noise in financial returns  
**Use Case**: Week 10 Factor Replication slides - Signal and Noise concepts

## Data Sources

### Core Equities (5 assets)
- AAPL, GOOGL, MSFT, NVDA, SPY
- Daily OHLCV data from Bloomberg Terminal
- Date range: 2018-01-02 to 2024-12-31

### Risk Gauges (3 indices)

These indices measure different dimensions of financial market risk and are used as benchmarks for understanding market uncertainty:

- **VIX Index**: CBOE Volatility Index, measuring 30-day expected volatility of the S&P 500. Often called the "fear gauge" as it spikes during market stress. Higher VIX indicates higher expected market volatility. Measures **equity market risk**.
  
  **How VIX Constructs "Expected" Volatility:**
  
  VIX is **not** calculated from historical price movements. Instead, it extracts the market's expectation of future volatility from **S&P 500 option prices** using a model-free methodology:
  
  1. **Data Source**: Uses prices of out-of-the-money (OTM) call and put options on the S&P 500 index
  2. **Time Horizon**: Options with approximately 23 and 37 days to expiration (interpolated to 30 days)
  3. **Model-Free Construction**: Uses a weighted average of option prices across different strike prices, avoiding assumptions about option pricing models (e.g., Black-Scholes)
  4. **Implied Volatility Extraction**: The option prices implicitly contain the market's expectation of volatility over the next 30 days—this is what VIX extracts
  
  **Why "Expected"?**
  
  - **Forward-looking**: VIX reflects what market participants expect volatility to be, not what it has been
  - **Market Consensus**: Option prices aggregate information from all market participants (traders, institutions, algorithms)
  - **Real-time**: Updates continuously as option prices change, reflecting changing market expectations
  - **Risk Premium Embedded**: Higher option prices (higher VIX) reflect both expected volatility and risk premiums demanded by option sellers
  
  **Mathematical Foundation**: VIX uses the variance swap replication approach—the weighted sum of OTM option prices equals the market's expectation of realized variance over the next 30 days. Taking the square root and annualizing gives the expected volatility (VIX).
  
  This makes VIX a **leading indicator** of market stress, as option prices react to news and uncertainty before actual volatility materializes in stock prices.

- **USGG10YR Index**: US Generic Government 10-Year Treasury Yield. Benchmark risk-free rate and key indicator of long-term interest rate expectations. Changes reflect inflation expectations and monetary policy. Measures **interest rate risk** and serves as the risk-free rate benchmark.

- **MOVE Index**: ICE BofA MOVE Index (Merrill Lynch Option Volatility Estimate), measuring expected volatility in US Treasury bond markets. The bond market equivalent of VIX, tracking uncertainty in interest rates. Measures **bond market volatility risk**.

**Why "Risk Gauges"?** These indices quantify different types of financial risk (equity volatility, interest rates, bond volatility) and are widely used by practitioners to assess market conditions and risk levels.

- Date range: 2018-01-01 to 2025-01-01

### Crypto (1 asset)
- BTCUSD (Bitcoin)
- Daily price data
- Date range: 2018-01-01 onwards

## Files

- `bloomberg_database.parquet` - Full database (Parquet format, efficient)
- `bloomberg_database.csv` - Full database (CSV format, readable)
- `signal_noise_metrics.csv` - Calculated signal-to-noise metrics
- `summary_statistics.csv` - Summary statistics by asset
- `signal_noise_analysis.png` - Visualization of signal vs noise
- `equity.csv`, `risk_gauge.csv`, `crypto.csv` - Data by asset type

## Signal-to-Noise Metrics

The database includes calculated metrics:

- **Signal-to-Noise Ratio**: |Mean Return| / Std Dev
- **Signal Fraction**: Proportion of variance explained by mean (signal)
- **Noise Fraction**: Proportion of variance unexplained (noise)
- **Sharpe Ratio**: Annualized risk-adjusted return

## Usage in Week 10 Slides

This database demonstrates:

1. **Low signal-to-noise in financial returns**: Most variance is noise, not signal
2. **Differences across asset classes**: Equities vs risk gauges vs crypto
3. **Time-varying noise**: Volatility clustering (GARCH effects)
4. **Why standard errors matter**: Large noise makes signal detection difficult

## Example Analysis

```python
import pandas as pd

# Load database
df = pd.read_parquet('data/bloomberg_database/bloomberg_database.parquet')

# Calculate signal-to-noise for SPY
spy = df[df['ticker'] == 'SPY']['return'].dropna()
signal_noise_ratio = abs(spy.mean()) / spy.std()
print(f"SPY Signal-to-Noise: {signal_noise_ratio:.4f}")

# Signal fraction
total_var = spy.var()
signal_var = spy.mean() ** 2
signal_frac = signal_var / total_var
print(f"Signal fraction: {signal_frac:.1%}")
print(f"Noise fraction: {1 - signal_frac:.1%}")
```

## Data Quality

- **Source**: Bloomberg Terminal (professional-grade data)
- **Adjustments**: Price data adjusted for splits/dividends
- **Missing values**: Handled appropriately (forward fill where needed)
- **Validation**: All returns calculated consistently

## Notes

- Daily returns calculated as: (Price_t / Price_t-1) - 1
- Log returns also included for statistical analysis
- All metrics annualized where appropriate (252 trading days)
