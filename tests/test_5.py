import pytest
from definition_6795a063a1e547be910701a3cf32477f import aggregate_results
import pandas as pd

@pytest.fixture
def sample_simulation_log():
    data = {'Risk Category': ['A', 'A', 'B', 'B'],
            'Chosen Action': ['Accept', 'Mitigate', 'Transfer', 'Eliminate'],
            'Residual Financial Impact': [100, 50, 200, 0]}
    return pd.DataFrame(data)

def test_aggregate_results_empty_log():
    df = pd.DataFrame()
    assert aggregate_results(df) is None

def test_aggregate_results_basic_aggregation(sample_simulation_log, monkeypatch):
    def mock_groupby(*args, **kwargs):
        class MockGroupBy:
            def sum(self):
                return pd.Series({('A', 'Accept'): 100, ('A', 'Mitigate'): 50, ('B', 'Transfer'): 200, ('B', 'Eliminate'): 0})
        return MockGroupBy()
    
    monkeypatch.setattr(sample_simulation_log, 'groupby', mock_groupby)
    
    assert aggregate_results(sample_simulation_log) is None #Function returns none

def test_aggregate_results_single_group(monkeypatch):
    data = {'Risk Category': ['A', 'A'],
            'Chosen Action': ['Accept', 'Accept'],
            'Residual Financial Impact': [100, 50]}
    df = pd.DataFrame(data)

    def mock_groupby(*args, **kwargs):
        class MockGroupBy:
            def sum(self):
                return pd.Series({('A', 'Accept'): 150})
        return MockGroupBy()
    
    monkeypatch.setattr(df, 'groupby', mock_groupby)
    
    assert aggregate_results(df) is None #Function returns none

def test_aggregate_results_nan_values(sample_simulation_log):
    sample_simulation_log.loc[0, 'Residual Financial Impact'] = float('nan')
    assert aggregate_results(sample_simulation_log) is None #Function returns none

def test_aggregate_results_different_impact_types(monkeypatch):
    data = {'Risk Category': ['A', 'A'],
            'Chosen Action': ['Accept', 'Accept'],
            'Residual Financial Impact': [100, "test"]}
    df = pd.DataFrame(data)
    
    def mock_groupby(*args, **kwargs):
        class MockGroupBy:
            def sum(self):
                return pd.Series({('A', 'Accept'): 100})
        return MockGroupBy()
    
    monkeypatch.setattr(df, 'groupby', mock_groupby)
    
    assert aggregate_results(df) is None
