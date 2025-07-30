import pytest
import pandas as pd
from definition_41c57fe42e324fab8e5ea7e13f854ba5 import generate_synthetic_data

def test_generate_synthetic_data_positive():
    df = generate_synthetic_data(10)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 10
    assert 'Scenario ID' in df.columns
    assert 'Risk Category' in df.columns
    assert 'Initial Likelihood' in df.columns
    assert 'Initial Impact (Financial)' in df.columns
    assert 'Initial Impact (Reputational)' in df.columns
    assert 'Initial Impact (Operational)' in df.columns

def test_generate_synthetic_data_zero():
    df = generate_synthetic_data(0)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0

def test_generate_synthetic_data_seed():
    df1 = generate_synthetic_data(5, seed=42)
    df2 = generate_synthetic_data(5, seed=42)
    pd.testing.assert_frame_equal(df1, df2)

def test_generate_synthetic_data_likelihood_range():
    df = generate_synthetic_data(100)
    assert df['Initial Likelihood'].min() >= 0
    assert df['Initial Likelihood'].max() <= 1

def test_generate_synthetic_data_type_error():
    with pytest.raises(TypeError):
        generate_synthetic_data("abc")
