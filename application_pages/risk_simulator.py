
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

# Initialize session state variables if they don't exist
if 'synthetic_data' not in st.session_state:
    st.session_state['synthetic_data'] = pd.DataFrame()
if 'risk_appetite_thresholds' not in st.session_state:
    st.session_state['risk_appetite_thresholds'] = {
        'Max Acceptable Financial Loss per Incident': 0.0,
        'Max Acceptable Incidents per Period': 0,
        'Max Acceptable Reputational Impact Score': 0.0
    }
if 'simulation_log' not in st.session_state:
    st.session_state['simulation_log'] = pd.DataFrame(columns=[
        'Scenario ID', 'Risk Category', 'Chosen Action',
        'Initial Likelihood', 'Initial Financial Impact', 'Initial Reputational Impact', 'Initial Operational Impact',
        'Residual Likelihood', 'Residual Financial Impact', 'Residual Reputational Impact', 'Residual Operational Impact',
        'Financial Compliance', 'Operational Compliance', 'Reputational Compliance'
    ])

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

def set_risk_appetite_st(max_financial_loss, max_incidents, max_reputational_impact):
    """Stores the risk appetite thresholds in a dictionary."""
    return {
        'Max Acceptable Financial Loss per Incident': float(max_financial_loss),
        'Max Acceptable Incidents per Period': int(max_incidents),
        'Max Acceptable Reputational Impact Score': float(max_reputational_impact)
    }

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

def calculate_cumulative_impact(simulation_log):
    """
    Processes the `simulation_log` to calculate cumulative financial impact and
    cumulative operational compliant incidents.
    Returns the modified simulation_log DataFrame.
    """
    if simulation_log.empty:
        return simulation_log.copy() # Return an empty copy if no data

    df_processed = simulation_log.copy() # Work on a copy

    # Convert 'Residual Financial Impact' to numeric, coercing errors
    if 'Residual Financial Impact' in df_processed.columns:
        df_processed['Residual Financial Impact'] = pd.to_numeric(df_processed['Residual Financial Impact'], errors='coerce')
        df_processed['Cumulative Financial Impact'] = df_processed['Residual Financial Impact'].cumsum()
    else:
        df_processed['Cumulative Financial Impact'] = 0 # Add column even if source is missing

    # Calculate Cumulative Compliant Incidents
    if 'Operational Compliance' in df_processed.columns:
        # Summing True (1) and False (0) for compliance count
        df_processed['Cumulative Compliant Incidents'] = df_processed['Operational Compliance'].astype(int).cumsum()
    else:
        df_processed['Cumulative Compliant Incidents'] = 0 # Add column even if source is missing

    return df_processed

def aggregate_results(simulation_log):
    """
    Groups the `simulation_log` by `Risk Category` and `Chosen Action`.
    Calculates sum of `Residual Financial Impact` for each group.
    Returns the grouped DataFrame.
    """
    if simulation_log.empty:
        return pd.DataFrame() # Return empty DataFrame if log is empty

    df_agg = simulation_log.copy()
    try:
        # Ensure 'Residual Financial Impact' is numeric before grouping
        df_agg['Residual Financial Impact'] = pd.to_numeric(df_agg['Residual Financial Impact'], errors='coerce')
        
        # Drop rows where 'Residual Financial Impact' became NaN due to coercion errors
        df_agg.dropna(subset=['Residual Financial Impact'], inplace=True)

        if df_agg.empty: # Check if DataFrame is empty after dropping NaNs
            return pd.DataFrame()

        # Group by 'Risk Category' and 'Chosen Action' and sum 'Residual Financial Impact'
        grouped = df_agg.groupby(['Risk Category', 'Chosen Action'])['Residual Financial Impact'].sum().reset_index()
        return grouped
    except KeyError as e:
        st.error(f"Missing expected column for aggregation: {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"An error occurred during aggregation: {e}")
        return pd.DataFrame()

def run_risk_simulator():
    # Step 1: Generating Synthetic Risk Scenario Data
    st.sidebar.header("Step 1: Generate Synthetic Risk Data")
    st.markdown("""
    ### Step 1: Generating Synthetic Risk Scenario Data
    **Business Value:**
    Simulating diverse risk events is crucial for testing and optimizing governance policies. Generating synthetic data across categories (Strategic, Financial, Operational, Compliance, Reputational) creates a safe testbed to evaluate risk responses and appetite settings. This aligns with governance best practice: "understand your risk universe" before defining appetite.

    **Formulae:**
    - Financial impact per event $\sim \mathrm{Uniform}(0, 100000)$
    - Reputational impact per event $\sim \mathrm{Uniform}(0, 10)$
    - Operational impact per event $\sim \mathrm{Uniform}(0, 100)$
    """)
    num_scenarios = st.sidebar.slider("Number of Scenarios", 5, 500, 50, help="Define how many synthetic risk scenarios to generate.")
    seed_input = st.sidebar.text_input("Random Seed (optional)", "", help="Enter an integer for reproducibility. Leave empty for random.")

    if st.sidebar.button("Generate Data"):
        try:
            seed = int(seed_input) if seed_input else None
            st.session_state['synthetic_data'] = generate_synthetic_data(num_scenarios, seed=seed)
            st.success(f"Generated {num_scenarios} synthetic risk scenarios.")
        except ValueError:
            st.error("Please enter a valid integer for the random seed.")

    st.subheader("Synthetic Risk Scenarios")
    if not st.session_state['synthetic_data'].empty:
        st.dataframe(st.session_state['synthetic_data'])
    else:
        st.info("Generate synthetic data using the sidebar controls.")

    st.divider()

    # Step 2: Defining the Firm's Risk Appetite
    st.sidebar.header("Step 2: Define Risk Appetite")
    st.markdown("""
    ### Step 2: Defining the Firm's Risk Appetite
    **Business Value:**
    Defining numerical risk appetite thresholds is a key activity for the board and senior management. These thresholds ensure management actions and decisions are anchored to the organization's capacity, supporting transparency and accountability.
    """)
    max_financial_loss = st.sidebar.number_input(
        "Max Acceptable Financial Loss per Incident ($)",
        min_value=0.0, value=50000.0, step=1000.0,
        help="The maximum financial loss per incident the firm is willing to tolerate."
    )
    max_incidents = st.sidebar.number_input(
        "Max Acceptable Incidents per Period",
        min_value=0, value=10, step=1,
        help="Sets a cap on operational events per period, enforcing operational discipline."
    )
    max_reputational_impact = st.sidebar.number_input(
        "Max Acceptable Reputational Impact Score",
        min_value=0.0, max_value=10.0, value=5.0, step=0.1,
        help="Limits damage to the firm's public standing (score out of 10)."
    )

    # Update risk appetite thresholds immediately as inputs change
    st.session_state['risk_appetite_thresholds'] = set_risk_appetite_st(
        max_financial_loss, max_incidents, max_reputational_impact
    )

    st.subheader("Current Risk Appetite Thresholds")
    st.write(f"**Max Financial Loss:** ${st.session_state['risk_appetite_thresholds']['Max Acceptable Financial Loss per Incident']:,}")
    st.write(f"**Max Incidents:** {st.session_state['risk_appetite_thresholds']['Max Acceptable Incidents per Period']}")
    st.write(f"**Max Reputational Impact:** {st.session_state['risk_appetite_thresholds']['Max Acceptable Reputational Impact Score']:.1f}")

    st.divider()

    # Step 3: Simulating Scenario Outcomes Based on Risk Management Actions
    st.sidebar.header("Step 3: Simulate Scenario Outcome")
    st.markdown("""
    ### Step 3: Simulating Scenario Outcomes Based on Risk Management Actions
    **Business Value:**
    This step models the impact of various risk management actions on the likelihood and impact of risk events, allowing users to observe the effect of their decisions. Compliance is evaluated by verifying that the residual impacts are within the predefined risk appetite.

    **Formulae:**
    -   **Mitigate:**
        -   Residual Likelihood = Initial Likelihood $ \times $ (1 - Mitigation Factor (Likelihood Reduction %))
        -   Residual Impact = Initial Impact $ \times $ (1 - Mitigation Factor (Impact Reduction %))
    -   **Transfer:**
        -   Covered Amount = Initial Financial Impact $ \times $ Insurance Coverage Ratio (%)
        -   Residual Financial Impact = max(0, Initial Financial Impact - Covered Amount) - Insurance Deductible
    -   **Eliminate:**
        -   Residual Likelihood = 0
        -   Residual Impact = 0
    """)

    if not st.session_state['synthetic_data'].empty:
        scenario_ids = st.session_state['synthetic_data']['Scenario ID'].tolist()
        selected_scenario_id = st.sidebar.selectbox("Select Scenario to Simulate", scenario_ids, help="Choose a scenario to apply a risk management action.")
        selected_scenario = st.session_state['synthetic_data'][
            st.session_state['synthetic_data']['Scenario ID'] == selected_scenario_id
        ].iloc[0]

        action_options = ['Accept', 'Mitigate', 'Transfer', 'Eliminate']
        selected_action = st.sidebar.selectbox("Choose Risk Management Action", action_options, help="Select a strategy to manage the chosen risk scenario.")

        action_params = {}
        if selected_action == 'Mitigate':
            action_params['Mitigation Factor (Impact Reduction %)'] = st.sidebar.slider(
                "Impact Reduction (%)", 0.0, 1.0, 0.5, 0.05,
                help="Proportion by which impact (financial, reputational, operational) is reduced."
            )
            action_params['Mitigation Factor (Likelihood Reduction %)'] = st.sidebar.slider(
                "Likelihood Reduction (%)", 0.0, 1.0, 0.5, 0.05,
                help="Proportion by which likelihood is reduced."
            )
        elif selected_action == 'Transfer':
            action_params['Insurance Deductible ($)'] = st.sidebar.number_input(
                "Insurance Deductible ($)", 0.0, 50000.0, 0.0, 100.0,
                help="Amount of financial loss not covered by insurance."
            )
            action_params['Insurance Coverage Ratio (%)'] = st.sidebar.slider(
                "Insurance Coverage Ratio (%)", 0.0, 1.0, 0.8, 0.05,
                help="Proportion of financial loss covered by insurance."
            )

        if st.sidebar.button("Run Simulation"):
            outcome = simulate_scenario_outcome(
                selected_scenario, selected_action, action_params, st.session_state['risk_appetite_thresholds']
            )
            st.session_state['last_simulated_outcome'] = outcome
            st.success(f"Simulation run for Scenario ID: {selected_scenario_id} with action: {selected_action}")
            st.subheader("Simulated Scenario Outcome")
            st.dataframe(pd.DataFrame([outcome]).set_index('Scenario ID')) # Display the single outcome

    else:
        st.sidebar.warning("Please generate synthetic data first to simulate scenarios.")
        st.info("Simulated Scenario Outcome will appear here after running a simulation.")

    st.divider()

    # Step 4: Logging Simulation Outcomes for Audit and Governance
    st.markdown("""
    ### Step 4: Logging Simulation Outcomes for Audit and Governance
    **Business Value:**
    Maintaining a historical log of simulated risk scenarios and their policy outcomes is vital for compliance, continuous governance improvement, and enabling trend/portfolio analysis. This aligns with good governance practices: tracking and reviewing risk-response effectiveness over time.
    """)
    if 'last_simulated_outcome' in st.session_state and st.session_state['last_simulated_outcome']:
        st.session_state['simulation_log'] = update_simulation_log_st(
            st.session_state['simulation_log'], st.session_state.pop('last_simulated_outcome')
        )
    
    st.subheader("Simulation Log")
    if not st.session_state['simulation_log'].empty:
        st.dataframe(st.session_state['simulation_log'])
    else:
        st.info("Run simulations to see the log here.")

    st.divider()

    # Step 5: Calculating Cumulative Impact Over Time
    st.markdown("""
    ### Step 5: Calculating Cumulative Impact Over Time
    **Business Value:**
    Aggregating risk impacts over time offers decision-makers critical insights into policy performance long-term. Tracking cumulative financial losses and incident counts helps identify trends, reassess risk appetites, and adjust mitigation strategies proactively.

    **Formula:**
    - Cumulative Financial Impact: $ CumulativeFinancialImpact_t = \sum_{i=1}^{t} ResidualFinancialImpact_i $
    """)
    st.subheader("Cumulative Impact Trends")
    processed_log = calculate_cumulative_impact(st.session_state['simulation_log'])

    if not processed_log.empty and 'Cumulative Financial Impact' in processed_log.columns and 'Cumulative Compliant Incidents' in processed_log.columns:
        # Ensure Scenario ID is treated as a continuous variable for plotting trends
        processed_log['Scenario Number'] = processed_log.index + 1

        # Plot Cumulative Financial Impact
        fig_finance = px.line(
            processed_log,
            x='Scenario Number',
            y='Cumulative Financial Impact',
            title='Cumulative Financial Impact Over Simulated Scenarios',
            labels={'Scenario Number': 'Scenario Number', 'Cumulative Financial Impact': 'Cumulative Financial Loss ($)'},
            hover_data={
                'Scenario ID': True,
                'Initial Financial Impact': ':.2f',
                'Residual Financial Impact': ':.2f',
                'Financial Compliance': True
            }
        )
        st.plotly_chart(fig_finance, use_container_width=True)

        # Plot Cumulative Compliant Incidents
        fig_incidents = px.line(
            processed_log,
            x='Scenario Number',
            y='Cumulative Compliant Incidents',
            title='Cumulative Compliant Operational Incidents Over Simulated Scenarios',
            labels={'Scenario Number': 'Scenario Number', 'Cumulative Compliant Incidents': 'Number of Compliant Incidents'},
             hover_data={
                'Scenario ID': True,
                'Initial Operational Impact': ':.2f',
                'Operational Compliance': True
            }
        )
        st.plotly_chart(fig_incidents, use_container_width=True)
    else:
        st.info("Run simulations to visualize cumulative impacts.")

    st.divider()
    
    # Relationship Plot (Initial vs. Residual Impact)
    st.markdown("""
    #### Initial vs. Residual Financial Impact
    This plot visualizes how risk management actions reduce the financial impact of events. Points below the "Max Acceptable Financial Loss" line are compliant with the firm's risk appetite.
    """)
    if not st.session_state['simulation_log'].empty:
        fig_scatter = px.scatter(
            st.session_state['simulation_log'],
            x='Initial Financial Impact',
            y='Residual Financial Impact',
            color='Financial Compliance',
            title='Initial vs. Residual Financial Impact per Scenario',
            labels={
                'Initial Financial Impact': 'Initial Financial Impact ($)',
                'Residual Financial Impact': 'Residual Financial Impact ($)',
                'Financial Compliance': 'In Financial Compliance'
            },
            hover_data={
                'Scenario ID': True,
                'Risk Category': True,
                'Chosen Action': True
            }
        )
        
        max_loss_threshold = st.session_state['risk_appetite_thresholds']['Max Acceptable Financial Loss per Incident']
        fig_scatter.add_hline(
            y=max_loss_threshold,
            line_dash="dot",
            line_color="red",
            annotation_text=f"Max Acceptable Financial Loss: ${max_loss_threshold:,}",
            annotation_position="bottom right"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.info("Run simulations to see the Initial vs. Residual Impact plot.")

    st.divider()

    # Step 6: Aggregating Results to Identify High-Risk Areas
    st.markdown("""
    ### Step 6: Aggregating Results to Identify High-Risk Areas
    **Business Value:**
    Grouping simulation results by risk category and chosen action allows senior management to quickly pinpoint areas with the greatest financial impact, where certain actions are more or less effective, and where risk appetite is most frequently breached. This targeted insight enables efficient resource allocation and focused policy adjustments.
    """)
    st.subheader("Aggregated Risk Insights")
    aggregated_df = aggregate_results(st.session_state['simulation_log'])

    if not aggregated_df.empty:
        st.dataframe(aggregated_df)

        fig_agg = px.bar(
            aggregated_df,
            x='Risk Category',
            y='Residual Financial Impact',
            color='Chosen Action',
            barmode='group',
            title='Aggregated Residual Financial Impact by Risk Category and Action',
            labels={
                'Risk Category': 'Risk Category',
                'Residual Financial Impact': 'Total Residual Financial Impact ($)',
                'Chosen Action': 'Action Taken'
            },
            hover_data={
                'Risk Category': True,
                'Chosen Action': True,
                'Residual Financial Impact': ':.2f'
            }
        )
        st.plotly_chart(fig_agg, use_container_width=True)
    else:
        st.info("Run simulations and log outcomes to view aggregated results.")

