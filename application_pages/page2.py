
import streamlit as st
import pandas as pd
import numpy as np

def simulate_scenario_outcome(scenario_data, action, action_params, risk_appetite_thresholds):
    """
    Simulates the outcome of a risk management scenario.
    Returns a dictionary of results including compliance.
    """
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
        mitigation_impact_reduction = action_params.get('Mitigation Factor (Impact Reduction %)', 0.0)
        mitigation_likelihood_reduction = action_params.get('Mitigation Factor (Likelihood Reduction %)', 0.0)

        residual_likelihood = initial_likelihood * (1 - mitigation_likelihood_reduction)
        residual_financial_impact = initial_financial_impact * (1 - mitigation_impact_reduction)
        residual_reputational_impact = initial_reputational_impact * (1 - mitigation_impact_reduction)
        residual_operational_impact = initial_operational_impact * (1 - mitigation_impact_reduction)

    elif action == 'Transfer':
        insurance_deductible = action_params.get('Insurance Deductible ($)', 0.0)
        insurance_coverage_ratio = action_params.get('Insurance Coverage Ratio (%)', 0.0)

        covered_amount = initial_financial_impact * insurance_coverage_ratio
        residual_financial_impact = max(0.0, initial_financial_impact - covered_amount - insurance_deductible) # Deductible applied after coverage

    elif action == 'Eliminate':
        residual_likelihood = 0.0
        residual_financial_impact = 0.0
        residual_reputational_impact = 0.0
        residual_operational_impact = 0.0

    else:
        raise ValueError("Invalid action specified.")

    # Compliance Check (Note: Operational compliance is checked against initial operational impact per notebook context)
    financial_compliance = residual_financial_impact <= risk_appetite_thresholds['Max Acceptable Financial Loss per Incident']
    operational_compliance = initial_operational_impact <= risk_appetite_thresholds['Max Acceptable Incidents per Period'] # Checked against Initial Impact
    reputational_compliance = residual_reputational_impact <= risk_appetite_thresholds['Max Acceptable Reputational Impact Score']

    result = {
        'Scenario ID': scenario_data['Scenario ID'],
        'Risk Category': scenario_data['Risk Category'],
        'Chosen Action': action,
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
    return result

def update_simulation_log_st(simulation_log_df, scenario_outcome):
    """
    Appends scenario outcome to a historical pandas.DataFrame log.
    Returns the updated DataFrame.
    """
    if scenario_outcome is None:
        raise TypeError("Scenario outcome cannot be None.")
    if not isinstance(scenario_outcome, dict):
        raise TypeError("Scenario outcome must be a dictionary.")
    if not scenario_outcome:
         raise KeyError("Scenario outcome dictionary cannot be empty.")
    
    # Ensure all expected columns are present to avoid future issues with concat
    expected_cols = [
        'Scenario ID', 'Risk Category', 'Chosen Action',
        'Initial Likelihood', 'Initial Financial Impact', 'Initial Reputational Impact', 'Initial Operational Impact',
        'Residual Likelihood', 'Residual Financial Impact', 'Residual Reputational Impact', 'Residual Operational Impact',
        'Financial Compliance', 'Operational Compliance', 'Reputational Compliance'
    ]
    new_row_df = pd.DataFrame([scenario_outcome])
    
    # Add missing columns to new_row_df if any, filling with NaN
    for col in expected_cols:
        if col not in new_row_df.columns:
            new_row_df[col] = np.nan

    # Ensure consistent order of columns before concatenation
    new_row_df = new_row_df[expected_cols]

    return pd.concat([simulation_log_df, new_row_df], ignore_index=True)


def run_page2():
    st.header("Scenario Simulation & Log")

    st.markdown("""
    ### Step 3: Simulating Scenario Outcomes Based on Risk Management Actions

    **Business Value:**
    This step models the impact of various risk management actions on the likelihood and impact of risk events, allowing users to observe the effect of their decisions. Compliance is evaluated by verifying that the residual impacts are within the predefined risk appetite.

    **Formulae:**
    *   **Mitigate:**
        *   Residual Likelihood = Initial Likelihood $ \times $ (1 - Mitigation Factor (Likelihood Reduction %))
        *   Residual Impact = Initial Impact $ \times $ (1 - Mitigation Factor (Impact Reduction %))
    *   **Transfer:**
        *   Covered Amount = Initial Financial Impact $ \times $ Insurance Coverage Ratio (%)
        *   Residual Financial Impact = max(0, Initial Financial Impact - Covered Amount) - Insurance Deductible
    *   **Eliminate:**
        *   Residual Likelihood = 0
        *   Residual Impact = 0
    """)

    st.subheader("Simulate Scenario Outcome")

    if not st.session_state['synthetic_data'].empty:
        scenario_ids = st.session_state['synthetic_data']['Scenario ID'].tolist()
        selected_scenario_id = st.selectbox("Select Scenario to Simulate", scenario_ids, help="Choose a scenario to apply a risk management action.")
        selected_scenario = st.session_state['synthetic_data'][
            st.session_state['synthetic_data']['Scenario ID'] == selected_scenario_id
        ].iloc[0]

        st.info(f"Selected Scenario Details (ID: {selected_scenario_id}):")
        st.write(f"- **Risk Category:** {selected_scenario['Risk Category']}")
        st.write(f"- **Initial Financial Impact:** ${selected_scenario['Initial Impact (Financial)']:,}")
        st.write(f"- **Initial Reputational Impact:** {selected_scenario['Initial Impact (Reputational)']:.1f}")
        st.write(f"- **Initial Operational Impact:** {selected_scenario['Initial Impact (Operational)']:.1f}")

        action_options = ['Accept', 'Mitigate', 'Transfer', 'Eliminate']
        selected_action = st.selectbox("Choose Risk Management Action", action_options, help="Select a strategy to manage the chosen risk scenario.")

        action_params = {}
        if selected_action == 'Mitigate':
            action_params['Mitigation Factor (Impact Reduction %)'] = st.slider(
                "Impact Reduction (%)", 0.0, 1.0, 0.5, 0.05,
                help="Proportion by which impact (financial, reputational, operational) is reduced."
            )
            action_params['Mitigation Factor (Likelihood Reduction %)'] = st.slider(
                "Likelihood Reduction (%)", 0.0, 1.0, 0.5, 0.05,
                help="Proportion by which likelihood is reduced."
            )
        elif selected_action == 'Transfer':
            action_params['Insurance Deductible ($)'] = st.number_input(
                "Insurance Deductible ($)", 0.0, 50000.0, 0.0, 100.0,
                help="Amount of financial loss not covered by insurance."
            )
            action_params['Insurance Coverage Ratio (%)'] = st.slider(
                "Insurance Coverage Ratio (%)", 0.0, 1.0, 0.8, 0.05,
                help="Proportion of financial loss covered by insurance."
            )

        if st.button("Run Simulation"):
            with st.spinner("Running simulation..."):
                outcome = simulate_scenario_outcome(
                    selected_scenario, selected_action, action_params, st.session_state['risk_appetite_thresholds']
                )
                st.session_state['last_simulated_outcome'] = outcome
                st.success(f"Simulation run for Scenario ID: {selected_scenario_id} with action: {selected_action}")
            
            st.markdown("""
            **Simulation Outcome:**
            The table below shows the results of the last simulation, including the initial impacts, the chosen action, the residual impacts after applying the action, and the compliance status against the defined risk appetite thresholds.
            """)
            st.dataframe(pd.DataFrame([outcome]).set_index('Scenario ID'), use_container_width=True)

    else:
        st.warning("Please generate synthetic data on the 'Data Generation & Risk Appetite' page first to simulate scenarios.")
        st.info("Simulated Scenario Outcome will appear here after running a simulation.")

    st.markdown("""
    ---
    ### Step 4: Logging Simulation Outcomes for Audit and Governance

    **Business Value:**
    Maintaining a historical log of simulated risk scenarios and their policy outcomes is vital for compliance, continuous governance improvement, and enabling trend/portfolio analysis. This aligns with good governance practices: tracking and reviewing risk-response effectiveness over time.
    """)

    st.subheader("Simulation Log")
    # This block processes the 'last_simulated_outcome' into the main 'simulation_log'
    if 'last_simulated_outcome' in st.session_state and st.session_state['last_simulated_outcome'] is not None:
        try:
            st.session_state['simulation_log'] = update_simulation_log_st(
                st.session_state['simulation_log'], st.session_state.pop('last_simulated_outcome')
            )
        except (TypeError, KeyError) as e:
            st.error(f"Error updating simulation log: {e}")
            st.session_state['last_simulated_outcome'] = None # Reset to prevent continuous errors
    
    if not st.session_state['simulation_log'].empty:
        st.dataframe(st.session_state['simulation_log'], use_container_width=True)
    else:
        st.info("Run simulations to see the log here. Each successful simulation will be added.")
