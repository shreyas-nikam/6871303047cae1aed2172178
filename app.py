
import streamlit as st

st.set_page_config(page_title="QuLab", layout="wide")

st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()

st.title("QuLab: Risk Appetite & Governance Simulator")
st.divider()

st.markdown("""
In this lab, we explore the critical interplay between an organization's **risk appetite** and its **risk management strategies**. This interactive simulator is designed for corporate governance professionals, risk practitioners, and finance students to understand how predefined risk boundaries influence the firm's response to various risk exposures (financial, operational, reputational) and how different governance choices dynamically shape its overall risk profile.

**Key Concepts:**
*   **Risk Appetite:** The amount and type of risk that an organization is willing to take in order to meet its strategic objectives.
*   **Risk Management Actions:** Strategies such as Accept, Mitigate, Transfer, or Eliminate, used to respond to identified risks.
*   **Compliance:** Verifying that residual risk impacts remain within the defined risk appetite thresholds.

Through a series of steps, you will:
1.  **Generate Synthetic Risk Data:** Create a diverse set of hypothetical risk scenarios.
2.  **Define Risk Appetite:** Set the firm's maximum acceptable thresholds for financial loss, operational incidents, and reputational impact.
3.  **Simulate Scenario Outcomes:** Apply different risk management actions to individual scenarios and observe their effects on initial versus residual impacts.
4.  **Log Simulations:** Maintain a historical record of all simulated events and their outcomes.
5.  **Calculate Cumulative Impact:** Analyze trends of total financial losses and compliant incidents over time.
6.  **Aggregate Results:** Identify high-risk areas and compare the effectiveness of different risk management actions across categories.

This tool aims to provide a practical understanding of how robust risk governance frameworks lead to more informed decision-making and a resilient organization.
""")

# Your code starts here
st.sidebar.markdown("### Navigation")
page = st.sidebar.selectbox(label="Go to", options=["Data Generation", "Risk Appetite & Simulation", "Cumulative & Aggregated Insights"])

if page == "Data Generation":
    from application_pages.page1_data_generation import run_page1
    run_page1()
elif page == "Risk Appetite & Simulation":
    from application_pages.page2_risk_appetite_simulation import run_page2
    run_page2()
elif page == "Cumulative & Aggregated Insights":
    from application_pages.page3_cumulative_aggregated import run_page3
    run_page3()
# Your code ends
