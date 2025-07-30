import pytest
import pandas as pd
from definition_f6925eaed3ea42ddb7d57f4e6f7dd3ad import calculate_cumulative_impact

@pytest.fixture
def sample_simulation_log():
    data = {'Residual Impact of Scenario': [100, 200, 150, 50, 300]}
    return pd.DataFrame(data)

def test_calculate_cumulative_impact_empty_log():
    empty_log = pd.DataFrame()
    result = calculate_cumulative_impact(empty_log)
    assert isinstance(result, pd.DataFrame)
    assert result.empty

def test_calculate_cumulative_impact_single_scenario(sample_simulation_log):
    single_scenario_log = sample_simulation_log.iloc[[0]]
    result = calculate_cumulative_impact(single_scenario_log)
    assert isinstance(result, pd.DataFrame)
    assert not result.empty

def test_calculate_cumulative_impact_typical_log(sample_simulation_log):
    result = calculate_cumulative_impact(sample_simulation_log)
    assert isinstance(result, pd.DataFrame)
    assert not result.empty

def test_calculate_cumulative_impact_negative_impact(sample_simulation_log):
    sample_simulation_log['Residual Impact of Scenario'][0] = -50
    result = calculate_cumulative_impact(sample_simulation_log)
    assert isinstance(result, pd.DataFrame)
    assert not result.empty

def test_calculate_cumulative_impact_non_dataframe_input():
    with pytest.raises(AttributeError):
        calculate_cumulative_impact([1, 2, 3])

