"""Timing and units checks against the notebook's actual calculation functions."""
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[1]

@pytest.fixture(scope='module')
def functions():
    # Load definitions, without running plots, network access or the exercise.
    import ast
    nb = json.loads((ROOT / 'labs/lab03_price_dividend.ipynb').read_text())
    ns = {'pd': pd, 'sm': sm}
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            tree = ast.parse(''.join(cell['source']))
            defs = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
            exec(compile(ast.Module(body=defs, type_ignores=[]), '<notebook>', 'exec'), ns)
    return ns

@pytest.fixture
def monthly():
    index = pd.period_range('1999-12', '2002-12', freq='M')
    return pd.DataFrame({'dy': 2., 'tr': 100. * 1.01 ** np.arange(len(index)),
                         'pe': 20., 'bill': 12., 'P': 100.}, index=index)

def test_constant_percent_yield_compounds_twelve_months(functions, monthly):
    dec = functions['annual_panel'](monthly)
    assert dec.loc['2000-12-31', 'rf_approx'] == pytest.approx(1.01**12 - 1)
    assert dec.loc['2000-12-31', 'R'] == pytest.approx(1.01**12 - 1)
    assert dec.loc['2000-12-31', 'ex'] == pytest.approx(0)
    assert dec.loc['2000-12-31', 'dp'] == .02
    assert dec.loc['2000-12-31', 'ep'] == .05
    assert np.isnan(dec.iloc[0]['R'])
    assert np.isnan(dec.iloc[0]['rf_approx'])

def test_rate_boundary_shocks(functions, monthly):
    base = functions['annual_panel'](monthly)
    # End-December shock must not affect that year's annual benchmark.
    monthly.loc['2000-12', 'bill'] = 24.
    shock = functions['annual_panel'](monthly)
    assert shock.loc['2000-12-31', 'rf_approx'] == base.loc['2000-12-31', 'rf_approx']
    assert shock.loc['2001-12-31', 'rf_approx'] == pytest.approx(1.02 * 1.01**11 - 1)
    # Starting December DOES enter the immediately following annual interval.
    monthly.loc['1999-12', 'bill'] = 0.
    shock = functions['annual_panel'](monthly)
    assert shock.loc['2000-12-31', 'rf_approx'] == pytest.approx(1.01**11 - 1)

@pytest.mark.parametrize('mode', ['absent', 'nan'])
def test_missing_month_invalidates_whole_annual_proxy(functions, monthly, mode):
    if mode == 'absent':
        monthly = monthly.drop(pd.Period('2000-06', 'M'))
    else:
        monthly.loc['2000-06', 'bill'] = np.nan
    dec = functions['annual_panel'](monthly)
    assert np.isnan(dec.loc['2000-12-31', 'rf_approx'])
    assert np.isnan(dec.loc['1999-12-31', 'ex_next'])
    assert pd.notna(dec.loc['2001-12-31', 'rf_approx'])
    assert pd.notna(dec.loc['2000-12-31', 'R'])

def test_missing_december_never_bridges_two_years(functions, monthly):
    dec = functions['annual_panel'](monthly.drop(pd.Period('2000-12', 'M')))
    assert np.isnan(dec.loc['2000-12-31', 'R'])
    assert np.isnan(dec.loc['2001-12-31', 'R'])
    assert np.isnan(dec.loc['1999-12-31', 'R_next'])

def test_next_outcomes_use_following_calendar_year(functions, monthly):
    dec = functions['annual_panel'](monthly)
    for name in ('R', 'ex', 'dg'):
        pd.testing.assert_series_equal(dec[name + '_next'], dec[name].shift(-1), check_names=False)
        assert np.isnan(dec.iloc[-1][name + '_next'])

def test_duplicate_month_rejected(functions, monthly):
    with pytest.raises(ValueError, match='one observation'):
        functions['annual_panel'](pd.concat([monthly, monthly.iloc[:1]]))

def test_zero_and_negative_yields(functions, monthly):
    for rate in (0., -1.):
        monthly['bill'] = rate
        dec = functions['annual_panel'](monthly)
        assert dec.loc['2000-12-31', 'rf_approx'] == pytest.approx((1 + rate / 1200)**12 - 1)

def test_unsorted_months(functions, monthly):
    pd.testing.assert_frame_equal(functions['annual_panel'](monthly),
                                  functions['annual_panel'](monthly.iloc[::-1]))

def test_published_extract_and_comparison(functions):
    raw = pd.read_parquet(ROOT / 'resources/price_dividend_ratio.parquet')
    raw = raw[raw.frequency.eq('monthly')]
    mappings = {'dy': ('SPX', 'EQY_DVD_YLD_12M'), 'tr': ('SPX', 'TOT_RETURN_INDEX_GROSS_DVDS'),
                'pe': ('SPX', 'PE_RATIO'), 'bill': ('USGG3M', 'PX_LAST'), 'P': ('SPX', 'PX_LAST')}
    series = {}
    for name, (ticker, field) in mappings.items():
        s = raw[raw.ticker.eq(ticker) & raw.field.eq(field)].set_index('date').value
        s.index = s.index.to_period('M')
        assert not s.index.has_duplicates
        series[name] = s
    dec = functions['annual_panel'](pd.DataFrame(series))
    assert dec.rf_approx.first_valid_index() == pd.Timestamp('1955-12-31')
    comparison = functions['compare_benchmarks'](dec)
    for cutoff, slope, r2, n in ((2009, 4.25, .089, 40), (2024, 2.96, .045, 55)):
        row = comparison[(comparison.predictor_end == cutoff) & (comparison.regression == 'R_next on dp')].iloc[0]
        assert row.n == n
        assert row.b_corrected == pytest.approx(slope, abs=.005)
        assert row.R2_corrected == pytest.approx(r2, abs=.0005)
    controls = comparison[comparison.regression.isin(['R_next on dp', 'dg_next on dp'])]
    np.testing.assert_allclose(controls.b_corrected, controls.b_old, rtol=0, atol=0)
    np.testing.assert_allclose(controls.R2_corrected, controls.R2_old, rtol=0, atol=0)
    # Every old/new pair shares exactly the same predictor dates; no sample loss here.
    assert comparison.n.tolist() == [40, 40, 40, 20, 40, 55, 55, 55, 35, 55]

def test_monthly_alignment_handles_different_business_dates(functions):
    raw = pd.DataFrame({'ticker': ['SPX', 'USGG3M'], 'field': ['PX_LAST', 'PX_LAST'],
                        'date': pd.to_datetime(['2000-12-29', '2000-12-31']),
                        'value': [100., 12.]})
    price = functions['monthly_field'](raw, 'SPX', 'PX_LAST')
    rate = functions['monthly_field'](raw, 'USGG3M', 'PX_LAST')
    combined = pd.concat({'P': price, 'bill': rate}, axis=1)
    assert len(combined) == 1
    assert combined.iloc[0].tolist() == [100., 12.]


def test_multiple_quotes_in_one_month_rejected(functions):
    raw = pd.DataFrame({'ticker': ['USGG3M'] * 2, 'field': ['PX_LAST'] * 2,
                        'date': pd.to_datetime(['2000-12-29', '2000-12-31']),
                        'value': [12., 12.]})
    with pytest.raises(ValueError, match='Multiple observations'):
        functions['monthly_field'](raw, 'USGG3M', 'PX_LAST')
