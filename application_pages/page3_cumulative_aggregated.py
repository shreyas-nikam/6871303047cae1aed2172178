
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

def calculate_cumulative_impact(simulation_log):
    """
    Processes the `simulation_log` to calculate cumulative financial impact and
    cumulative operational compliant incidents.
    Returns the modified simulation_log DataFrame.
    """
    if simulation_log.empty:
        return simulation_log.copy() # Return an empty copy if no data

    df_processed = simulation_log.copy() # Work on a copy

    # Convert 'Residual Financial Impact' to numeric, coercing errors
    if 'Residual Financial Impact' in df_processed.columns:
        df_processed['Residual Financial Impact'] = pd.to_numeric(df_processed['Residual Financial Impact'], errors='coerce')
        df_processed['Cumulative Financial Impact'] = df_processed['Residual Financial Impact'].cumsum()
    else:
        df_processed['Cumulative Financial Impact'] = 0 # Add column even if source is missing

    # Calculate Cumulative Compliant Incidents
    if 'Operational Compliance' in df_processed.columns:
        # Summing True (1) and False (0) for compliance count
        df_processed['Cumulative Compliant Incidents'] = df_processed['Operational Compliance'].astype(int).cumsum()
    else:
        df_processed['Cumulative Compliant Incidents'] = 0 # Add column even if source is missing

    return df_processed

def aggregate_results(simulation_log):
    """
    Groups the `simulation_log` by `Risk Category` and `Chosen Action`.
    Calculates sum of `Residual Financial Impact` for each group.
    Returns the grouped DataFrame.
    """
    if simulation_log.empty:
        return pd.DataFrame() # Return empty DataFrame if log is empty

    df_agg = simulation_log.copy()
    try:
        # Ensure 'Residual Financial Impact' is numeric before grouping
        df_agg['Residual Financial Impact'] = pd.to_numeric(df_agg['Residual Financial Impact'], errors='coerce')
        
        # Drop rows where 'Residual Financial Impact' became NaN due to coercion errors
        df_agg.dropna(subset=['Residual Financial Impact'], inplace=True)

        if df_agg.empty: # Check if DataFrame is empty after dropping NaNs
            return pd.DataFrame()

        # Group by 'Risk Category' and 'Chosen Action' and sum 'Residual Financial Impact'
        grouped = df_agg.groupby(['Risk Category', 'Chosen Action'])['Residual Financial Impact'].sum().reset_index()
        return grouped
    except KeyError as e:
        st.error(f"Missing expected column for aggregation: {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"An error occurred during aggregation: {e}")
        return pd.DataFrame()

def run_page3():
    st.markdown("""
    ## Step 5: Calculating Cumulative Impact Over Time

    **Business Value:**
    Aggregating risk impacts over time offers decision-makers critical insights into policy performance long-term. Tracking cumulative financial losses and incident counts helps identify trends, reassess risk appetites, and adjust mitigation strategies proactively.

    **Formula:**
    *   Cumulative Financial Impact: $$ CumulativeFinancialImpact_t = \sum_{i=1}^{t} ResidualFinancialImpact_i $$
    """)

    st.header("Cumulative Impact Trends")
    processed_log = calculate_cumulative_impact(st.session_state['simulation_log'])

    if not processed_log.empty and 'Cumulative Financial Impact' in processed_log.columns and 'Cumulative Compliant Incidents' in processed_log.columns:
        # Ensure Scenario ID is treated as a continuous variable for plotting trends
        processed_log['Scenario Number'] = processed_log.index + 1

        # Plot Cumulative Financial Impact
        fig_finance = px.line(
            processed_log,
            x='Scenario Number',
            y='Cumulative Financial Impact',
            title='Cumulative Financial Impact Over Simulated Scenarios',
            labels={'Scenario Number': 'Scenario Number', 'Cumulative Financial Impact': 'Cumulative Financial Loss ($)'},
            hover_data=['Scenario ID', 'Residual Financial Impact', 'Financial Compliance']
        )
        st.plotly_chart(fig_finance, use_container_width=True)

        # Plot Cumulative Compliant Incidents
        fig_incidents = px.line(
            processed_log,
            x='Scenario Number',
            y='Cumulative Compliant Incidents',
            title='Cumulative Compliant Operational Incidents Over Simulated Scenarios',
            labels={'Scenario Number': 'Scenario Number', 'Cumulative Compliant Incidents': 'Number of Compliant Incidents'},
            hover_data=['Scenario ID', 'Operational Compliance']
        )
        st.plotly_chart(fig_incidents, use_container_width=True)
    else:
        st.info("Run simulations to visualize cumulative impacts. Go to 'Risk Appetite & Simulation' page to run simulations.")

    st.markdown("""
    ## Step 6: Aggregating Results to Identify High-Risk Areas

    **Business Value:**
    Grouping simulation results by risk category and chosen action allows senior management to quickly pinpoint areas with the greatest financial impact, where certain actions are more or less effective, and where risk appetite is most frequently breached. This targeted insight enables efficient resource allocation and focused policy adjustments.
    """)

    st.header("Aggregated Risk Insights")
    aggregated_df = aggregate_results(st.session_state['simulation_log'])

    if not aggregated_df.empty:
        st.dataframe(aggregated_df, use_container_width=True)

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
            },
            hover_data=['Risk Category', 'Chosen Action', 'Residual Financial Impact']
        )
        st.plotly_chart(fig_agg, use_container_width=True)
    else:
        st.info("Run simulations and log outcomes to view aggregated results. Go to 'Risk Appetite & Simulation' page to run simulations.")
