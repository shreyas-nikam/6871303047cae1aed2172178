import pandas as pd
import numpy as np

def generate_synthetic_data(num_scenarios, seed=None):
    """Generates synthetic risk scenario data."""
    if not isinstance(num_scenarios, int):
        raise TypeError("num_scenarios must be an integer")

    if seed is not None:
        np.random.seed(seed)

    data = {
        'Scenario ID': range(1, num_scenarios + 1),
        'Risk Category': np.random.choice(['Financial', 'Reputational', 'Operational', 'Compliance', 'Strategic'], num_scenarios),
        'Initial Likelihood': np.random.beta(a=2, b=5, size=num_scenarios),  # Beta distribution for likelihood (skewed towards lower values)
        'Initial Impact (Financial)': np.random.lognormal(mean=5, sigma=2, size=num_scenarios),  # Lognormal for financial impact
        'Initial Impact (Reputational)': np.random.randint(1, 6, size=num_scenarios),  # Scale of 1-5
        'Initial Impact (Operational)': np.random.randint(1, 6, size=num_scenarios)   # Scale of 1-5
    }

    df = pd.DataFrame(data)
    return df

def set_risk_appetite(max_financial_loss, max_incidents, max_reputational_impact):
                """Stores the user-defined risk appetite thresholds."""

                global RISK_APPETITE
                RISK_APPETITE = {
                    "max_financial_loss": max_financial_loss,
                    "max_incidents": max_incidents,
                    "max_reputational_impact": max_reputational_impact,
                }

import pandas as pd

def simulate_scenario_outcome(scenario_data, action, action_params, risk_appetite_thresholds):
    """Simulates scenario outcome based on action and risk appetite."""

    initial_likelihood = scenario_data['Initial Likelihood']
    initial_financial_impact = scenario_data['Initial Impact (Financial)']
    initial_reputational_impact = scenario_data['Initial Impact (Reputational)']
    initial_operational_impact = scenario_data['Initial Impact (Operational)']

    residual_likelihood = initial_likelihood
    residual_financial_impact = initial_financial_impact
    residual_reputational_impact = initial_reputational_impact
    residual_operational_impact = initial_operational_impact

    if action == 'Accept':
        pass  # No change

    elif action == 'Mitigate':
        impact_reduction = action_params.get('Mitigation Factor (Impact Reduction %)', 0)
        likelihood_reduction = action_params.get('Mitigation Factor (Likelihood Reduction %)', 0)
        residual_likelihood = initial_likelihood * (1 - likelihood_reduction)
        residual_financial_impact = initial_financial_impact * (1 - impact_reduction)
        residual_reputational_impact = initial_reputational_impact * (1 - impact_reduction)
        residual_operational_impact = initial_operational_impact * (1 - impact_reduction)

    elif action == 'Transfer':
        deductible = action_params.get('Insurance Deductible ($)', 0)
        coverage_ratio = action_params.get('Insurance Coverage Ratio (%)', 0)
        residual_financial_impact = deductible + (initial_financial_impact - deductible) * (1 - coverage_ratio)


    elif action == 'Eliminate':
        residual_likelihood = 0
        residual_financial_impact = 0
        residual_reputational_impact = 0
        residual_operational_impact = 0


    else:
        raise Exception("Invalid action")

    max_acceptable_financial_loss = risk_appetite_thresholds['Max Acceptable Financial Loss per Incident']
    max_acceptable_incidents = risk_appetite_thresholds['Max Acceptable Incidents per Period']
    max_acceptable_reputational_impact = risk_appetite_thresholds['Max Acceptable Reputational Impact Score']

    financial_compliant = residual_financial_impact <= max_acceptable_financial_loss
    operational_compliant = initial_likelihood <= max_acceptable_incidents  # Assuming likelihood represents incident frequency
    reputational_compliant = residual_reputational_impact <= max_acceptable_reputational_impact

    result = {
        'Initial Likelihood': initial_likelihood,
        'Initial Financial Impact': initial_financial_impact,
        'Initial Reputational Impact': initial_reputational_impact,
        'Initial Operational Impact': initial_operational_impact,
        'Residual Likelihood': residual_likelihood,
        'Residual Financial Impact': residual_financial_impact,
        'Residual Reputational Impact': residual_reputational_impact,
        'Residual Operational Impact': residual_operational_impact,
        'Financial Compliant': financial_compliant,
        'Operational Compliant': operational_compliant,
        'Reputational Compliant': reputational_compliant
    }

    return result

import pandas as pd

SIMULATION_LOG = pd.DataFrame()

def update_simulation_log(scenario_outcome):
    """Appends scenario outcome to the global SIMULATION_LOG DataFrame."""
    global SIMULATION_LOG

    if not isinstance(scenario_outcome, dict):
        raise TypeError("scenario_outcome must be a dictionary")

    if 'scenario_id' not in scenario_outcome or 'residual_impact' not in scenario_outcome:
        raise KeyError("scenario_outcome must contain 'scenario_id' and 'residual_impact'")
    
    if not isinstance(scenario_outcome['scenario_id'], str):
        raise TypeError("scenario_id must be a string")

    if not isinstance(scenario_outcome['residual_impact'], (int, float)):
        raise TypeError("residual_impact must be a number")

    # Append the scenario outcome to the log
    SIMULATION_LOG = pd.concat([SIMULATION_LOG, pd.DataFrame([scenario_outcome])], ignore_index=True)

import pandas as pd

def calculate_cumulative_impact(simulation_log):
    """Processes the `simulation_log` to calculate cumulative financial impact.
    """
    if not isinstance(simulation_log, pd.DataFrame):
        raise AttributeError("simulation_log must be a pandas DataFrame.")

    if simulation_log.empty:
        return pd.DataFrame()

    cumulative_impact = simulation_log['Residual Impact of Scenario'].cumsum()
    cumulative_impact_df = pd.DataFrame({'Cumulative Impact': cumulative_impact})
    return cumulative_impact_df

import pandas as pd


def aggregate_results(simulation_log):
    """Groups the `simulation_log` by `Risk Category` and `Chosen Action`.
    Calculates sum or average of `Residual Financial Impact` for each group.
    Args:
        simulation_log: pandas.DataFrame, the simulation log.
    Returns:
        pandas.DataFrame.
    """
    if simulation_log.empty:
        return pd.DataFrame()

    if 'Residual Financial Impact' not in simulation_log.columns:
        raise KeyError("Residual Financial Impact column not found.")

    if not pd.api.types.is_numeric_dtype(simulation_log['Residual Financial Impact']):
        raise TypeError("Residual Financial Impact column must be numeric.")

    aggregated_results = simulation_log.groupby(['Risk Category', 'Chosen Action'])['Residual Financial Impact'].mean().reset_index()
    return aggregated_results