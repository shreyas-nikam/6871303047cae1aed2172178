
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

def set_risk_appetite_st(max_financial_loss, max_incidents, max_reputational_impact):
    """Stores the risk appetite thresholds in a dictionary."""
    return {
        'Max Acceptable Financial Loss per Incident': float(max_financial_loss),
        'Max Acceptable Incidents per Period': int(max_incidents),
        'Max Acceptable Reputational Impact Score': float(max_reputational_impact)
    }

def run_page1():
    st.header("Risk Data Generation & Appetite Definition")

    st.markdown("""
    ### Step 1: Generating Synthetic Risk Scenario Data

    **Business Value:**
    Simulating diverse risk events is crucial for testing and optimizing governance policies. Generating synthetic data across categories (Strategic, Financial, Operational, Compliance, Reputational) creates a safe testbed to evaluate risk responses and appetite settings. This aligns with governance best practice: "understand your risk universe" before defining appetite.

    **Formulae:**
    *   Financial impact per event $ \sim \mathrm{Uniform}(0, 100000) $
    *   Reputational impact per event $ \sim \mathrm{Uniform}(0, 10) $
    *   Operational impact per event $ \sim \mathrm{Uniform}(0, 100) $
    """)

    st.subheader("Generate Synthetic Risk Data")
    num_scenarios = st.slider("Number of Scenarios", 5, 500, 50, help="Define how many synthetic risk scenarios to generate.")
    seed_input = st.text_input("Random Seed (optional)", "", help="Enter an integer for reproducibility. Leave empty for random.")

    if st.button("Generate Data"):
        try:
            seed = int(seed_input) if seed_input else None
            st.session_state['synthetic_data'] = generate_synthetic_data(num_scenarios, seed=seed)
            st.success(f"Generated {num_scenarios} synthetic risk scenarios.")
        except ValueError:
            st.error("Please enter a valid integer for the random seed.")

    st.markdown("""
    **Synthetic Risk Scenarios Table:**
    The table below displays the generated synthetic risk scenario data. Each row represents a unique potential risk event with its initial likelihood and estimated impacts across financial, reputational, and operational dimensions. This data forms the basis for our simulations.
    """)
    if not st.session_state['synthetic_data'].empty:
        st.dataframe(st.session_state['synthetic_data'], use_container_width=True)
    else:
        st.info("Generate synthetic data using the controls above.")

    st.markdown("""
    ---
    ### Step 2: Defining the Firm's Risk Appetite

    **Business Value:**
    Defining numerical risk appetite thresholds is a key activity for the board and senior management. These thresholds ensure management actions and decisions are anchored to the organization's capacity, supporting transparency and accountability.
    """)

    st.subheader("Define Risk Appetite Thresholds")
    max_financial_loss = st.number_input(
        "Max Acceptable Financial Loss per Incident ($)",
        min_value=0.0, value=st.session_state['risk_appetite_thresholds'].get('Max Acceptable Financial Loss per Incident', 50000.0), step=1000.0,
        help="The maximum financial loss per incident the firm is willing to tolerate."
    )
    max_incidents = st.number_input(
        "Max Acceptable Operational Incidents per Period",
        min_value=0, value=st.session_state['risk_appetite_thresholds'].get('Max Acceptable Incidents per Period', 10), step=1,
        help="Sets a cap on operational events per period, enforcing operational discipline."
    )
    max_reputational_impact = st.number_input(
        "Max Acceptable Reputational Impact Score",
        min_value=0.0, max_value=10.0, value=st.session_state['risk_appetite_thresholds'].get('Max Acceptable Reputational Impact Score', 5.0), step=0.1,
        help="Limits damage to the firm's public standing (score out of 10)."
    )

    # Update risk appetite thresholds immediately as inputs change
    st.session_state['risk_appetite_thresholds'] = set_risk_appetite_st(
        max_financial_loss, max_incidents, max_reputational_impact
    )

    st.markdown("""
    **Current Risk Appetite Thresholds:**
    These are the boundaries within which the firm aims to operate. Understanding and adhering to these limits is critical for sound risk governance.
    """)
    st.write(f"**Max Financial Loss:** ${st.session_state['risk_appetite_thresholds']['Max Acceptable Financial Loss per Incident']:,}")
    st.write(f"**Max Operational Incidents:** {st.session_state['risk_appetite_thresholds']['Max Acceptable Incidents per Period']}")
    st.write(f"**Max Reputational Impact:** {st.session_state['risk_appetite_thresholds']['Max Acceptable Reputational Impact Score']:.1f}")
