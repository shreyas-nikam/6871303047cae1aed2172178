id: 6871303047cae1aed2172178_documentation
summary: Risk Governance Lab 1 Documentation
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# QuLab: Risk Governance Lab 1 - A Developer's Guide

## Introduction: Understanding Risk Governance with QuLab
Duration: 00:05:00

<aside class="positive">
This codelab provides a comprehensive guide to **QuLab: Risk Governance Lab 1**, an interactive Streamlit application designed to simulate risk management strategies and visualize their impact within a firm's defined risk appetite.
</aside>

**Why is this application important?**

In today's dynamic business environment, effective risk governance is paramount. Organizations must not only identify potential risks but also formulate robust strategies to manage them, all while adhering to their pre-defined risk appetite. QuLab empowers developers and risk professionals to:

*   **Understand Risk Appetite:** Define and visualize the boundaries of acceptable risk.
*   **Simulate Real-World Scenarios:** Test the effectiveness of different risk management actions (Accept, Mitigate, Transfer, Eliminate) against synthetic risk events.
*   **Evaluate Policy Compliance:** Instantly see if a chosen strategy keeps residual risk within the firm's appetite.
*   **Track Performance Over Time:** Analyze cumulative impacts and identify trends in risk exposure.
*   **Inform Strategic Decisions:** Aggregate results to pinpoint high-risk areas and optimize resource allocation for risk mitigation.

**Core Concepts Explained:**

*   **Risk Appetite:** The total amount and type of risk that an organization is willing to take in order to meet its strategic objectives. This application focuses on quantitative thresholds for financial loss, incident frequency, and reputational impact.
*   **Risk Management Actions:** The strategies employed to address identified risks:
    *   **Accept:** Acknowledge the risk and take no action, absorbing any potential loss.
    *   **Mitigate:** Reduce the likelihood or impact of a risk event.
    *   **Transfer:** Shift the risk (or part of it) to another party, often through insurance.
    *   **Eliminate:** Take steps to completely remove the risk.
*   **Initial vs. Residual Impact:** The impact of a risk before any management action (initial) versus the impact after a management action has been applied (residual).
*   **Compliance:** The state of adhering to the defined risk appetite thresholds.
*   **Cumulative Impact:** The running total of financial losses or compliant incidents over a series of simulated events, providing a long-term view of risk exposure.
*   **Aggregation:** Grouping and summarizing results to identify patterns and areas of concern across different risk categories or actions.

This application is structured into a logical flow of steps, mirroring a typical risk management lifecycle, from data generation to analysis and reporting.

### Application Architecture and Data Flow

The QuLab application follows a modular structure, typical for Streamlit applications, separating the main application logic (`app.py`) from the core functionalities (`application_pages/risk_simulator.py`).

The `risk_simulator.py` script orchestrates the entire simulation process, utilizing Streamlit's session state for persistent data storage across user interactions.

Here's a simplified data flow diagram:

```mermaid
graph TD
    A[User Inputs: Number of Scenarios, Risk Appetite] --> B{Step 1: Generate Synthetic Data}
    B --> C[Scenario Data (DataFrame)]
    C --> D{Step 2: Define Risk Appetite}
    D --> E[Risk Appetite Thresholds (Dict)]
    C & E & F[User Inputs: Selected Scenario, Action, Action Params] --> G{Step 3: Simulate Scenario Outcome}
    G --> H[Scenario Outcome (Dict)]
    H --> I{Step 4: Log Simulation Outcomes}
    I --> J[Simulation Log (DataFrame)]
    J --> K{Step 5: Calculate Cumulative Impact}
    K --> L[Processed Log (DataFrame) for Trends]
    J --> M{Step 6: Aggregate Results}
    M --> N[Aggregated Data (DataFrame)]
    L & N --> O[Visualizations (Plotly Charts)]
```

**Key components and their roles:**

*   `app.py`: The entry point for the Streamlit application. Sets up the page configuration, displays a welcome message, and routes to the `risk_simulator` page.
*   `application_pages/risk_simulator.py`: Contains all the core logic for risk simulation, including:
    *   **Session State Management:** Utilizes `st.session_state` to store and retrieve data across reruns (e.g., `synthetic_data`, `risk_appetite_thresholds`, `simulation_log`).
    *   **Data Generation Function (`generate_synthetic_data`):** Creates simulated risk events.
    *   **Risk Appetite Definition Function (`set_risk_appetite_st`):** Manages user-defined risk tolerance.
    *   **Simulation Function (`simulate_scenario_outcome`):** Applies risk management actions and calculates residual impacts and compliance.
    *   **Logging Function (`update_simulation_log_st`):** Maintains a historical record of all simulations.
    *   **Analysis Functions (`calculate_cumulative_impact`, `aggregate_results`):** Process the logged data for trends and aggregated insights.
    *   **Streamlit UI Elements:** Integrates all functionalities with interactive widgets (sliders, number inputs, selectboxes, buttons) and displays results using dataframes and Plotly charts.

Let's dive into each step!

## Step 1: Generating Synthetic Risk Scenario Data
Duration: 00:07:00

The first crucial step in risk simulation is to have data representing potential risk events. QuLab allows you to generate synthetic risk scenarios, providing a diverse set of events to test your risk management strategies against. This functionality is vital for establishing a safe, reproducible, and comprehensive test environment without relying on sensitive real-world data.

<aside class="positive">
**Business Value:**
Simulating diverse risk events is crucial for testing and optimizing governance policies. Generating synthetic data across categories (Strategic, Financial, Operational, Compliance, Reputational) creates a safe testbed to evaluate risk responses and appetite settings. This aligns with governance best practice: "understand your risk universe" before defining appetite.
</aside>

### Function: `generate_synthetic_data`

The `generate_synthetic_data` function is responsible for creating this dataset.

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

**Understanding the Data Generation:**

*   **Risk Categories:** Scenarios are randomly assigned to one of five predefined risk categories: Strategic, Financial, Operational, Compliance, or Reputational.
*   **Initial Likelihood:** Represents the probability of a risk event occurring, simulated using a uniform random distribution between 0 and 1.
*   **Initial Impact (Financial):** The monetary loss associated with the event, simulated using a uniform random distribution between $0 and $100,000.
    $$ \text{Financial impact per event} \sim \mathrm{Uniform}(0, 100000) $$
*   **Initial Impact (Reputational):** The damage to the firm's reputation, on a scale of 0 to 10, simulated using a uniform random distribution.
    $$ \text{Reputational impact per event} \sim \mathrm{Uniform}(0, 10) $$
*   **Initial Impact (Operational):** The disruption to operations, simulated using a uniform random distribution between 0 and 100.
    $$ \text{Operational impact per event} \sim \mathrm{Uniform}(0, 100) $$
*   **Reproducibility:** The `seed` parameter allows you to set a random seed for reproducible data generation. If the same seed is used, the same set of synthetic scenarios will be generated every time.

### Interacting with the Application (Step 1)

In the Streamlit application, you'll find controls in the sidebar to generate data:

1.  **Number of Scenarios:** Use the slider labeled "Number of Scenarios" to determine how many synthetic risk events you want to generate (between 5 and 500).
2.  **Random Seed (optional):** Enter an integer in the "Random Seed (optional)" text input for reproducible data. Leave it empty for truly random data each time.
3.  **Generate Data Button:** Click the "Generate Data" button to execute the `generate_synthetic_data` function and populate the `st.session_state['synthetic_data']` DataFrame.

```python
# From application_pages/risk_simulator.py (within run_risk_simulator function)
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
```

Once generated, the synthetic data DataFrame will be displayed on the main page under "Synthetic Risk Scenarios". This data will then be available for subsequent simulation steps.

## Step 2: Defining the Firm's Risk Appetite
Duration: 00:05:00

After generating risk scenarios, the next critical step in risk governance is to define the boundaries of acceptable risk. This is where the firm's "risk appetite" comes into play. QuLab allows users to set quantitative thresholds for different types of risk impact.

<aside class="positive">
**Business Value:**
Defining numerical risk appetite thresholds is a key activity for the board and senior management. These thresholds ensure management actions and decisions are anchored to the organization's capacity, supporting transparency and accountability.
</aside>

### Function: `set_risk_appetite_st`

The `set_risk_appetite_st` function stores the user-defined risk appetite thresholds in a dictionary.

```python
def set_risk_appetite_st(max_financial_loss, max_incidents, max_reputational_impact):
    """Stores the risk appetite thresholds in a dictionary."""
    return {
        'Max Acceptable Financial Loss per Incident': float(max_financial_loss),
        'Max Acceptable Incidents per Period': int(max_incidents),
        'Max Acceptable Reputational Impact Score': float(max_reputational_impact)
    }
```

**Understanding Risk Appetite Thresholds:**

*   **Max Acceptable Financial Loss per Incident:** This threshold defines the maximum monetary loss the firm is willing to incur from a single risk incident. Exceeding this value indicates a breach of financial risk appetite.
*   **Max Acceptable Incidents per Period:** This sets a limit on the number of operational events or incidents that the firm is willing to tolerate within a given period. It helps enforce operational discipline and highlights excessive operational risk.
*   **Max Acceptable Reputational Impact Score:** This numerical score (typically on a scale, here 0-10) limits the damage to the firm's public standing or brand reputation. A higher score means more significant negative reputational impact.

### Interacting with the Application (Step 2)

In the Streamlit application, you'll find number input widgets in the sidebar under "Step 2: Define Risk Appetite" to set these thresholds:

1.  **Max Acceptable Financial Loss per Incident ($):** Define the maximum financial loss tolerated per event.
2.  **Max Acceptable Incidents per Period:** Set the maximum number of incidents.
3.  **Max Acceptable Reputational Impact Score:** Define the maximum reputational impact score tolerated.

```python
# From application_pages/risk_simulator.py (within run_risk_simulator function)
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
```

The application immediately updates and displays the "Current Risk Appetite Thresholds" on the main page as you adjust the inputs. These defined thresholds will be used in the next step to evaluate the compliance of simulated risk outcomes.

## Step 3: Simulating Scenario Outcomes Based on Risk Management Actions
Duration: 00:10:00

This step is the core of the risk simulation. Here, you apply various risk management actions to a chosen synthetic scenario and observe their effect on the initial likelihood and impact. The application then evaluates if the residual (remaining) impacts are within the firm's defined risk appetite.

<aside class="positive">
**Business Value:**
This step models the impact of various risk management actions on the likelihood and impact of risk events, allowing users to observe the effect of their decisions. Compliance is evaluated by verifying that the residual impacts are within the predefined risk appetite. This provides a practical way to understand how different strategies reduce risk exposure and contribute to meeting governance objectives.
</aside>

### Function: `simulate_scenario_outcome`

The `simulate_scenario_outcome` function takes a specific risk scenario, a chosen action, action-specific parameters, and the defined risk appetite thresholds as input. It then calculates the residual likelihood and impacts and performs compliance checks.

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

**Risk Management Action Logic and Formulas:**

*   **Accept:** No changes occur. The residual impacts and likelihood remain the same as the initial values.
*   **Mitigate:** This action reduces both the likelihood and various impacts by specified factors.
    *   Residual Likelihood = Initial Likelihood $\times$ (1 - Mitigation Factor (Likelihood Reduction %))
    *   Residual Impact = Initial Impact $\times$ (1 - Mitigation Factor (Impact Reduction %))
*   **Transfer:** Primarily applies to financial impact, simulating insurance coverage.
    *   Covered Amount = Initial Financial Impact $\times$ Insurance Coverage Ratio (%)
    *   Residual Financial Impact = max(0, Initial Financial Impact - Covered Amount) - Insurance Deductible
    *   **Note:** The deductible is applied *after* the coverage. The `max(0, ...)` ensures the residual impact does not go negative.
*   **Eliminate:** This action aims to completely remove the risk.
    *   Residual Likelihood = 0
    *   Residual Impact = 0 (for all types: Financial, Reputational, Operational)

**Compliance Checks:**

After calculating the residual impacts, the function checks for compliance against the risk appetite thresholds defined in Step 2:

*   **Financial Compliance:** `Residual Financial Impact <= Max Acceptable Financial Loss per Incident`
*   **Operational Compliance:** `Initial Operational Impact <= Max Acceptable Incidents per Period` (Note: As per the application's design, operational compliance is checked against the *initial* operational impact, indicating if the *initial severity* of the operational event itself is within a tolerable incident threshold, not necessarily its residual impact post-action).
*   **Reputational Compliance:** `Residual Reputational Impact <= Max Acceptable Reputational Impact Score`

### Interacting with the Application (Step 3)

In the Streamlit application, you'll find controls in the sidebar under "Step 3: Simulate Scenario Outcome":

1.  **Select Scenario to Simulate:** Choose a `Scenario ID` from the dropdown. The details of the selected scenario will be displayed.
2.  **Choose Risk Management Action:** Select one of 'Accept', 'Mitigate', 'Transfer', or 'Eliminate'.
3.  **Action-Specific Parameters:** Depending on the chosen action, additional sliders or number inputs will appear in the sidebar:
    *   **Mitigate:** "Impact Reduction (%)" and "Likelihood Reduction (%)" sliders.
    *   **Transfer:** "Insurance Deductible ($)" and "Insurance Coverage Ratio (%)" inputs.
4.  **Run Simulation Button:** Click "Run Simulation" to execute the `simulate_scenario_outcome` function for the selected scenario and action.

```python
# From application_pages/risk_simulator.py (within run_risk_simulator function)
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
        st.session_state['last_simulated_outcome'] = outcome # Store for logging in next step
        st.success(f"Simulation run for Scenario ID: {selected_scenario_id} with action: {selected_action}")
        st.subheader("Simulated Scenario Outcome")
        st.dataframe(pd.DataFrame([outcome]).set_index('Scenario ID')) # Display the single outcome

else:
    st.sidebar.warning("Please generate synthetic data first to simulate scenarios.")
    st.info("Simulated Scenario Outcome will appear here after running a simulation.")
```

After a simulation is run, the "Simulated Scenario Outcome" table on the main page will update to show the initial and residual values, along with the compliance status for Financial, Operational, and Reputational aspects. The outcome is also temporarily stored in `st.session_state['last_simulated_outcome']` for the next logging step.

## Step 4: Logging Simulation Outcomes for Audit and Governance
Duration: 00:05:00

After each simulation, it's crucial to record the outcome for historical tracking, auditing, and future analysis. This logging step ensures that all decisions and their resulting impacts are preserved, providing a comprehensive audit trail for risk governance.

<aside class="positive">
**Business Value:**
Maintaining a historical log of simulated risk scenarios and their policy outcomes is vital for compliance, continuous governance improvement, and enabling trend/portfolio analysis. This aligns with good governance practices: tracking and reviewing risk-response effectiveness over time.
</aside>

### Function: `update_simulation_log_st`

The `update_simulation_log_st` function is responsible for appending the results of each simulation to a persistent DataFrame stored in Streamlit's session state.

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

**How it works:**

1.  **Retrieving Last Outcome:** The application retrieves the `last_simulated_outcome` (a dictionary) that was stored in `st.session_state` during Step 3.
2.  **Appending to Log:** This dictionary is converted into a new row DataFrame. The `update_simulation_log_st` function then concatenates this new row with the existing `simulation_log` DataFrame.
3.  **Persistence:** The `simulation_log` DataFrame is stored in `st.session_state['simulation_log']`, ensuring that it persists even when Streamlit reruns the script due to user interactions. This allows you to build a cumulative history of all simulations performed during a session.

### Interacting with the Application (Step 4)

There's no direct user interaction needed for this step beyond running simulations in Step 3. The logging happens automatically.

```python
# From application_pages/risk_simulator.py (within run_risk_simulator function)
st.markdown("""
### Step 4: Logging Simulation Outcomes for Audit and Governance
...
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
```

The "Simulation Log" table on the main page will display the complete history of all simulated scenarios, their chosen actions, initial and residual impacts, and their compliance status. This log is the foundation for the subsequent analytical steps.

## Step 5: Calculating Cumulative Impact Over Time
Duration: 00:10:00

Understanding the impact of risk events in isolation is important, but true risk governance requires insights into the aggregated effect of multiple events over time. This step allows you to visualize cumulative financial losses and the total number of compliant operational incidents, providing a macro view of your firm's risk exposure and policy effectiveness.

<aside class="positive">
**Business Value:**
Aggregating risk impacts over time offers decision-makers critical insights into policy performance long-term. Tracking cumulative financial losses and incident counts helps identify trends, reassess risk appetites, and adjust mitigation strategies proactively. This continuous monitoring is a cornerstone of effective governance.
</aside>

### Function: `calculate_cumulative_impact`

The `calculate_cumulative_impact` function processes the `simulation_log` to add new columns for cumulative financial impact and cumulative compliant operational incidents.

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

**Formulas and Concepts:**

*   **Cumulative Financial Impact:** This is a running sum of the `Residual Financial Impact` from each simulated scenario.
    $$ \text{CumulativeFinancialImpact}_t = \sum_{i=1}^{t} \text{ResidualFinancialImpact}_i $$
    where $t$ is the current scenario in the log. This helps visualize the total financial exposure over time as more risk events occur and are managed.
*   **Cumulative Compliant Incidents:** This is a running count of how many operational incidents have been *compliant* with the firm's risk appetite thresholds. Since `Operational Compliance` is a boolean (True/False), converting it to an integer (True=1, False=0) and then taking a cumulative sum effectively counts the compliant incidents.

### Interacting with the Application (Step 5)

Similar to logging, this step runs automatically whenever the `simulation_log` is updated. The results are presented through interactive Plotly charts.

```python
# From application_pages/risk_simulator.py (within run_risk_simulator function)
st.markdown("""
### Step 5: Calculating Cumulative Impact Over Time
...
""")
st.subheader("Cumulative Impact Trends")
processed_log = calculate_cumulative_impact(st.session_state['simulation_log'])

if not processed_log.empty and 'Cumulative Financial Impact' in processed_log.columns and 'Cumulative Compliant Incidents' in processed_log.columns:
    processed_log['Scenario Number'] = processed_log.index + 1 # For plotting sequence

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
```

**Visualizations:**

*   **Cumulative Financial Impact Over Simulated Scenarios:** A line chart showing the running total of residual financial losses. This graph helps identify if the cumulative financial exposure remains within acceptable limits over time.
*   **Cumulative Compliant Operational Incidents Over Simulated Scenarios:** A line chart tracking the number of operational events that met the firm's compliance criteria. This helps assess the effectiveness of operational risk controls.
*   **Initial vs. Residual Financial Impact per Scenario:** A scatter plot comparing the financial impact before and after a risk management action.
    *   Each point represents a simulated scenario.
    *   The `color` indicates whether the scenario's residual financial impact was `Financial Compliance` (True/False).
    *   A red dotted `hline` represents the `Max Acceptable Financial Loss` threshold. Points below this line are compliant; points above it are not. This visual provides immediate feedback on the efficacy of chosen actions in meeting financial risk appetite.

These visualizations provide critical insights for risk managers, allowing them to spot trends, assess overall risk posture, and identify potential issues that might be masked by looking at individual incidents.

## Step 6: Aggregating Results to Identify High-Risk Areas
Duration: 00:07:00

The final step in the QuLab simulation provides aggregated insights from all the logged scenarios. By grouping results by risk category and the chosen risk management action, you can quickly identify which areas consistently pose the greatest residual financial impact and which actions are most or least effective.

<aside class="positive">
**Business Value:**
Grouping simulation results by risk category and chosen action allows senior management to quickly pinpoint areas with the greatest financial impact, where certain actions are more or less effective, and where risk appetite is most frequently breached. This targeted insight enables efficient resource allocation and focused policy adjustments, contributing to a more mature risk governance framework.
</aside>

### Function: `aggregate_results`

The `aggregate_results` function processes the `simulation_log` to group data and sum the `Residual Financial Impact`.

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

**How it works:**

1.  **Grouping:** The function groups the entire `simulation_log` DataFrame by two key dimensions: `Risk Category` and `Chosen Action`.
2.  **Aggregation:** For each unique combination of `Risk Category` and `Chosen Action`, it calculates the sum of `Residual Financial Impact`. This provides a total financial cost associated with a specific action within a given risk category across all simulations.
3.  **Insights:** This aggregated view helps answer questions like:
    *   Which risk category consistently results in the highest residual financial impact, regardless of the action taken?
    *   Within a specific risk category, which risk management action leads to the lowest or highest total residual financial impact?
    *   Are there certain actions that are generally less effective (resulting in higher aggregated residual impact) across multiple risk categories?

### Interacting with the Application (Step 6)

This step automatically displays results after you have run simulations and logged outcomes.

```python
# From application_pages/risk_simulator.py (within run_risk_simulator function)
st.markdown("""
### Step 6: Aggregating Results to Identify High-Risk Areas
...
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
```

**Visualization:**

*   **Aggregated Residual Financial Impact by Risk Category and Action:** A grouped bar chart visually represents the summed `Residual Financial Impact` for each combination of `Risk Category` and `Chosen Action`.
    *   The x-axis represents the `Risk Category`.
    *   The y-axis represents the `Total Residual Financial Impact`.
    *   Different colored bars within each category indicate the `Chosen Action`, allowing for direct comparison of action effectiveness within a risk type.

This aggregated view is critical for strategic decision-making in risk governance. It enables senior management to allocate resources effectively, refine risk appetite statements, and adjust risk management policies based on the holistic impact of various strategies across the entire risk landscape. By identifying patterns and concentrations of residual risk, organizations can continuously mature their risk governance framework.
