# Chapter 01 Data Cache: FinTech vs Traditional Banks

## Overview

**Generated**: 2025-10-07 15:22:43  
**Period**: 2021-01-01 to 2024-10-01 (~3 years)  
**Purpose**: Compare performance between traditional banks and FinTech companies

## Data Groups

### Traditional Banks (4 companies)
- JPM: JPMorgan Chase
- BAC: Bank of America
- WFC: Wells Fargo
- C: Citigroup

### FinTech Companies (4 companies)
- PYPL: PayPal Holdings
- SQ: Block (Square)
- SOFI: SoFi Technologies
- AFRM: Affirm Holdings

## Files

- `jpm_data.csv`: JPMorgan Chase (Traditional Bank)
- `bac_data.csv`: Bank of America (Traditional Bank)
- `wfc_data.csv`: Wells Fargo (Traditional Bank)
- `c_data.csv`: Citigroup (Traditional Bank)
- `pypl_data.csv`: PayPal Holdings (FinTech)
- `sq_data.csv`: Block (Square) (FinTech)
- `sofi_data.csv`: SoFi Technologies (FinTech)
- `afrm_data.csv`: Affirm Holdings (FinTech)

## Purpose

This cached data enables:

1. **Reproducible analysis** across all student machines
2. **No rate limits** during chapter rendering
3. **Offline work** without Bloomberg Terminal
4. **Consistent results** for teaching demonstrations

## Data Characteristics

- **Traditional Banks**: Lower volatility (~24% annual), stable returns
- **FinTech**: Higher volatility (~44% annual), growth-oriented

## Regeneration

To fetch fresh data:

```bash
# On Bloomberg Terminal (professional data)
python scripts/fetch_chapter01_data.py

# Script auto-detects Bloomberg and falls back to synthetic data
```

## Bloomberg Usage

This script uses **conservative rate limiting**:
- Fetches 1 symbol at a time
- 2-second delays between requests
- Total time: ~16 seconds for 8 symbols
- Very safe for university Bloomberg licenses
