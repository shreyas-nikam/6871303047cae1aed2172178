
# Streamlit Application Requirements Specification: Risk Appetite & Governance Simulator

This document outlines the requirements for developing a Streamlit application based on the provided Jupyter Notebook content and user specifications. It aims to provide a blueprint for an interactive tool that simulates risk management strategies and visualizes their impact within a firm's defined risk appetite.

## 1. Application Overview

**Purpose and Objectives:**
The primary purpose of this Streamlit application is to create an interactive simulator for corporate governance professionals, risk practitioners, and finance students. It will demonstrate how risk appetite boundaries influence a firm's ability to manage various risk exposures, and how different governance and policy choices dynamically shape an organization's risk profile in real-time.

**Key Objectives:**
*   Enable users to define and quantify risk appetite thresholds across financial, operational, and reputational dimensions.
*   Allow users to simulate risk events and apply various risk management strategies (Accept, Mitigate, Transfer, Eliminate).
*   Provide a compliance dashboard to visualize actual risk exposure against defined risk appetite boundaries.
*   Display cumulative impact trends of losses and incidents over time under different governance setups.
*   Facilitate aggregated policy analysis to compare the effectiveness of different risk management approaches across various risk categories.

## 2. User Interface Requirements

**Layout and Navigation Structure:**
The application will feature a clear, intuitive layout:
*   **Sidebar:** Will host primary input widgets and controls for defining parameters, generating data, and setting risk appetite.
*   **Main Content Area:** Will display the simulation results, interactive tables, and various visualization components (plots, charts, dashboards) across different sections corresponding to the simulation steps.
*   **Sectional Organization:** Content will be logically divided into distinct sections (e.g., "Step 1: Data Generation," "Step 2: Risk Appetite," "Step 3: Scenario Simulation") to guide the user through the workflow.

**Input Widgets and Controls:**
Users will interact with the application through the following components, primarily located in the sidebar:

*   **1. Risk Scenario Data Generation:**
    *   **Number of Scenarios:** `st.slider` or `st.number_input` (integer, e.g., 5 to 500) to specify the quantity of synthetic risk events.
    *   **Random Seed:** `st.text_input` to allow users to set a seed for reproducible data generation.
    *   **Action Button:** `st.button` to trigger the data generation process.

*   **2. Firm's Risk Appetite Definition:**
    *   **Max Acceptable Financial Loss:** `st.number_input` or `st.slider` (float, e.g., $0 to $100,000) for the maximum financial loss per incident.
    *   **Max Operational Incidents:** `st.number_input` or `st.slider` (integer, e.g., 1 to 20) for the maximum number of operational incidents per period.
    *   **Max Reputational Impact Score:** `st.number_input` or `st.slider` (float, e.g., 0 to 10) for the maximum acceptable reputational impact score.

*   **3. Scenario Outcome Simulation:**
    *   **Select Scenario:** `st.selectbox` to choose a specific scenario (by `Scenario ID`) from the generated synthetic data for simulation.
    *   **Choose Action:** `st.selectbox` with options: 'Accept', 'Mitigate', 'Transfer', 'Eliminate'.
    *   **Action-Specific Parameters (Conditional Visibility):**
        *   **If 'Mitigate' is selected:**
            *   `Mitigation Factor (Impact Reduction %)`: `st.slider` (float, 0.0 to 1.0, step 0.05).
            *   `Mitigation Factor (Likelihood Reduction %)`: `st.slider` (float, 0.0 to 1.0, step 0.05).
        *   **If 'Transfer' is selected:**
            *   `Insurance Deductible ($)`: `st.number_input` (float, e.g., $0 to $20,000).
            *   `Insurance Coverage Ratio (%)`: `st.slider` (float, 0.0 to 1.0, step 0.05).
    *   **Run Simulation Button:** `st.button` to execute the selected risk management action on the chosen scenario.

**Visualization Components:**
The application will leverage Streamlit's visualization capabilities to present data and simulation results effectively.

*   **Data Tables:** `st.dataframe` will be used to display:
    *   The generated synthetic risk scenario data.
    *   The cumulative simulation log, showing initial and residual impacts, along with compliance status for each simulated event.
    *   Aggregated results, summarizing financial impacts by risk category and chosen action.
*   **Core Visuals (using Plotly for interactivity):**
    1.  **Trend Plot (Cumulative Impact):** A `plotly.express.line` chart displaying:
        *   "Cumulative Financial Impact" over `Scenario ID` (or simulation step).
        *   "Cumulative Compliant Incidents" over `Scenario ID` (or simulation step).
        *   Clear titles, labeled axes (e.g., "Scenario Number" vs. "Cumulative Financial Loss ($)"), and legends.
    2.  **Relationship Plot (Initial vs. Residual Impact):** A `plotly.express.scatter` plot showing:
        *   "Initial Financial Impact" vs. "Residual Financial Impact" for all simulated scenarios.
        *   Points colored based on "Financial Compliance" status (True/False).
        *   A horizontal line representing the "Max Acceptable Financial Loss per Incident" from the risk appetite thresholds.
        *   Clear titles and labeled axes.
    3.  **Aggregated Comparison (Bar Chart):** A `plotly.express.bar` chart visualizing:
        *   Sum of "Residual Financial Impact" grouped by "Risk Category" and "Chosen Action".
        *   Allows for comparison of effectiveness across different actions and categories.
        *   Clear titles, labeled axes, and legends.

**Interactive Elements and Feedback Mechanisms:**
*   **Dynamic Updates:** All charts and tables will automatically update as input parameters (e.g., risk appetite thresholds, simulation action parameters) are changed or new simulations are run.
*   **Tooltips and Help Text:** Inline help text or `st.help` and `st.info` will be provided next to input controls to explain their purpose and expected values, enhancing user understanding as per user requirements.
*   **Compliance Status Indicators:** The simulation outcome display will clearly indicate (e.g., "In Compliance" / "Out of Compliance") for financial, operational, and reputational metrics.
*   **Error Handling/Messages:** Informative messages will guide the user if invalid inputs are provided or if data processing encounters issues (e.g., empty simulation log for cumulative calculations).

## 3. Additional Requirements

**Real-time Updates and Responsiveness:**
The Streamlit application will be designed for near real-time interactivity. Changes to input sliders or dropdowns will trigger immediate re-execution of relevant calculations and updates to displayed data and visualizations without requiring manual refresh. This ensures a dynamic and engaging user experience.

**Annotation and Tooltip Specifications:**
*   **Input Controls:** Each input widget (sliders, number inputs, select boxes) will include `help` parameters or nearby `st.info` boxes explaining its function and impact on the simulation.
*   **Visualizations:**
    *   **Risk Appetite Lines:** Critical thresholds from the defined risk appetite (e.g., maximum acceptable financial loss) will be plotted as horizontal reference lines on relevant charts (e.g., the financial impact scatter plot) to visually indicate compliance boundaries.
    *   **Data Point Tooltips:** Interactive plots (e.g., Scatter, Line Charts) will feature tooltips on hover to display detailed information for specific data points (e.g., Scenario ID, Initial Impact, Residual Impact, Compliance Status for a simulated event).
    *   **Explanatory Text:** Markdown cells (`st.markdown`) will be used throughout the application to provide narrative explanations of the current step, the business value of the analysis, and interpretations of the displayed results and plots, mirroring the narrative cells from the Jupyter Notebook.

## 4. Notebook Content and Code Requirements

This section details the Python code extracted from the Jupyter Notebook and how it will be integrated into the Streamlit application, along with necessary modifications for a web environment. Global variables from the notebook will be managed using Streamlit's `st.session_state`.

**Core Libraries:**
The application will primarily use `pandas` for data manipulation, `numpy` for numerical operations, and `plotly.express` for interactive visualizations.

```python
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
```

**Streamlit Session State Initialization:**
All dynamic data and state variables will be stored in `st.session_state` to maintain persistence across reruns.

```python
# Initialize session state variables if they don't exist
if 'synthetic_data' not in st.session_state:
    st.session_state['synthetic_data'] = pd.DataFrame()
if 'risk_appetite_thresholds' not in st.session_state:
    st.session_state['risk_appetite_thresholds'] = {
        'Max Acceptable Financial Loss per Incident': 0,
        'Max Acceptable Incidents per Period': 0,
        'Max Acceptable Reputational Impact Score': 0
    }
if 'simulation_log' not in st.session_state:
    st.session_state['simulation_log'] = pd.DataFrame(columns=[
        'Scenario ID', 'Risk Category', 'Chosen Action',
        'Initial Likelihood', 'Initial Financial Impact', 'Initial Reputational Impact', 'Initial Operational Impact',
        'Residual Likelihood', 'Residual Financial Impact', 'Residual Reputational Impact', 'Residual Operational Impact',
        'Financial Compliance', 'Operational Compliance', 'Reputational Compliance'
    ])
```

---

### Step 1: Generating Synthetic Risk Scenario Data

**Business Value:**
Simulating diverse risk events is crucial for testing and optimizing governance policies. Generating synthetic data across categories (Strategic, Financial, Operational, Compliance, Reputational) creates a safe testbed to evaluate risk responses and appetite settings. This aligns with governance best practice: "understand your risk universe" before defining appetite.

**Technical Implementation:**
The `generate_synthetic_data` function will be called with user-defined parameters for the number of scenarios and an optional random seed. The generated DataFrame will be stored in `st.session_state.synthetic_data` and displayed to the user.

**Formulae:**
*   Financial impact per event $\sim \mathrm{Uniform}(0, 100000)$
*   Reputational impact per event $\sim \mathrm{Uniform}(0, 10)$
*   Operational impact per event $\sim \mathrm{Uniform}(0, 100)$

**Relevant Code:**
```python
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
```

**Streamlit Integration:**
```python
st.sidebar.header("Step 1: Generate Synthetic Risk Data")
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
```

---

### Step 2: Defining the Firm's Risk Appetite

**Business Value:**
Defining numerical risk appetite thresholds is a key activity for the board and senior management. These thresholds ensure management actions and decisions are anchored to the organization's capacity, supporting transparency and accountability.

**Technical Implementation:**
The `set_risk_appetite_st` function will capture user-defined thresholds and store them in `st.session_state.risk_appetite_thresholds`.

**Relevant Code:**
```python
def set_risk_appetite_st(max_financial_loss, max_incidents, max_reputational_impact):
    """Stores the risk appetite thresholds in a dictionary."""
    return {
        'Max Acceptable Financial Loss per Incident': float(max_financial_loss),
        'Max Acceptable Incidents per Period': int(max_incidents),
        'Max Acceptable Reputational Impact Score': float(max_reputational_impact)
    }
```

**Streamlit Integration:**
```python
st.sidebar.header("Step 2: Define Risk Appetite")
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
```

---

### Step 3: Simulating Scenario Outcomes Based on Risk Management Actions

**Business Value:**
This step models the impact of various risk management actions on the likelihood and impact of risk events, allowing users to observe the effect of their decisions. Compliance is evaluated by verifying that the residual impacts are within the predefined risk appetite.

**Technical Implementation:**
The `simulate_scenario_outcome` function will calculate residual likelihood and impact based on the chosen action and its parameters. The function is modified to return a comprehensive dictionary containing both initial and residual impacts, chosen action, and compliance flags.

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

**Relevant Code:**
```python
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
```

**Streamlit Integration:**
```python
st.sidebar.header("Step 3: Simulate Scenario Outcome")

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
        # Store the individual outcome temporarily or directly log it.
        # For simplicity, we directly add it to the log here.
        st.session_state['last_simulated_outcome'] = outcome
        st.success(f"Simulation run for Scenario ID: {selected_scenario_id} with action: {selected_action}")
        st.dataframe(pd.DataFrame([outcome]).set_index('Scenario ID')) # Display the single outcome

else:
    st.sidebar.warning("Please generate synthetic data first to simulate scenarios.")
    st.info("Simulated Scenario Outcome will appear here after running a simulation.")
```

---

### Step 4: Logging Simulation Outcomes for Audit and Governance

**Business Value:**
Maintaining a historical log of simulated risk scenarios and their policy outcomes is vital for compliance, continuous governance improvement, and enabling trend/portfolio analysis. This aligns with good governance practices: tracking and reviewing risk-response effectiveness over time.

**Technical Implementation:**
The `update_simulation_log_st` function appends the result of each simulation to `st.session_state.simulation_log`.

**Relevant Code:**
```python
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
```

**Streamlit Integration:**
```python
if 'last_simulated_outcome' in st.session_state and st.session_state['last_simulated_outcome']:
    st.session_state['simulation_log'] = update_simulation_log_st(
        st.session_state['simulation_log'], st.session_state.pop('last_simulated_outcome')
    )
    # Clear the temporary variable after processing
    # st.session_state['last_simulated_outcome'] = None # No need to clear, pop handles it

st.subheader("Simulation Log")
if not st.session_state['simulation_log'].empty:
    st.dataframe(st.session_state['simulation_log'])
else:
    st.info("Run simulations to see the log here.")
```

---

### Step 5: Calculating Cumulative Impact Over Time

**Business Value:**
Aggregating risk impacts over time offers decision-makers critical insights into policy performance long-term. Tracking cumulative financial losses and incident counts helps identify trends, reassess risk appetites, and adjust mitigation strategies proactively.

**Technical Implementation:**
The `calculate_cumulative_impact` function computes running totals for financial impact and compliant incidents. It operates on a copy of the simulation log to avoid modifying the original DataFrame directly.

**Formula:**
*   Cumulative Financial Impact: $ CumulativeFinancialImpact_t = \sum_{i=1}^{t} ResidualFinancialImpact_i $

**Relevant Code:**
```python
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
```

**Streamlit Integration:**
```python
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
        labels={'Scenario Number': 'Scenario Number', 'Cumulative Financial Impact': 'Cumulative Financial Loss ($)'}
    )
    st.plotly_chart(fig_finance, use_container_width=True)

    # Plot Cumulative Compliant Incidents
    fig_incidents = px.line(
        processed_log,
        x='Scenario Number',
        y='Cumulative Compliant Incidents',
        title='Cumulative Compliant Operational Incidents Over Simulated Scenarios',
        labels={'Scenario Number': 'Scenario Number', 'Cumulative Compliant Incidents': 'Number of Compliant Incidents'}
    )
    st.plotly_chart(fig_incidents, use_container_width=True)
else:
    st.info("Run simulations to visualize cumulative impacts.")
```

---

### Step 6: Aggregating Results to Identify High-Risk Areas

**Business Value:**
Grouping simulation results by risk category and chosen action allows senior management to quickly pinpoint areas with the greatest financial impact, where certain actions are more or less effective, and where risk appetite is most frequently breached. This targeted insight enables efficient resource allocation and focused policy adjustments.

**Technical Implementation:**
The `aggregate_results` function groups the `simulation_log` by `Risk Category` and `Chosen Action` and calculates the sum of `Residual Financial Impact` for each group. The function is modified to return the grouped DataFrame.

**Relevant Code:**
```python
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
```

**Streamlit Integration:**
```python
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
        }
    )
    st.plotly_chart(fig_agg, use_container_width=True)
else:
    st.info("Run simulations and log outcomes to view aggregated results.")
```
