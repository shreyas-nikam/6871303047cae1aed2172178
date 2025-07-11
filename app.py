
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="QuLab", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab")
st.divider()
st.markdown("""
In this lab, we explore the dynamic interaction between a firm's risk appetite and its risk management strategies. This interactive simulator is designed for corporate governance professionals, risk practitioners, and finance students to understand how defined risk appetite boundaries influence a firm's ability to manage various risk exposures.

The application demonstrates how different governance and policy choices dynamically shape an organization's risk profile in real-time. You will be able to:
*   Define and quantify risk appetite thresholds across financial, operational, and reputational dimensions.
*   Simulate risk events and apply various risk management strategies (Accept, Mitigate, Transfer, Eliminate).
*   Visualize actual risk exposure against defined risk appetite boundaries using a compliance dashboard.
*   Display cumulative impact trends of losses and incidents over time under different governance setups.
*   Perform aggregated policy analysis to compare the effectiveness of different risk management approaches across various risk categories.

**Navigation:** Use the sidebar on the left to navigate between different steps of the simulation. Each page guides you through a specific aspect of risk governance.
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

# Your code starts here
page = st.sidebar.selectbox(label="Navigation", options=["Step 1: Data Generation", "Step 2: Risk Appetite", "Step 3-6: Simulation & Analysis"])

if page == "Step 1: Data Generation":
    from application_pages.page1_data_generation import run_page1
    run_page1()
elif page == "Step 2: Risk Appetite":
    from application_pages.page2_risk_appetite import run_page2
    run_page2()
elif page == "Step 3-6: Simulation & Analysis":
    from application_pages.page3_6_simulation_analysis import run_page3_6
    run_page3_6()
# Your code ends
