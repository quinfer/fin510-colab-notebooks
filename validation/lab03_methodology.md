# Lab 3 annual Treasury benchmark correction

The original notebook at `027c830b4041ca07e1b298377a32ab0666b272d2`
subtracts the end-of-year USGG3M yield from the preceding December-to-December
S&P 500 total return. The revised notebook compounds twelve monthly accrual
approximations, each using the preceding month-end annual quoted yield / 100 / 12.
The December Y annual outcome uses December Y-1 through November Y yields.
The complete annual outcome is then shifted to predictor December Y-1.

This makes timing consistent; it does not turn a generic three-month quoted
yield into an observed one-month investment return. Equal monthly accrual
periods and simple annual-rate/12 conversion are stated assumptions. Neither
Bloomberg yield conventions nor security prices, day counts, exact maturities
and cash flows are supplied in the extract. The proxy is not an actual
buy-and-hold or realised risk-free return. Reinvestment rates after the first
month are not known at the beginning of the year. Their use in the subsequent
outcome is distinct from putting future rates in a forecast's information set.

See the [US Treasury's bill-rate definitions](https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_bill_rates)
for discount versus investment-yield distinctions. No exact Bloomberg
convention is inferred from those definitions.

## Available data and timing

- Extract: `resources/price_dividend_ratio.parquet`, unchanged.
- USGG3M: 873 monthly observations, January 1954 to September 2026; no missing
  months or duplicate calendar months. Units are `yield_percent` (e.g. 1.5 = 1.5%).
- First complete December-to-December annual proxy: 1955; last: 2025.
- Missing months are explicitly reindexed and never filled. Twelve valid lagged
  yields are required. Annual price/dividend changes never bridge a missing December.
- Predictor cutoffs remain 2009 and 2024, inclusive. Outcomes end in 2010 and
  2025 respectively. No post-2024 predictors enter the second sample.
- The total-return and dividend-growth exercises and sector plots are retained.
- FIN510 analyses supplied historical data and uses simulation activities;
  live Bloomberg extraction remains a FIN306 activity. No Terminal dependency
  or extraction requirement is introduced.

## Regression comparison

`lab03_regression_comparison.csv` records sample size, predictor-year range,
intercept, slope, conventional OLS t statistic and R-squared for each benchmark.
Every old/corrected pair uses the exact intersection of predictor dates.
For the excess-return autoregression, both predictor and outcome are corrected.
The `ex_next on dp` specification is an explicitly labelled additional
sensitivity check; the original specifications are retained.

For predictors through 2024:

| Specification | N | Original slope | Corrected slope | Original R² | Corrected R² |
| --- | ---: | ---: | ---: | ---: | ---: |
| Next total return on D/P | 55 | 2.959833 | 2.959833 | 0.045499 | 0.045499 |
| Next dividend growth on D/P | 55 | -0.340979 | -0.340979 | 0.002587 | 0.002587 |
| Next approximate excess return on E/P | 35 | 4.192418 | 3.994099 | 0.121292 | 0.110871 |
| Next approximate excess return on lagged approximate excess return | 55 | -0.062121 | -0.054956 | 0.003869 | 0.003035 |
| Next approximate excess return on D/P (additional sensitivity) | 55 | 1.032724 | 0.920153 | 0.005464 | 0.004304 |

The total-return/D/P fit through 2009 is also unchanged: N=40, slope 4.253973,
R²=0.089233. Through 2009 the E/P excess-return fit changes from slope 4.562238,
R²=0.156637 to slope 4.344769, R²=0.139692 (N=20).
The correction modestly changes these sample fits, without establishing a
tradable forecasting rule or replicating Cochrane's CRSP regression.

## Source-of-truth check before propagation

Checked the current repository, tracked files, README, notebook metadata,
relevant commit history, all accessible `quinfer` repository names, and GitHub
code search for `lab03_price_dividend` and `price_dividend_ratio`. The only
matching course notebook and loader were in this Colab repository; no generator,
Quarto source, sync workflow or AGENTS.md is tracked here. No open issue or pull
request existed at inspection. Related accessible `bloomberg-edu` and
`quantitative-finance-foundations` READMEs do not identify an upstream source
for this lab. Saved-file searches did not locate a source copy.

Prior context names local `FIN510-website` and `financial-data-science` course
folders. Neither is available in this workspace or the accessible GitHub
repository inventory; `quinfer/financial-data-science` returns 404. This is
**not** evidence that no local authoritative source exists. Changes are
therefore supplied as a reviewable GitHub branch/PR, without modifying a guessed
course source or merging to the student-facing main branch. Before any future
regeneration, reconcile the corresponding Lab 3 source with this correction.

## Reproduce validation

```bash
python -m pip install -r requirements-validation.txt
python -m pytest -q tests/test_price_dividend.py
python scripts/validate_price_dividend.py
# Optional on a machine permitting Jupyter kernel sockets:
python scripts/validate_price_dividend.py --jupyter
```

The default runner validates notebook schema and executes every code cell in
order in fresh Python processes from repository root, `labs/`, and an isolated
directory with no course loader. The isolated run tests the HTTP fallback used
by a standalone Colab copy. Runtime versions and results are in
`lab03_execution.json`. Actual Google Colab service execution is not claimed.
This environment rejects Jupyter TCP and IPC sockets, so kernel execution could
not be validated here. Notebook outputs are cleared to avoid stale results.

Tests cover percent-to-decimal units, compounding, start/end yield shocks,
missing and duplicate months, missing Decembers, annual outcome shifts,
zero/negative yields, unsorted input and published-data regression controls.
