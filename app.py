
import streamlit as st

st.set_page_config(page_title="QuLab", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab: Risk Appetite & Governance Simulator")
st.divider()
st.markdown("""
In this lab, we present an interactive simulator for corporate governance professionals, risk practitioners, and finance students. Its primary purpose is to demonstrate how **risk appetite boundaries** influence a firm's ability to manage various risk exposures, and how different **governance and policy choices** dynamically shape an organization's risk profile in real-time.

**Key Objectives:**
*   Enable users to define and quantify risk appetite thresholds across financial, operational, and reputational dimensions.
*   Allow users to simulate risk events and apply various risk management strategies (Accept, Mitigate, Transfer, Eliminate).
*   Provide a compliance dashboard to visualize actual risk exposure against defined risk appetite boundaries.
*   Display cumulative impact trends of losses and incidents over time under different governance setups.
*   Facilitate aggregated policy analysis to compare the effectiveness of different risk management approaches across various risk categories.

Navigate through the sections using the sidebar to explore different aspects of risk governance simulation.
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
# For temporary storage of the last simulation outcome before adding to log
if 'last_simulated_outcome' not in st.session_state:
    st.session_state['last_simulated_outcome'] = None

# Your code starts here
import pandas as pd
import numpy as np
import plotly.express as px

page = st.sidebar.selectbox(label="Navigation", options=["Data Generation & Risk Appetite", "Scenario Simulation & Logging", "Cumulative & Aggregated Analysis"])

if page == "Data Generation & Risk Appetite":
    from application_pages.page1 import run_page1
    run_page1()
elif page == "Scenario Simulation & Logging":
    from application_pages.page2 import run_page2
    run_page2()
elif page == "Cumulative & Aggregated Analysis":
    from application_pages.page3 import run_page3
    run_page3()
# Your code ends
