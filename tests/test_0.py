import pytest
import pandas as pd
from definition_471f490445434665a6cd239e51840c15 import generate_synthetic_data

def test_generate_synthetic_data_positive_scenarios():
    df = generate_synthetic_data(10)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 10
    assert 'Scenario ID' in df.columns
    assert 'Risk Category' in df.columns
    assert 'Initial Likelihood' in df.columns
    assert 'Initial Impact (Financial)' in df.columns
    assert 'Initial Impact (Reputational)' in df.columns
    assert 'Initial Impact (Operational)' in df.columns

def test_generate_synthetic_data_zero_scenarios():
    df = generate_synthetic_data(0)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0
    assert 'Scenario ID' in df.columns
    assert 'Risk Category' in df.columns
    assert 'Initial Likelihood' in df.columns
    assert 'Initial Impact (Financial)' in df.columns
    assert 'Initial Impact (Reputational)' in df.columns
    assert 'Initial Impact (Operational)' in df.columns

def test_generate_synthetic_data_seed_reproducibility():
    df1 = generate_synthetic_data(5, seed=42)
    df2 = generate_synthetic_data(5, seed=42)
    pd.testing.assert_frame_equal(df1, df2)

def test_generate_synthetic_data_different_seed():
    df1 = generate_synthetic_data(5, seed=42)
    df2 = generate_synthetic_data(5, seed=123)
    with pytest.raises(AssertionError):
        pd.testing.assert_frame_equal(df1, df2)

def test_generate_synthetic_data_column_types():
    df = generate_synthetic_data(5)
    assert df['Initial Likelihood'].dtype == 'float64'
    assert df['Initial Impact (Financial)'].dtype == 'float64'
    assert df['Initial Impact (Reputational)'].dtype == 'float64'
    assert df['Initial Impact (Operational)'].dtype == 'float64'
