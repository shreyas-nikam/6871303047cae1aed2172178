
import streamlit as st

st.set_page_config(page_title="QuLab", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab: Risk Governance Lab 1")
st.divider()
st.markdown("""
This interactive application simulates risk management strategies and visualizes their impact within a firm's defined risk appetite.
It allows users to define risk appetite thresholds, simulate risk events, and apply various risk management actions.

The application is structured as follows:

-   **Step 1: Data Generation:** Generate synthetic risk scenario data.
-   **Step 2: Risk Appetite Definition:** Define the firm's risk appetite thresholds.
-   **Step 3: Scenario Outcome Simulation:** Simulate scenario outcomes based on risk management actions.
-   **Step 4: Logging Simulation Outcomes:** Log simulation outcomes for audit and governance.
-   **Step 5: Cumulative Impact Over Time:** Calculate cumulative impact over time.
-   **Step 6: Aggregating Results:** Aggregate results to identify high-risk areas.
""")

page = st.sidebar.selectbox(
    label="Navigation",
    options=["Risk Scenario Simulator"]
)

if page == "Risk Scenario Simulator":
    from application_pages.risk_simulator import run_risk_simulator
    run_risk_simulator()
