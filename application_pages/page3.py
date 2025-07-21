
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

def calculate_cumulative_impact(simulation_log):
    \"\"\"
    Processes the `simulation_log` to calculate cumulative financial impact and
    cumulative operational compliant incidents.
    Returns the modified simulation_log DataFrame.
    \"\"\"
    if simulation_log.empty:
        return simulation_log.copy()

    df_processed = simulation_log.copy()

    if 'Residual Financial Impact' in df_processed.columns:
        df_processed['Residual Financial Impact'] = pd.to_numeric(df_processed['Residual Financial Impact'], errors='coerce')
        df_processed['Cumulative Financial Impact'] = df_processed['Residual Financial Impact'].cumsum()
    else:
        df_processed['Cumulative Financial Impact'] = 0

    if 'Operational Compliance' in df_processed.columns:
        df_processed['Cumulative Compliant Incidents'] = df_processed['Operational Compliance'].astype(int).cumsum()
    else:
        df_processed['Cumulative Compliant Incidents'] = 0

    return df_processed

def aggregate_results(simulation_log):
    \"\"\"
    Groups the `simulation_log` by `Risk Category` and `Chosen Action`.
    Calculates sum of `Residual Financial Impact` for each group.
    Returns the grouped DataFrame.
    \"\"\"
    if simulation_log.empty:
        return pd.DataFrame()

    df_agg = simulation_log.copy()
    try:
        df_agg['Residual Financial Impact'] = pd.to_numeric(df_agg['Residual Financial Impact'], errors='coerce')
        df_agg.dropna(subset=['Residual Financial Impact'], inplace=True)

        if df_agg.empty:
            return pd.DataFrame()

        grouped = df_agg.groupby(['Risk Category', 'Chosen Action'])['Residual Financial Impact'].sum().reset_index()
        return grouped
    except KeyError as e:
        st.error(f"Missing expected column for aggregation: {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"An error occurred during aggregation: {e}")
        return pd.DataFrame()

def run_page3():
    st.header("Analysis & Insights")

    st.subheader("Cumulative Impact Trends")
    if 'simulation_log' in st.session_state:
        processed_log = calculate_cumulative_impact(st.session_state['simulation_log'])

        if not processed_log.empty and 'Cumulative Financial Impact' in processed_log.columns and 'Cumulative Compliant Incidents' in processed_log.columns:
            processed_log['Scenario Number'] = processed_log.index + 1

            fig_finance = px.line(
                processed_log,
                x='Scenario Number',
                y='Cumulative Financial Impact',
                title='Cumulative Financial Impact Over Simulated Scenarios',
                labels={'Scenario Number': 'Scenario Number', 'Cumulative Financial Impact': 'Cumulative Financial Loss ($)'}
            )
            st.plotly_chart(fig_finance, use_container_width=True)

            fig_incidents = px.line(
                processed_log,
                x='Scenario Number',
                y='Cumulative Compliant Incidents',
                title='Cumulative Compliant Operational Incidents Over Simulated Scenarios',
                labels={'Scenario Number': 'Scenario Number', 'Cumulative Compliant Incidents': 'Number of Compliant Incidents'}
            )
            st.plotly_chart(fig_incidents, use_container_width=True)
        else:
            st.info("Run simulations to visualize cumulative impacts.")

        st.subheader("Aggregated Risk Insights")
        aggregated_df = aggregate_results(st.session_state['simulation_log'])

        if not aggregated_df.empty:
            st.dataframe(aggregated_df)

            fig_agg = px.bar(
                aggregated_df,
                x='Risk Category',
                y='Residual Financial Impact',
                color='Chosen Action',
                barmode='group',
                title='Aggregated Residual Financial Impact by Risk Category and Action',
                labels={
                    'Risk Category': 'Risk Category',
                    'Residual Financial Impact': 'Total Residual Financial Impact ($)',
                    'Chosen Action': 'Action Taken'
                }
            )
            st.plotly_chart(fig_agg, use_container_width=True)
        else:
            st.info("Run simulations and log outcomes to view aggregated results.")
    else:
        st.info("Please run simulations first to generate data for analysis.")

