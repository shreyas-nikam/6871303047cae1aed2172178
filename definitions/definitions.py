import pandas as pd
import numpy as np

def generate_synthetic_data(num_scenarios, seed=None):
    """Generates a DataFrame with synthetic risk scenario data."""
    if seed is not None:
        np.random.seed(seed)

    risk_categories = ['Strategic', 'Financial', 'Operational', 'Compliance', 'Reputational']

    data = {
        'Scenario ID': range(1, num_scenarios + 1),
        'Risk Category': np.random.choice(risk_categories, num_scenarios),
        'Initial Likelihood': np.random.rand(num_scenarios),
        'Initial Impact (Financial)': np.random.rand(num_scenarios) * 100000,
        'Initial Impact (Reputational)': np.random.rand(num_scenarios) * 10,
        'Initial Impact (Operational)': np.random.rand(num_scenarios) * 100
    }

    df = pd.DataFrame(data)
    return df

def set_risk_appetite(max_financial_loss, max_incidents, max_reputational_impact):
                """Stores the risk appetite thresholds."""

                global _max_financial_loss
                global _max_incidents
                global _max_reputational_impact

                _max_financial_loss = max_financial_loss
                _max_incidents = max_incidents
                _max_reputational_impact = max_reputational_impact

import pandas as pd

def simulate_scenario_outcome(scenario_data, action, action_params, risk_appetite_thresholds):
    """Simulates the outcome of a risk management scenario."""

    initial_likelihood = scenario_data['Initial Likelihood']
    initial_financial_impact = scenario_data['Initial Impact (Financial)']
    initial_reputational_impact = scenario_data['Initial Impact (Reputational)']
    initial_operational_impact = scenario_data['Initial Impact (Operational)']

    residual_likelihood = initial_likelihood
    residual_financial_impact = initial_financial_impact
    residual_reputational_impact = initial_reputational_impact
    residual_operational_impact = initial_operational_impact

    if action == 'Accept':
        pass  # No changes to impact or likelihood

    elif action == 'Mitigate':
        mitigation_impact_reduction = action_params.get('Mitigation Factor (Impact Reduction %)', 0)
        mitigation_likelihood_reduction = action_params.get('Mitigation Factor (Likelihood Reduction %)', 0)

        residual_likelihood = initial_likelihood * (1 - mitigation_likelihood_reduction)
        residual_financial_impact = initial_financial_impact * (1 - mitigation_impact_reduction)
        residual_reputational_impact = initial_reputational_impact * (1 - mitigation_impact_reduction)
        residual_operational_impact = initial_operational_impact * (1 - mitigation_impact_reduction)

    elif action == 'Transfer':
        insurance_deductible = action_params.get('Insurance Deductible ($)', 0)
        insurance_coverage_ratio = action_params.get('Insurance Coverage Ratio (%)', 0)

        covered_amount = initial_financial_impact * insurance_coverage_ratio
        residual_financial_impact = max(0, initial_financial_impact - covered_amount)
        residual_financial_impact = max(0, residual_financial_impact - insurance_deductible)


    elif action == 'Eliminate':
        residual_likelihood = 0
        residual_financial_impact = 0
        residual_reputational_impact = 0
        residual_operational_impact = 0


    else:
        raise Exception("Invalid action specified.")

    # Compliance Check
    financial_compliance = residual_financial_impact <= risk_appetite_thresholds['Max Acceptable Financial Loss per Incident']
    operational_compliance = initial_operational_impact <= risk_appetite_thresholds['Max Acceptable Incidents per Period']
    reputational_compliance = residual_reputational_impact <= risk_appetite_thresholds['Max Acceptable Reputational Impact Score']


    result = {
        'Initial Likelihood': initial_likelihood,
        'Initial Financial Impact': initial_financial_impact,
        'Initial Reputational Impact': initial_reputational_impact,
        'Initial Operational Impact': initial_operational_impact,
        'Residual Likelihood': residual_likelihood,
        'Residual Financial Impact': residual_financial_impact,
        'Residual Reputational Impact': residual_reputational_impact,
        'Residual Operational Impact': residual_operational_impact,
        'Financial Compliance': financial_compliance,
        'Operational Compliance': operational_compliance,
        'Reputational Compliance': reputational_compliance
    }

    return None

import pandas as pd

_simulation_log = pd.DataFrame()

def update_simulation_log(scenario_outcome):
    """Appends scenario outcome to a historical pandas.DataFrame log."""
    global _simulation_log

    if scenario_outcome is None:
        raise TypeError("Scenario outcome cannot be None.")

    if not isinstance(scenario_outcome, dict):
        raise TypeError("Scenario outcome must be a dictionary.")
    
    if not scenario_outcome:
         raise KeyError("Scenario outcome dictionary cannot be empty.")

    if 'Scenario ID' not in scenario_outcome or 'Residual Impact' not in scenario_outcome:
        raise KeyError("Scenario outcome must contain 'Scenario ID' and 'Residual Impact'.")

    if not isinstance(scenario_outcome['Scenario ID'], str):
        raise TypeError("Scenario ID must be a string.")

    if not isinstance(scenario_outcome['Residual Impact'], (int, float)):
        raise TypeError("Residual Impact must be a number.")

    new_row = pd.DataFrame([scenario_outcome])

    _simulation_log = pd.concat([_simulation_log, new_row], ignore_index=True)

import pandas as pd

def calculate_cumulative_impact(simulation_log):
    """Processes the `simulation_log` to calculate cumulative financial impact and cumulative incident count.

    Args:
        simulation_log: The historical log of simulated scenarios.
    """

    if simulation_log.empty:
        return

    if 'Residual Financial Impact' in simulation_log.columns:
        try:
            simulation_log['Cumulative Financial Impact'] = simulation_log['Residual Financial Impact'].cumsum()
        except TypeError:
            raise TypeError("Financial impact data must be numeric.")

    if 'Operational Incident Compliance' in simulation_log.columns:
        simulation_log['Cumulative Compliant Incidents'] = simulation_log['Operational Incident Compliance'].cumsum()

import pandas as pd

def aggregate_results(simulation_log):
    """Groups the `simulation_log` by `Risk Category` and `Chosen Action`.
    Calculates sum of `Residual Financial Impact` for each group.
    Args:
        simulation_log: The historical log of simulated scenarios and their outcomes.
    Output: None
    """
    if simulation_log.empty:
        return None

    try:
        simulation_log['Residual Financial Impact'] = pd.to_numeric(simulation_log['Residual Financial Impact'], errors='raise')
        grouped = simulation_log.groupby(['Risk Category', 'Chosen Action'])['Residual Financial Impact'].sum()
    except (ValueError, TypeError):
        return None
    except KeyError:
        return None
    
    return None