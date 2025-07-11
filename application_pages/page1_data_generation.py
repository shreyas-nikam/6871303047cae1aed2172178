
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
    st.header("Step 1: Generate Synthetic Risk Scenario Data")
    st.markdown("""
    **Business Value:**
    Simulating diverse risk events is crucial for testing and optimizing governance policies. Generating synthetic data across categories (Strategic, Financial, Operational, Compliance, Reputational) creates a safe testbed to evaluate risk responses and appetite settings. This aligns with governance best practice: "understand your risk universe" before defining appetite.

    **Formulae:**
    *   Financial impact per event $\sim \mathrm{Uniform}(0, 100000)$
    *   Reputational impact per event $\sim \mathrm{Uniform}(0, 10)$
    *   Operational impact per event $\sim \mathrm{Uniform}(0, 100)$
    """)

    st.subheader("Configuration")
    num_scenarios = st.slider(
        "Number of Scenarios",
        5, 500, 50,
        help="Define how many synthetic risk scenarios to generate. More scenarios provide a richer dataset for analysis."
    )
    seed_input = st.text_input(
        "Random Seed (optional)",
        "",
        help="Enter an integer for reproducible data generation. Leave empty for new random data each time."
    )

    if st.button("Generate Data"):
        try:
            seed = int(seed_input) if seed_input else None
            st.session_state['synthetic_data'] = generate_synthetic_data(num_scenarios, seed=seed)
            st.success(f"Generated {num_scenarios} synthetic risk scenarios. You can now proceed to Step 2 or 3-6.")
        except ValueError:
            st.error("Please enter a valid integer for the random seed.")

    st.subheader("Generated Risk Scenarios Preview")
    if not st.session_state['synthetic_data'].empty:
        st.dataframe(st.session_state['synthetic_data'])
        st.info("This table shows a preview of the generated synthetic risk events. Each row represents a unique scenario with its initial likelihood and various impact metrics.")
    else:
        st.info("Generate synthetic data using the controls above to populate this table.")
