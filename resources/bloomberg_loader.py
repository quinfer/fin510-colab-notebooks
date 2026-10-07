"""
Shared Bloomberg data loader.

Resolves the long-standing problem of two disjoint parquet files
(Dropbox UK exports vs repo US/global data) by reading from BOTH
and returning a single merged DataFrame.

Usage in any QMD file (execute-dir: project):

    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path("scripts").resolve()))
    from bloomberg_loader import load_bloomberg

    df = load_bloomberg()                  # all tickers
    spy = load_bloomberg(tickers=["SPY"])   # filtered
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Sequence

import pandas as pd
import yaml

logger = logging.getLogger(__name__)

_CONFIG_PATH = Path("config/data_root.yml")
_REPO_PARQUET = Path("data/bloomberg_database/bloomberg_database.parquet")


def _resolve_data_root() -> Path:
    """Read data_root from config/data_root.yml; fall back to repo data/."""
    try:
        with open(_CONFIG_PATH) as fh:
            cfg = yaml.safe_load(fh)
        return Path(cfg.get("data_root", "data")).expanduser().resolve()
    except Exception:
        return Path("data").resolve()


def load_bloomberg(
    tickers: Sequence[str] | None = None,
    *,
    columns: Sequence[str] | None = None,
) -> pd.DataFrame:
    """Load Bloomberg data from all available parquet sources.

    Reads from:
      1. The Dropbox/OneDrive parquet pointed to by config/data_root.yml
      2. The repo-local parquet at data/bloomberg_database/

    Concatenates both (deduplicating on ticker+date), so callers
    always see the full ticker universe regardless of which
    parquet contains the ticker they need.

    Parameters
    ----------
    tickers : list of str, optional
        Filter to these tickers (case-insensitive). None returns all.
    columns : list of str, optional
        Columns to read from parquet. None reads all.
    """
    frames: list[pd.DataFrame] = []

    data_root = _resolve_data_root()
    primary = data_root / "bloomberg_database" / "bloomberg_database.parquet"
    repo = _REPO_PARQUET.resolve()
    # fin510-colab-notebooks layout: resources/bloomberg_database.parquet (cwd repo root or labs/)
    colab_resources = Path("resources/bloomberg_database.parquet").resolve()
    colab_resources_up = Path("../resources/bloomberg_database.parquet").resolve()

    sources: list[tuple[str, Path]] = [
        ("primary (data_root)", primary),
        ("repo (data/bloomberg_database)", repo),
        ("colab resources", colab_resources),
        ("colab ../resources", colab_resources_up),
    ]

    for label, path in sources:
        if not path.exists():
            logger.debug("Bloomberg parquet not found at %s [%s]", path, label)
            continue
        try:
            df = pd.read_parquet(path, columns=columns)
            logger.debug(
                "Loaded %d rows from %s [%s]", len(df), path, label
            )
            frames.append(df)
        except Exception as exc:
            logger.warning("Failed to read %s [%s]: %s", path, label, exc)

    if not frames:
        checked = "\n".join(f"  {lbl}: {p}" for lbl, p in sources)
        raise FileNotFoundError(
            "No Bloomberg parquet found. Checked:\n" + checked
        )

    merged = pd.concat(frames, ignore_index=True)

    # Deduplicate: prefer primary (data_root) rows when both have same
    # ticker+date combination.  Primary is first in `frames`, so
    # keep='first' after concat preserves it.
    dedup_cols = []
    if "ticker" in merged.columns:
        dedup_cols.append("ticker")
    if "date" in merged.columns:
        dedup_cols.append("date")
    if dedup_cols:
        merged = merged.drop_duplicates(subset=dedup_cols, keep="first")

    if tickers is not None:
        upper = {t.strip().upper() for t in tickers}
        if "ticker" in merged.columns:
            merged = merged[
                merged["ticker"].astype(str).str.strip().str.upper().isin(upper)
            ]

    return merged


_PRICE_DIVIDEND_NAME = "price_dividend_ratio.parquet"
_PRICE_DIVIDEND_URL = (
    "https://raw.githubusercontent.com/quinfer/fin510-colab-notebooks/"
    "main/resources/price_dividend_ratio.parquet"
)


def load_price_dividend(
    tickers: Sequence[str] | None = None,
    *,
    fields: Sequence[str] | None = None,
    frequency: str | None = None,
) -> pd.DataFrame:
    """Load the S&P 500 price-dividend extract.

    This is not part of load_bloomberg(). The main parquet has one PX_LAST
    per ticker and date, and callers turn that column into a return. Dividend
    yields and Treasury yields in this extract are levels, not prices.

    Columns: date, ticker, security, field, value, value_type, frequency.
    value_type is price, total_return, dividend_yield_percent, pe_ratio,
    price_to_book, or yield_percent. Dividend yields and Treasury yields
    are in percent (1.5 means 1.5%).

    Looks for data/bloomberg_database/price_dividend_ratio.parquet, then
    resources/ beside a Colab notebook. If neither file is present, reads
    the copy published to fin510-colab-notebooks.
    """
    candidates = [
        Path("data/bloomberg_database") / _PRICE_DIVIDEND_NAME,
        Path("resources") / _PRICE_DIVIDEND_NAME,
        Path("../resources") / _PRICE_DIVIDEND_NAME,
    ]
    frame = None
    for path in candidates:
        if path.exists():
            frame = pd.read_parquet(path)
            break
    if frame is None:
        frame = pd.read_parquet(_PRICE_DIVIDEND_URL)

    if tickers is not None:
        upper = {t.strip().upper() for t in tickers}
        frame = frame[frame["ticker"].astype(str).str.upper().isin(upper)]
    if fields is not None:
        wanted = {f.strip() for f in fields}
        frame = frame[frame["field"].isin(wanted)]
    if frequency is not None:
        frame = frame[frame["frequency"].eq(frequency)]
    return frame.reset_index(drop=True)
