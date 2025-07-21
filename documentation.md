id: 6871303047cae1aed2172178_documentation
summary: Risk Governance Lab 1 Documentation
feedback link: https://docs.google.com/forms/d/e/1FAIpQLSfWkOK-in_bMMoHSZfcIvAeO58PAH9wrDqcxnJABHaxiDqhSA/viewform?usp=sf_link
environments: Web
status: Published
# Building a Risk Governance Lab with Streamlit

## 1. Understanding the Risk Governance Lab Application
Duration: 00:05:00

This codelab provides a comprehensive guide to a Streamlit application designed as a **Risk Governance Lab**. The application simulates various aspects of risk management within a firm, focusing on how different risk management actions impact a firm's adherence to its predefined risk appetite. For developers, understanding this application provides insights into:

*   **Interactive Data Generation:** How to create synthetic datasets within a Streamlit application, allowing users to control parameters for data variety.
*   **Session State Management:** The critical role of `st.session_state` for persisting data and user inputs across different pages and interactions in a multi-page Streamlit application. This is fundamental for maintaining context and data consistency.
*   **Modular Application Design:** How to structure a larger Streamlit application using separate Python files for different "pages" or functionalities, improving code organization and maintainability.
*   **Simulation and Logic Implementation:** Implementing core business logic, such as risk impact calculations, action-based modifications, and compliance checks, directly within a Streamlit application.
*   **Data Visualization for Analysis:** Leveraging libraries like Plotly Express to create interactive visualizations that transform raw simulation data into actionable insights for decision-making.

<aside class="positive">
<b>Why is this important?</b>
In finance and business, effective risk governance is paramount. This application provides a sandbox environment to:
<ul>
  <li><b>Test Risk Appetite:</b> Evaluate if the defined risk appetite (e.g., maximum financial loss) is appropriate under various scenarios.</li>
  <li><b>Assess Action Effectiveness:</b> Understand how different risk mitigation, transfer, acceptance, or elimination strategies perform.</li>
  <li><b>Improve Decision Making:</b> Provide a data-driven basis for allocating resources for risk management.</li>
  <li><b>Enhance Compliance:</b> Simulate compliance with internal policies and external regulations.</li>
</ul>
</aside>

### Application Architecture Overview

The application is structured into a main `app.py` file and three sub-modules within an `application_pages` directory, each handling a specific part of the risk governance process:

*   **`app.py`**: The entry point. It sets up the main Streamlit page, displays the application title, and uses a sidebar `st.selectbox` to navigate between the different functional pages.
*   **`application_pages/page1.py`**: Handles **Data Generation & Risk Appetite** definition. This is where synthetic risk scenarios are created and the firm's risk tolerance thresholds are set.
*   **`application_pages/page2.py`**: Manages **Scenario Simulation**. Users select a generated scenario, choose a risk management action, and see the simulated outcome, which is then logged.
*   **`application_pages/page3.py`**: Focuses on **Impact Analysis**. It visualizes the cumulative effects of simulated scenarios and aggregates results to identify high-risk areas.

<aside class="positive">
<b>Key Concept: Streamlit's `st.session_state`</b>
Throughout this application, <code>st.session_state</code> is heavily utilized. It's a dictionary-like object that allows you to persist information across reruns of your Streamlit app, and importantly, across different pages when using a multi-page setup. This is crucial for passing data (like generated scenarios or risk appetite thresholds) from one page to another.
</aside>

Here's a high-level conceptual flow:

```
User launches app.py
       |
       V
  Sidebar Navigation
       |
++--+
|      |           |
V      V           V
Page 1           Page 2           Page 3
(Data Gen & RA)  (Scenario Sim)   (Impact Analysis)
       |             |                |
       +-+-+
             |
             V
      st.session_state
  (shared data persistence)
```

## 2. Setting Up the Environment and Running the Application
Duration: 00:02:00

Before diving into the code, let's ensure you have the necessary environment set up to run this Streamlit application.

### Prerequisites

*   Python 3.7+
*   `pip` (Python package installer)

### Installation Steps

1.  **Create a project directory** and navigate into it:
    ```bash
    mkdir risk_governance_lab
    cd risk_governance_lab
    ```

2.  **Create a virtual environment** (recommended for dependency management):
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment**:
    *   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4.  **Install the required libraries**:
    ```bash
    pip install streamlit pandas numpy plotly
    ```

5.  **Create the application files**:

    *   Create `app.py`:
        ```python
        # app.py
        import streamlit as st

        st.set_page_config(page_title="Risk Governance Lab", layout="wide")
        st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
        st.sidebar.divider()
        st.title("Risk Governance Lab 1")
        st.divider()

        st.markdown("""
        This application simulates risk management strategies within a firm's risk appetite.
        It allows users to generate synthetic risk scenarios, define risk appetite thresholds,
        simulate risk management actions, and visualize the impact of these actions.
        """)

        page = st.sidebar.selectbox(
            label="Navigation",
            options=["Data Generation & Risk Appetite", "Scenario Simulation", "Impact Analysis"]
        )

        if page == "Data Generation & Risk Appetite":
            from application_pages.page1 import run_page1
            run_page1()
        elif page == "Scenario Simulation":
            from application_pages.page2 import run_page2
            run_page2()
        elif page == "Impact Analysis":
            from application_pages.page3 import run_page3
            run_page3()
        ```

    *   Create a directory `application_pages`:
        ```bash
        mkdir application_pages
        ```

    *   Create `application_pages/page1.py`:
        ```python
        # application_pages/page1.py
        import streamlit as st
        import pandas as pd
        import numpy as np

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

        def run_page1():
            st.header("Step 1: Generate Synthetic Risk Data")
            st.markdown("""
            Simulating diverse risk events is crucial for testing and optimizing governance policies.
            Generating synthetic data across categories (Strategic, Financial, Operational, Compliance, Reputational)
            creates a safe testbed to evaluate risk responses and appetite settings.
            This aligns with governance best practice: "understand your risk universe" before defining appetite.

            **Formulae for data generation:**
            *   Financial impact per event $ \sim \mathrm{Uniform}(0, 100000) $
            *   Reputational impact per event $ \sim \mathrm{Uniform}(0, 10) $
            *   Operational impact per event $ \sim \mathrm{Uniform}(0, 100) $
            """)

            num_scenarios = st.slider(
                "Number of Scenarios", 5, 500, 50,
                help="Define how many synthetic risk scenarios to generate."
            )
            seed_input = st.text_input(
                "Random Seed (optional)", "",
                help="Enter an integer for reproducibility. Leave empty for random."
            )

            if st.button("Generate Data"):
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
                st.info("Generate synthetic data using the controls above.")

            st.divider()

            st.header("Step 2: Define Risk Appetite")
            st.markdown("""
            Defining numerical risk appetite thresholds is a key activity for the board and senior management.
            These thresholds ensure management actions and decisions are anchored to the organization's capacity,
            supporting transparency and accountability.
            """)

            max_financial_loss = st.number_input(
                "Max Acceptable Financial Loss per Incident ($)",
                min_value=0.0, value=50000.0, step=1000.0,
                help="The maximum financial loss per incident the firm is willing to tolerate."
            )
            max_incidents = st.number_input(
                "Max Acceptable Incidents per Period",
                min_value=0, value=10, step=1,
                help="Sets a cap on operational events per period, enforcing operational discipline."
            )
            max_reputational_impact = st.number_input(
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

    *   Create `application_pages/page2.py`:
        ```python
        # application_pages/page2.py
        import streamlit as st
        import pandas as pd
        import numpy as np

        # Re-initialize session state variables if they don't exist (for direct page access/refresh)
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
            st.header("Step 3: Simulating Scenario Outcomes Based on Risk Management Actions")
            st.markdown("""
            This step models the impact of various risk management actions on the likelihood and impact of risk events,
            allowing users to observe the effect of their decisions. Compliance is evaluated by verifying that the
            residual impacts are within the predefined risk appetite.

            **Formulae for actions:**
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

            if not st.session_state['synthetic_data'].empty:
                scenario_ids = st.session_state['synthetic_data']['Scenario ID'].tolist()
                selected_scenario_id = st.selectbox(
                    "Select Scenario to Simulate", scenario_ids,
                    help="Choose a scenario to apply a risk management action."
                )
                selected_scenario = st.session_state['synthetic_data'][
                    st.session_state['synthetic_data']['Scenario ID'] == selected_scenario_id
                ].iloc[0]

                action_options = ['Accept', 'Mitigate', 'Transfer', 'Eliminate']
                selected_action = st.selectbox(
                    "Choose Risk Management Action", action_options,
                    help="Select a strategy to manage the chosen risk scenario."
                )

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
                    outcome = simulate_scenario_outcome(
                        selected_scenario, selected_action, action_params, st.session_state['risk_appetite_thresholds']
                    )
                    st.session_state['last_simulated_outcome'] = outcome
                    st.success(f"Simulation run for Scenario ID: {selected_scenario_id} with action: {selected_action}")
                    st.dataframe(pd.DataFrame([outcome]).set_index('Scenario ID')) # Display the single outcome

            else:
                st.warning("Please generate synthetic data on the 'Data Generation & Risk Appetite' page first to simulate scenarios.")
                st.info("Simulated Scenario Outcome will appear here after running a simulation.")

            st.divider()

            st.header("Step 4: Logging Simulation Outcomes for Audit and Governance")
            st.markdown("""
            Maintaining a historical log of simulated risk scenarios and their policy outcomes is vital for compliance,
            continuous governance improvement, and enabling trend/portfolio analysis. This aligns with good governance practices:
            tracking and reviewing risk-response effectiveness over time.
            """)

            if 'last_simulated_outcome' in st.session_state and st.session_state['last_simulated_outcome']:
                # Check if the scenario ID already exists in the log to prevent duplicates if user clicks multiple times
                current_scenario_id = st.session_state['last_simulated_outcome']['Scenario ID']
                if current_scenario_id not in st.session_state['simulation_log']['Scenario ID'].values:
                    st.session_state['simulation_log'] = update_simulation_log_st(
                        st.session_state['simulation_log'], st.session_state.pop('last_simulated_outcome')
                    )
                else:
                    # If scenario ID exists, update the existing entry
                    idx_to_update = st.session_state['simulation_log'][st.session_state['simulation_log']['Scenario ID'] == current_scenario_id].index[0]
                    st.session_state['simulation_log'].loc[idx_to_update] = st.session_state.pop('last_simulated_outcome')
                st.success(f"Scenario ID {current_scenario_id} added/updated in simulation log.")
            # Ensure last_simulated_outcome is cleared even if not added to log to prevent re-adding on refresh
            if 'last_simulated_outcome' in st.session_state:
                del st.session_state['last_simulated_outcome']


            st.subheader("Simulation Log")
            if not st.session_state['simulation_log'].empty:
                st.dataframe(st.session_state['simulation_log'])
            else:
                st.info("Run simulations to see the log here.")
        ```

    *   Create `application_pages/page3.py`:
        ```python
        # application_pages/page3.py
        import streamlit as st
        import pandas as pd
        import plotly.express as px

        # Re-initialize session state variables if they don't exist (for direct page access/refresh)
        if 'synthetic_data' not in st.session_state:
            st.session_state['synthetic_data'] = pd.DataFrame()
        if 'risk_appetite_thresholds' not in st.session_state:
            st.session_state['risk_appetiapplication_pages/page3.py:te_thresholds'] = {
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

        def run_page3():
            st.header("Step 5: Calculating Cumulative Impact Over Time")
            st.markdown("""
            Aggregating risk impacts over time offers decision-makers critical insights into policy performance long-term.
            Tracking cumulative financial losses and incident counts helps identify trends, reassess risk appetites,
            and adjust mitigation strategies proactively.

            **Formula:**
            *   Cumulative Financial Impact: $ CumulativeFinancialImpact_t = \sum_{i=1}^{t} ResidualFinancialImpact_i $
            """)

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

            st.divider()

            st.header("Step 6: Aggregating Results to Identify High-Risk Areas")
            st.markdown("""
            Grouping simulation results by risk category and chosen action allows senior management to quickly pinpoint areas
            with the greatest financial impact, where certain actions are more or less effective, and where risk appetite
            is most frequently breached. This targeted insight enables efficient resource allocation and focused policy adjustments.
            """)

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

### Running the Application

Once all files are in place, run the application from your terminal (in the `risk_governance_lab` directory with your virtual environment activated):

```bash
streamlit run app.py
```

This command will open the Streamlit application in your default web browser.

## 3. Page 1: Data Generation & Risk Appetite (application_pages/page1.py)
Duration: 00:07:00

This page serves as the foundation of the simulation, allowing users to define the universe of risk scenarios and the organizational boundaries for risk tolerance.

### 3.1 Generating Synthetic Risk Data

The first section allows users to generate a synthetic dataset of risk scenarios. This is crucial because real-world risk data is often sensitive or scarce. Synthetic data provides a controlled environment for testing and validating risk models and policies without exposing actual sensitive information.

The `generate_synthetic_data` function is at the core of this functionality:

```python
import numpy as np
import pandas as pd

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

**Key Concepts:**
*   **Synthetic Data:** Data that is artificially created rather than being generated by actual events. It's used here to represent diverse risk events for simulation.
*   **Reproducibility:** The `seed` parameter for `np.random.seed()` allows users to generate the exact same dataset multiple times, which is vital for consistent testing and debugging.
*   **Random Distributions:** Impacts are generated using uniform random distributions:
    *   Financial impact: $ \mathrm{Uniform}(0, 100000) $
    *   Reputational impact: $ \mathrm{Uniform}(0, 10) $
    *   Operational impact: $ \mathrm{Uniform}(0, 100) $
    Likelihood is also uniformly distributed between 0 and 1.
*   **`st.session_state['synthetic_data']`**: The generated DataFrame is stored in Streamlit's session state, making it accessible on subsequent pages (Scenario Simulation, Impact Analysis).

### 3.2 Defining Risk Appetite

This section allows the firm to define its tolerance levels for various types of risk. Risk appetite is a strategic declaration from the board, guiding management in everyday decision-making regarding risk-taking.

The `set_risk_appetite_st` function captures these thresholds:

```python
def set_risk_appetite_st(max_financial_loss, max_incidents, max_reputational_impact):
    """Stores the risk appetite thresholds in a dictionary."""
    return {
        'Max Acceptable Financial Loss per Incident': float(max_financial_loss),
        'Max Acceptable Incidents per Period': int(max_incidents),
        'Max Acceptable Reputational Impact Score': float(max_reputational_impact)
    }
```

**Key Concepts:**
*   **Risk Appetite Thresholds:** Numerical values that define the maximum acceptable level of risk. In this application, these include:
    *   `Max Acceptable Financial Loss per Incident`: The monetary loss the firm is willing to bear from a single event.
    *   `Max Acceptable Incidents per Period`: A cap on the number of operational events over a period.
    *   `Max Acceptable Reputational Impact Score`: A score (e.g., out of 10) representing the maximum acceptable damage to the firm's reputation.
*   **Dynamic Updates:** Unlike the data generation which requires a button click, risk appetite thresholds update immediately as the user changes the `st.number_input` values. This is achieved by directly assigning the return value of `set_risk_appetite_st` to `st.session_state['risk_appetite_thresholds']` on every rerun.

<aside class="negative">
<b>Important Note on Session State Initialization:</b>
Notice that all `st.session_state` variables (`synthetic_data`, `risk_appetite_thresholds`, `simulation_log`) are initialized at the top of each page's file (`page1.py`, `page2.py`, `page3.py`). This is a crucial defensive programming practice in Streamlit. If a user navigates directly to a page or refreshes it, these variables might not have been set by a previous page. Initializing them ensures the app doesn't crash due to missing keys in `st.session_state`.
</aside>

## 4. Page 2: Scenario Simulation (application_pages/page2.py)
Duration: 00:10:00

This page is where the core risk management actions are simulated, demonstrating their impact on initial risk levels and evaluating compliance against the defined risk appetite.

### 4.1 Simulating Scenario Outcomes

The `simulate_scenario_outcome` function is the heart of the simulation logic. It takes a specific risk scenario, a chosen risk management action, and its parameters, then calculates the residual likelihood and impacts.

```python
import streamlit as st
import pandas as pd
import numpy as np

# ... (session state initialization as seen in the page2.py code) ...

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

**Formulas and Logic for Actions:**
*   **Accept**: The organization decides to take no action and bear the full consequences of the risk.
    *   No changes to likelihood or impact.
*   **Mitigate**: Actions taken to reduce the likelihood and/or impact of a risk event.
    *   Residual Likelihood = Initial Likelihood $ \times $ (1 - Mitigation Factor (Likelihood Reduction %))
    *   Residual Impact = Initial Impact $ \times $ (1 - Mitigation Factor (Impact Reduction %))
    *   The user controls the `Mitigation Factor` via sliders (0.0 to 1.0).
*   **Transfer**: Shifting the financial burden of a risk to a third party, typically through insurance.
    *   Covered Amount = Initial Financial Impact $ \times $ Insurance Coverage Ratio (%)
    *   Residual Financial Impact = max(0, Initial Financial Impact - Covered Amount - Insurance Deductible)
    *   The deductible is applied *after* the coverage. Other impacts (reputational, operational) are not directly affected by financial transfer.
*   **Eliminate**: Taking steps to remove the risk entirely.
    *   Residual Likelihood = 0
    *   Residual Impact = 0 (for all types: financial, reputational, operational)

**Compliance Checks:**
After calculating the residual impacts, the function checks if these residual values are within the firm's defined risk appetite thresholds.
*   `Financial Compliance`: `residual_financial_impact <= Max Acceptable Financial Loss per Incident`
*   `Reputational Compliance`: `residual_reputational_impact <= Max Acceptable Reputational Impact Score`
*   `Operational Compliance`: `initial_operational_impact <= Max Acceptable Incidents per Period` (Note: This is checked against the *initial* operational impact, implying the firm sets its appetite on the frequency/magnitude of raw operational events rather than post-action residual).

### 4.2 Logging Simulation Outcomes

To support audit, analysis, and continuous improvement, all simulation outcomes are logged historically. The `update_simulation_log_st` function handles adding new or updating existing scenario outcomes to a `pandas.DataFrame` stored in `st.session_state['simulation_log']`.

```python
def update_simulation_log_st(simulation_log_df, scenario_outcome):
    """
    Appends scenario outcome to a historical pandas.DataFrame log.
    Returns the updated DataFrame.
    """
    # ... (error handling and column alignment logic) ...
    new_row_df = pd.DataFrame([scenario_outcome])
    # ... (ensure consistent columns and order) ...
    return pd.concat([simulation_log_df, new_row_df], ignore_index=True)
```

**Key Concepts:**
*   **Audit Trail:** The simulation log serves as an audit trail of decisions and their projected outcomes, essential for governance.
*   **Data Persistence:** The `st.session_state['simulation_log']` ensures that the log persists as the user navigates between pages and performs multiple simulations.
*   **Idempotency (for updates):** The logging mechanism checks if a scenario ID already exists in the log. If it does, it updates the existing entry rather than adding a duplicate. This is important if a user re-simulates the same scenario multiple times.
*   **`st.session_state.pop('last_simulated_outcome')`**: After a simulation is run, the immediate outcome is stored in `st.session_state['last_simulated_outcome']`. After it's processed and added/updated in the `simulation_log`, it's removed (`pop`) to ensure it's not re-added on subsequent page refreshes without a new simulation.

### Workflow on Page 2:
1.  **Select Scenario:** Choose from the scenarios generated on Page 1.
2.  **Choose Action:** Select 'Accept', 'Mitigate', 'Transfer', or 'Eliminate'.
3.  **Set Action Parameters:** Sliders/inputs appear dynamically based on the chosen action.
4.  **Run Simulation:** Clicking the button triggers `simulate_scenario_outcome`. The immediate result is displayed.
5.  **Log Outcome:** The application automatically adds or updates the outcome in the simulation log, which is displayed at the bottom of the page.

## 5. Page 3: Impact Analysis (application_pages/page3.py)
Duration: 00:08:00

This page provides the analytical insights into the simulated risk scenarios, helping users understand the cumulative effects of their decisions and identify broader trends or problematic areas.

### 5.1 Calculating Cumulative Impact Over Time

One of the most important analyses in risk management is understanding the total impact over a series of events. This section calculates and visualizes the cumulative financial loss and the count of compliant operational incidents.

The `calculate_cumulative_impact` function performs these calculations:

```python
import streamlit as st
import pandas as pd
import plotly.express as px

# ... (session state initialization as seen in the page3.py code) ...

def calculate_cumulative_impact(simulation_log):
    """
    Processes the `simulation_log` to calculate cumulative financial impact and
    cumulative operational compliant incidents.
    Returns the modified simulation_log DataFrame.
    """
    if simulation_log.empty:
        return simulation_log.copy()

    df_processed = simulation_log.copy()

    # Convert 'Residual Financial Impact' to numeric, coercing errors
    if 'Residual Financial Impact' in df_processed.columns:
        df_processed['Residual Financial Impact'] = pd.to_numeric(df_processed['Residual Financial Impact'], errors='coerce')
        df_processed['Cumulative Financial Impact'] = df_processed['Residual Financial Impact'].cumsum()
    else:
        df_processed['Cumulative Financial Impact'] = 0

    # Calculate Cumulative Compliant Incidents
    if 'Operational Compliance' in df_processed.columns:
        df_processed['Cumulative Compliant Incidents'] = df_processed['Operational Compliance'].astype(int).cumsum()
    else:
        df_processed['Cumulative Compliant Incidents'] = 0

    return df_processed
```

**Formulas and Concepts:**
*   **Cumulative Financial Impact:** This is a running total of all residual financial impacts from simulated scenarios.
    *   $ CumulativeFinancialImpact_t = \sum_{i=1}^{t} ResidualFinancialImpact_i $
    *   This metric helps identify if the aggregated losses are staying within an acceptable cumulative budget or trending upwards unsustainably.
*   **Cumulative Compliant Incidents:** This tracks how many scenarios resulted in `Operational Compliance` (where the initial operational impact was within the set appetite). While it might seem counter-intuitive to track *compliant* incidents cumulatively, it provides insight into the frequency of "acceptable" events.
*   **`df.cumsum()`:** A `pandas` DataFrame method that calculates the cumulative sum of a series.
*   **Plotly Express:** Used to generate interactive line charts for visualizing these trends over time (represented by scenario number).

### 5.2 Aggregating Results to Identify High-Risk Areas

Beyond cumulative impacts, it's crucial to identify which risk categories or chosen actions lead to the highest overall residual impacts. This aggregation helps pinpoint areas requiring more robust policies or different strategies.

The `aggregate_results` function performs this grouping and summation:

```python
def aggregate_results(simulation_log):
    """
    Groups the `simulation_log` by `Risk Category` and `Chosen Action`.
    Calculates sum of `Residual Financial Impact` for each group.
    Returns the grouped DataFrame.
    """
    if simulation_log.empty:
        return pd.DataFrame()

    df_agg = simulation_log.copy()
    try:
        df_agg['Residual Financial Impact'] = pd.to_numeric(df_agg['Residual Financial Impact'], errors='coerce')
        df_agg.dropna(subset=['Residual Financial Impact'], inplace=True) # Drop rows where conversion failed

        if df_agg.empty:
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

**Key Concepts:**
*   **Grouping and Aggregation:** Using `df.groupby()` and `sum()` to consolidate data by `Risk Category` and `Chosen Action`. This transforms detailed per-scenario data into high-level summaries.
*   **Targeted Insight:** The resulting grouped data, visualized as a bar chart, clearly shows which combinations of risk categories and actions result in the largest total financial impact. This helps management focus their efforts.
*   **Data Cleaning (`dropna`):** The code explicitly drops rows where `Residual Financial Impact` might have become `NaN` during the numeric conversion (`pd.to_numeric(..., errors='coerce')`). This ensures robust aggregation.
*   **Plotly Express:** Used to generate an interactive bar chart that visually compares total residual financial impact across different risk categories and actions.

<aside class="positive">
<b>Governance Implication:</b>
Visualizing aggregated results helps answer critical governance questions such as:
<ul>
  <li>Which risk categories consistently incur the highest residual costs, even after applying actions?</li>
  <li>Are certain risk management actions less effective than others for particular risk types?</li>
  <li>Does the overall risk profile remain within the strategic risk appetite when viewed cumulatively and by category?</li>
</ul>
These insights inform strategic adjustments to risk policies, resource allocation, and even organizational structure.
</aside>
