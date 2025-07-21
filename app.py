
import streamlit as st

st.set_page_config(page_title="Risk Governance Lab", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("QuLab: Risk Governance Lab 1")
st.divider()

st.markdown("""
This lab provides an interactive simulation environment to explore risk appetite and governance strategies within a firm.
Users can generate synthetic risk scenarios, define risk appetite thresholds, simulate the outcomes of risk management actions,
and analyze cumulative impacts over time. This tool is designed for corporate governance professionals, risk practitioners,
and finance students to understand how risk appetite boundaries influence a firm's ability to manage risk exposures.

**Key Features:**
*   **Risk Scenario Generation:** Create diverse risk scenarios with varying financial, operational, and reputational impacts.
*   **Risk Appetite Definition:** Set thresholds for maximum acceptable financial loss, operational incidents, and reputational impact.
*   **Scenario Simulation:** Simulate risk management actions (Accept, Mitigate, Transfer, Eliminate) and observe their impact on risk outcomes.
*   **Compliance Dashboard:** Visualize real-time risk exposure against defined risk appetite boundaries.
*   **Aggregated Policy Analysis:** Compare the effectiveness of different risk management approaches across various risk categories.
""")

page = st.sidebar.selectbox(
    label="Navigation",
    options=["Data Generation & Risk Appetite", "Scenario Simulation", "Analysis & Insights"]
)

if page == "Data Generation & Risk Appetite":
    from application_pages.page1 import run_page1
    run_page1()
elif page == "Scenario Simulation":
    from application_pages.page2 import run_page2
    run_page2()
elif page == "Analysis & Insights":
    from application_pages.page3 import run_page3
    run_page3()

