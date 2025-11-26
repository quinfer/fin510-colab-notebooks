# Chapter 04 Data Cache: Robo-Advisor Portfolio Optimization

## Overview

**Generated**: 2025-10-07 15:32:25  
**Period**: 2022-01-01 to 2024-10-01 (~2 years)  
**Purpose**: Portfolio optimization for robo-advisor demonstrations

## Asset Universe (5 Liquid ETFs)

Diversified portfolio spanning major asset classes:

- **SPY**: SPDR S&P 500 ETF (US Large Cap)
- **IWM**: iShares Russell 2000 (US Small Cap)
- **EFA**: iShares MSCI EAFE (International Developed)
- **BND**: Vanguard Total Bond Market (Bonds)
- **VNQ**: Vanguard Real Estate ETF (REITs)

## Use Cases in Chapter 04

1. **Modern Portfolio Theory**: Mean-variance optimization
2. **Risk Profiling**: Conservative/Moderate/Aggressive allocations
3. **ML-Enhanced Allocation**: Return prediction models
4. **Performance Validation**: Backtesting & Sharpe ratios

## Data Characteristics

- **Equity ETFs** (SPY, IWM, EFA): Higher returns, higher volatility
- **Bond ETF** (BND): Lower risk, provides diversification
- **Real Estate** (VNQ): Moderate risk, alternative asset class
- **Correlations**: Realistic diversification benefits

## Files

- `spy_data.csv`: SPY (2022-01-03 to 2024-10-01)
- `iwm_data.csv`: IWM (2022-01-03 to 2024-10-01)
- `efa_data.csv`: EFA (2022-01-03 to 2024-10-01)
- `bnd_data.csv`: BND (2022-01-03 to 2024-10-01)
- `vnq_data.csv`: VNQ (2022-01-03 to 2024-10-01)

## Purpose

This cached data enables:

1. **Fast rendering** - No API calls during chapter rendering
2. **Reproducible results** - Identical optimization outcomes for all students
3. **Offline work** - No Bloomberg Terminal or internet required
4. **Temporal correctness** - Data snapshot represents specific time period

## Regeneration

To fetch fresh data:

```bash
# On Bloomberg Terminal (professional data)
python scripts/fetch_chapter04_data.py

# Script auto-detects Bloomberg and falls back to synthetic data
```

## Bloomberg Usage

This script uses **conservative rate limiting**:
- Fetches 1 ETF at a time
- 2-second delays between requests
- Total time: ~10 seconds for 5 ETFs
- Very safe for university Bloomberg licenses

## Portfolio Optimization Notes

The 5-asset universe provides:
- Sufficient diversification for educational purposes
- Realistic correlation structure for demonstrating benefits
- Liquid instruments that students can relate to
- Representative of actual robo-advisor portfolios
