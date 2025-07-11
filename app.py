
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="QuLab - Risk Governance Lab 1", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab: Risk Governance Lab 1")
st.divider()
st.markdown("""
Welcome to the **Risk Governance Lab 1**!

This interactive simulator is designed for corporate governance professionals, risk practitioners, and finance students. It demonstrates how **risk appetite boundaries** influence a firm's ability to manage various risk exposures, and how different governance and policy choices dynamically shape an organization's risk profile in real-time.

### Key Objectives:
*   **Define and Quantify Risk Appetite:** Set thresholds across financial, operational, and reputational dimensions.
*   **Simulate Risk Events:** Apply various risk management strategies (Accept, Mitigate, Transfer, Eliminate) to synthetic risk scenarios.
*   **Visualize Compliance:** Observe actual risk exposure against defined risk appetite boundaries through a compliance dashboard.
*   **Analyze Cumulative Trends:** Track the cumulative impact of losses and incidents over time under different governance setups.
*   **Compare Effectiveness:** Facilitate aggregated policy analysis to compare the effectiveness of different risk management approaches across various risk categories.

Navigate through the sections using the sidebar to explore different aspects of risk governance simulation.
""")

# Initialize session state variables if they don't exist
if 'synthetic_data' not in st.session_state:
    st.session_state['synthetic_data'] = pd.DataFrame()
if 'risk_appetite_thresholds' not in st.session_state:
    st.session_state['risk_appetite_thresholds'] = {
        'Max Acceptable Financial Loss per Incident': 50000.0,
        'Max Acceptable Incidents per Period': 10,
        'Max Acceptable Reputational Impact Score': 5.0
    }
if 'simulation_log' not in st.session_state:
    st.session_state['simulation_log'] = pd.DataFrame(columns=[
        'Scenario ID', 'Risk Category', 'Chosen Action',
        'Initial Likelihood', 'Initial Financial Impact', 'Initial Reputational Impact', 'Initial Operational Impact',
        'Residual Likelihood', 'Residual Financial Impact', 'Residual Reputational Impact', 'Residual Operational Impact',
        'Financial Compliance', 'Operational Compliance', 'Reputational Compliance'
    ])
# This temporary variable holds the last simulation outcome before it's appended to the log
if 'last_simulated_outcome' not in st.session_state:
    st.session_state['last_simulated_outcome'] = None


st.sidebar.divider()
page = st.sidebar.selectbox(label="Navigation", options=["Data Generation & Risk Appetite", "Scenario Simulation & Logging", "Cumulative & Aggregated Insights"])

if page == "Data Generation & Risk Appetite":
    from application_pages.page1 import run_page1
    run_page1()
elif page == "Scenario Simulation & Logging":
    from application_pages.page2 import run_page2
    run_page2()
elif page == "Cumulative & Aggregated Insights":
    from application_pages.page3 import run_page3
    run_page3()
