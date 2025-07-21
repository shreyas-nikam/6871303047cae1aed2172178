import streamlit as st

st.set_page_config(page_title="Risk Governance Lab", layout="wide")
st.sidebar.image("https://www.quantuniversity.com/assets/img/logo5.jpg")
st.sidebar.divider()
st.title("Risk Governance Lab 1")
st.divider()

st.markdown("""
This application simulates risk management strategies within a firm's risk appetite.
It allows users to generate synthetic risk scenarios, define risk appetite thresholds,
simulate risk management actions, and visualize the impact of these actions.
""")

page = st.sidebar.selectbox(
    label="Navigation",
    options=["Data Generation & Risk Appetite", "Scenario Simulation", "Impact Analysis"]
)

if page == "Data Generation & Risk Appetite":
    from application_pages.page1 import run_page1
    run_page1()
elif page == "Scenario Simulation":
    from application_pages.page2 import run_page2
    run_page2()
elif page == "Impact Analysis":
    from application_pages.page3 import run_page3
    run_page3()