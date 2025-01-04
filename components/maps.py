import streamlit as st
from utils.map_utils import create_heatmap
import plotly.express as px
import pandas as pd

def render_map_view(df):
    """Render the main map view with controls and insights"""
    st.subheader("🗺️ Restaurant Safety by Neighborhood")

    # Add neighborhood insights
    col1, col2 = st.columns(2)

    with col1:
        # Neighborhood rankings
        boro_stats = df.groupby('boro').agg({
            'score': ['mean', 'count'],
            'grade': lambda x: (x == 'A').mean() * 100
        }).round(1)

        boro_stats.columns = ['Avg Score', 'Inspections', 'Grade A %']
        boro_stats = boro_stats.sort_values('Avg Score')

        st.markdown("### Neighborhood Rankings")
        st.dataframe(
            boro_stats,
            column_config={
                "Avg Score": st.column_config.NumberColumn(
                    help="Lower is better",
                    format="%.1f"
                ),
                "Grade A %": st.column_config.NumberColumn(
                    help="Percentage of Grade A restaurants",
                    format="%.1f%%"
                ),
            },
            hide_index=False,
        )

    with col2:
        # Time analysis
        st.markdown("### Inspection Trends")

        # Get inspection counts by day of week
        df['day_of_week'] = pd.to_datetime(df['inspection_date']).dt.day_name()
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily_counts = df['day_of_week'].value_counts().reindex(day_order)

        fig = px.bar(
            x=daily_counts.index, 
            y=daily_counts.values,
            title="Inspections by Day of Week",
            labels={'x': 'Day', 'y': 'Number of Inspections'},
            color=daily_counts.values,
            color_continuous_scale='Oranges'
        )
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    # Year selector for time-lapse
    years = sorted(df['year'].unique())
    selected_year = st.select_slider(
        "Select Year",
        options=years,
        value=years[-1]
    )

    # Filter data for selected year
    year_data = df[df['year'] == selected_year]

    # Create and display heatmap
    fig = create_heatmap(year_data)
    st.plotly_chart(fig, use_container_width=True)

    # Display statistics
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Inspections",
            len(year_data),
            f"{len(year_data) - len(df[df['year'] == selected_year-1])}"
        )

    with col2:
        avg_score = year_data['score'].mean()
        prev_avg = df[df['year'] == selected_year-1]['score'].mean()
        st.metric(
            "Average Score",
            f"{avg_score:.1f}",
            f"{avg_score - prev_avg:.1f}"
        )

    with col3:
        grade_a = len(year_data[year_data['grade'] == 'A'])
        prev_grade_a = len(df[(df['year'] == selected_year-1) & (df['grade'] == 'A')])
        st.metric(
            "Grade A Restaurants",
            grade_a,
            f"{grade_a - prev_grade_a}"
        )