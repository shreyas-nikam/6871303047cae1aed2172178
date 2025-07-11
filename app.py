
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
In this lab, we present the **Risk Appetite & Governance Simulator**, an interactive Streamlit application designed for corporate governance professionals, risk practitioners, and finance students.

**Purpose and Objectives:**
The primary purpose of this tool is to demonstrate how predefined risk appetite boundaries influence a firm's ability to manage various risk exposures. It also illustrates how different governance and policy choices dynamically shape an organization's risk profile in real-time.

**Key Objectives:**
*   Enable users to define and quantify risk appetite thresholds across financial, operational, and reputational dimensions.
*   Allow users to simulate risk events and apply various risk management strategies (Accept, Mitigate, Transfer, Eliminate).
*   Provide a compliance dashboard to visualize actual risk exposure against defined risk appetite boundaries.
*   Display cumulative impact trends of losses and incidents over time under different governance setups.
*   Facilitate aggregated policy analysis to compare the effectiveness of different risk management approaches across various risk categories.

Through this simulator, users can explore:
1.  **How to define a "risk universe"** by generating diverse synthetic risk events.
2.  **The critical role of risk appetite** in setting boundaries for acceptable risk exposure.
3.  **The real-time impact of risk management actions** on an organization's risk profile and compliance status.
4.  **The importance of logging and aggregating simulation outcomes** for continuous governance improvement and strategic decision-making.

Navigate through the pages using the sidebar to explore each step of the risk governance process.
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

page = st.sidebar.selectbox(label="Navigation", options=["Data Generation & Risk Appetite", "Scenario Simulation & Logging", "Cumulative Analysis & Aggregation"])

if page == "Data Generation & Risk Appetite":
    from application_pages.page1 import run_page1
    run_page1()
elif page == "Scenario Simulation & Logging":
    from application_pages.page2 import run_page2
    run_page2()
elif page == "Cumulative Analysis & Aggregation":
    from application_pages.page3 import run_page3
    run_page3()
