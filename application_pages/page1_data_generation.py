
import streamlit as st
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

def run_page1():
    st.markdown("""
    ## Step 1: Generating Synthetic Risk Scenario Data

    **Business Value:**
    Simulating diverse risk events is crucial for testing and optimizing governance policies. Generating synthetic data across categories (Strategic, Financial, Operational, Compliance, Reputational) creates a safe testbed to evaluate risk responses and appetite settings. This aligns with governance best practice: "understand your risk universe" before defining appetite.

    **Formulae:**
    *   Financial impact per event $$\sim \mathrm{Uniform}(0, 100000)$$
    *   Reputational impact per event $$\sim \mathrm{Uniform}(0, 10)$$
    *   Operational impact per event $$\sim \mathrm{Uniform}(0, 100)$$
    """)

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
    if 'last_simulated_outcome' not in st.session_state:
        st.session_state['last_simulated_outcome'] = None

    st.header("Generate Synthetic Risk Data")
    num_scenarios = st.slider("Number of Scenarios", 5, 500, 50, help="Define how many synthetic risk scenarios to generate.")
    seed_input = st.text_input("Random Seed (optional)", "", help="Enter an integer for reproducibility. Leave empty for random.")

    if st.button("Generate Data"):
        try:
            seed = int(seed_input) if seed_input else None
            st.session_state['synthetic_data'] = generate_synthetic_data(num_scenarios, seed=seed)
            st.success(f"Generated {num_scenarios} synthetic risk scenarios.")
        except ValueError:
            st.error("Please enter a valid integer for the random seed.")

    st.subheader("Synthetic Risk Scenarios Table")
    if not st.session_state['synthetic_data'].empty:
        st.dataframe(st.session_state['synthetic_data'], use_container_width=True)
    else:
        st.info("Generate synthetic data using the controls above.")
