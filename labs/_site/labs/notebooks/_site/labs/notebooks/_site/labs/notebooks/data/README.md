# Data Configs

This folder contains configuration files for local/offline data usage. The Bloomberg Desktop API config is designed for one‑off pulls on a Terminal PC.

`bbg_config.yml`
- meta
  - `output_root`: where CSVs are written (e.g., `outputs/bbg`)
  - Throttles/batching: `requests_per_minute`, `sleep_between_batches_sec`, `max_tickers_per_request`, `max_fields_per_request`
- historical.groups
  - Define small universes (tickers) and a few fields (e.g., `PX_LAST`, `PX_VOLUME`)
  - Common sets: equities_core, benchmarks, rates, fx, etfs
  - Dates/periodicity set at the top of `historical`
- reference.groups
  - One‑shot descriptors (e.g., `NAME`, `CRNCY`, `GICS_SECTOR_NAME`)

Edit safely
- Add/remove tickers; keep lists short for license and stability
- Adjust date range and periodicity as needed
- Verify every field mnemonic with FLDS <GO> on the Terminal

Run
- See `scripts/README.md` for CLI usage and environment requirements
