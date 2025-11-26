# Chapter 02 Data Cache

## Overview

This directory contains cached data for Chapter 02: Financial Data APIs.

**Generated**: 2025-10-07 13:08:24

## Files

- `aapl_data.csv`: AAPL (2023-01-02 to 2024-10-01, 457 rows)
- `googl_data.csv`: GOOGL (2023-01-02 to 2024-10-01, 457 rows)
- `msft_data.csv`: MSFT (2023-01-02 to 2024-10-01, 457 rows)
- `jpm_data.csv`: JPM (2023-01-02 to 2024-10-01, 457 rows)
- `pypl_data.csv`: PYPL (2023-01-02 to 2024-10-01, 457 rows)

## Purpose

This data is cached to:

1. **Avoid API rate limits** during chapter rendering
2. **Ensure reproducibility** across renders and student machines
3. **Demonstrate production practice** of separating acquisition from analysis
4. **Enable offline work** without Bloomberg Terminal access

## Regeneration

To regenerate this data:

```bash
# On Bloomberg Terminal
python scripts/fetch_chapter02_data.py

# Without Bloomberg (synthetic)
python scripts/fetch_chapter02_data.py
```

The script automatically detects Bloomberg availability and falls back to synthetic data.

## Data Quality

- **Real data** (from Bloomberg): Professional-grade, adjusted for splits/dividends
- **Synthetic data**: Production-quality simulation with fat tails, volatility clustering, and realistic OHLC relationships

Both are suitable for teaching core concepts in Chapter 02.
