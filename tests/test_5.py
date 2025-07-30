import pytest
import pandas as pd
from definition_a78dde759189481aa580a4b3971b1d7c import aggregate_results

@pytest.fixture
def mock_simulation_log():
    data = {'Risk Category': ['A', 'A', 'B', 'B', 'A'],
            'Chosen Action': ['Accept', 'Mitigate', 'Transfer', 'Accept', 'Mitigate'],
            'Residual Financial Impact': [100, 50, 200, 75, 25]}
    return pd.DataFrame(data)

def test_aggregate_results_empty_log():
    empty_df = pd.DataFrame()
    result = aggregate_results(empty_df)
    assert isinstance(result, pd.DataFrame)
    assert result.empty

def test_aggregate_results_basic_aggregation(mock_simulation_log):
    result = aggregate_results(mock_simulation_log)
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert 'Residual Financial Impact' in result.columns

def test_aggregate_results_groupby_risk_category_and_action(mock_simulation_log):
    result = aggregate_results(mock_simulation_log)
    expected_groups = {('A', 'Accept'), ('A', 'Mitigate'), ('B', 'Transfer'), ('B', 'Accept')}

    actual_groups = set(zip(result['Risk Category'], result['Chosen Action']))
    assert actual_groups == expected_groups

def test_aggregate_results_different_data_types():
    data = {'Risk Category': ['A', 'A'],
            'Chosen Action': ['Accept', 'Mitigate'],
            'Residual Financial Impact': ['100', 50]}  # '100' is a string
    df = pd.DataFrame(data)
    with pytest.raises(TypeError):
        aggregate_results(df)
        
def test_aggregate_results_no_residual_financial_impact():
    data = {'Risk Category': ['A', 'B'], 'Chosen Action': ['Accept', 'Mitigate']}
    df = pd.DataFrame(data)
    with pytest.raises(KeyError):
        aggregate_results(df)
