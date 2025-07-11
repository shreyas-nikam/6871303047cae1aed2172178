
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
    st.header("Cumulative & Aggregated Risk Insights")

    st.markdown("""
    ### Step 5: Calculating Cumulative Impact Over Time

    **Business Value:**
    Aggregating risk impacts over time offers decision-makers critical insights into policy performance long-term. Tracking cumulative financial losses and incident counts helps identify trends, reassess risk appetites, and adjust mitigation strategies proactively.

    **Formula:**
    *   Cumulative Financial Impact: $ CumulativeFinancialImpact_t = \sum_{i=1}^{t} ResidualFinancialImpact_i $
    """)

    st.subheader("Cumulative Impact Trends")
    processed_log = calculate_cumulative_impact(st.session_state['simulation_log'])

    if not processed_log.empty and 'Cumulative Financial Impact' in processed_log.columns and 'Cumulative Compliant Incidents' in processed_log.columns:
        # Ensure Scenario ID is treated as a continuous variable for plotting trends
        processed_log['Scenario Number'] = processed_log.index + 1

        st.markdown("""
        **Cumulative Financial Impact Over Simulated Scenarios:**
        This chart tracks the total financial losses incurred as more scenarios are simulated, showcasing the accumulating financial exposure.
        """)
        # Plot Cumulative Financial Impact
        fig_finance = px.line(
            processed_log,
            x='Scenario Number',
            y='Cumulative Financial Impact',
            title='Cumulative Financial Impact Over Simulated Scenarios',
            labels={'Scenario Number': 'Scenario Number', 'Cumulative Financial Impact': 'Cumulative Financial Loss ($)'},
            hover_data={
                'Scenario Number': True,
                'Cumulative Financial Impact': ':.2f',
                'Residual Financial Impact': ':.2f',
                'Financial Compliance': True
            }
        )
        st.plotly_chart(fig_finance, use_container_width=True)

        st.markdown("""
        **Cumulative Compliant Operational Incidents Over Simulated Scenarios:**
        This chart shows how many operational incidents remained within the defined risk appetite boundaries over time, indicating the effectiveness of operational risk controls.
        """)
        # Plot Cumulative Compliant Incidents
        fig_incidents = px.line(
            processed_log,
            x='Scenario Number',
            y='Cumulative Compliant Incidents',
            title='Cumulative Compliant Operational Incidents Over Simulated Scenarios',
            labels={'Scenario Number': 'Scenario Number', 'Cumulative Compliant Incidents': 'Number of Compliant Incidents'},
            hover_data={
                'Scenario Number': True,
                'Cumulative Compliant Incidents': True,
                'Operational Compliance': True
            }
        )
        st.plotly_chart(fig_incidents, use_container_width=True)
    else:
        st.info("Run simulations and log outcomes on the 'Scenario Simulation & Logging' page to visualize cumulative impacts.")

    st.markdown("""
    ---
    ### Relationship Plot: Initial vs. Residual Impact

    This scatter plot visualizes the effectiveness of risk management actions by comparing the initial financial impact of scenarios against their residual financial impact after a chosen action. Points are colored based on financial compliance, and a horizontal line indicates the maximum acceptable financial loss.
    """)
    if not st.session_state['simulation_log'].empty:
        df_impact = st.session_state['simulation_log'].copy()
        df_impact['Financial Compliance Text'] = df_impact['Financial Compliance'].apply(lambda x: 'In Compliance' if x else 'Out of Compliance')
        
        fig_scatter = px.scatter(
            df_impact,
            x='Initial Financial Impact',
            y='Residual Financial Impact',
            color='Financial Compliance Text',
            title='Initial vs. Residual Financial Impact per Scenario',
            labels={
                'Initial Financial Impact': 'Initial Financial Impact ($)',
                'Residual Financial Impact': 'Residual Financial Impact ($)',
                'Financial Compliance Text': 'Compliance Status'
            },
            hover_data={
                'Scenario ID': True,
                'Risk Category': True,
                'Chosen Action': True,
                'Initial Financial Impact': ':.2f',
                'Residual Financial Impact': ':.2f',
                'Financial Compliance Text': True
            }
        )
        # Add the Max Acceptable Financial Loss as a horizontal line
        max_loss_threshold = st.session_state['risk_appetite_thresholds']['Max Acceptable Financial Loss per Incident']
        fig_scatter.add_hline(y=max_loss_threshold, line_dash="dash", line_color="red", 
                              annotation_text=f"Max Acceptable Loss: ${max_loss_threshold:,.0f}", 
                              annotation_position="top right")
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.info("Run simulations to see the Initial vs. Residual Impact plot.")


    st.markdown("""
    ---
    ### Step 6: Aggregating Results to Identify High-Risk Areas

    **Business Value:**
    Grouping simulation results by risk category and chosen action allows senior management to quickly pinpoint areas with the greatest financial impact, where certain actions are more or less effective, and where risk appetite is most frequently breached. This targeted insight enables efficient resource allocation and focused policy adjustments.
    """)

    st.subheader("Aggregated Risk Insights")
    aggregated_df = aggregate_results(st.session_state['simulation_log'])

    if not aggregated_df.empty:
        st.markdown("""
        **Aggregated Residual Financial Impact Table:**
        This table summarizes the total residual financial impact for each combination of risk category and the action taken, providing a clear view of where risk remains after mitigation efforts.
        """)
        st.dataframe(aggregated_df, use_container_width=True)

        st.markdown("""
        **Aggregated Residual Financial Impact by Risk Category and Action:**
        This bar chart visually compares the total residual financial impact across different risk categories and the risk management actions applied. This helps in understanding which actions are most effective for specific risk types and identifying areas requiring further policy refinement.
        """)
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
            hover_data={
                'Risk Category': True,
                'Chosen Action': True,
                'Residual Financial Impact': ':.2f'
            }
        )
        st.plotly_chart(fig_agg, use_container_width=True)
    else:
        st.info("Run simulations and log outcomes on the 'Scenario Simulation & Logging' page to view aggregated results.")
