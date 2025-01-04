import streamlit as st
from utils.map_utils import create_heatmap
import plotly.express as px
import pandas as pd

def render_map_view(df):
    """Render the main map view with controls and insights"""
    st.subheader("🗺️ Restaurant Safety Explorer")

    # Neighborhood selector
    all_neighborhoods = sorted(df['boro'].unique())
    selected_neighborhood = st.selectbox(
        "Select a neighborhood to explore",
        ["All Neighborhoods"] + list(all_neighborhoods)
    )

    # Filter data for selected neighborhood
    if selected_neighborhood != "All Neighborhoods":
        neighborhood_data = df[df['boro'] == selected_neighborhood]
        st.markdown(f"### {selected_neighborhood} Safety Overview")
    else:
        neighborhood_data = df
        st.markdown("### Citywide Safety Overview")

    # Display key metrics for the selected area
    col1, col2, col3 = st.columns(3)

    with col1:
        total_restaurants = len(neighborhood_data['camis'].unique())
        st.metric(
            "Total Restaurants",
            f"{total_restaurants:,}",
            help="Number of unique restaurants inspected"
        )

    with col2:
        grade_a_percent = (len(neighborhood_data[neighborhood_data['grade'] == 'A']) / len(neighborhood_data) * 100)
        st.metric(
            "Grade A Restaurants",
            f"{grade_a_percent:.1f}%",
            help="Percentage of restaurants with Grade A"
        )

    with col3:
        avg_score = neighborhood_data['score'].mean()
        st.metric(
            "Average Score",
            f"{avg_score:.1f}",
            help="Lower is better"
        )

    # Grade distribution
    st.markdown("### Grade Distribution")
    grade_dist = neighborhood_data['grade'].value_counts()
    fig_grades = px.pie(
        values=grade_dist.values,
        names=grade_dist.index,
        title="Restaurant Grades",
        color_discrete_sequence=px.colors.sequential.Oranges,
        hole=0.4
    )
    fig_grades.update_traces(textinfo='percent+label')
    st.plotly_chart(fig_grades, use_container_width=True)

    # Time analysis
    st.markdown("### Inspection Trends")
    col1, col2 = st.columns(2)

    with col1:
        # Day of week analysis
        neighborhood_data['day_of_week'] = pd.to_datetime(neighborhood_data['inspection_date']).dt.day_name()
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily_counts = neighborhood_data['day_of_week'].value_counts().reindex(day_order)

        fig_daily = px.bar(
            x=daily_counts.index,
            y=daily_counts.values,
            title="Inspections by Day",
            labels={'x': 'Day', 'y': 'Number of Inspections'},
            color=daily_counts.values,
            color_continuous_scale='Oranges'
        )
        fig_daily.update_layout(showlegend=False)
        st.plotly_chart(fig_daily, use_container_width=True)

    with col2:
        # Monthly analysis
        neighborhood_data['month'] = pd.to_datetime(neighborhood_data['inspection_date']).dt.strftime('%B')
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                      'July', 'August', 'September', 'October', 'November', 'December']
        monthly_counts = neighborhood_data['month'].value_counts().reindex(month_order)

        fig_monthly = px.bar(
            x=monthly_counts.index,
            y=monthly_counts.values,
            title="Inspections by Month",
            labels={'x': 'Month', 'y': 'Number of Inspections'},
            color=monthly_counts.values,
            color_continuous_scale='Oranges'
        )
        fig_monthly.update_layout(showlegend=False)
        st.plotly_chart(fig_monthly, use_container_width=True)

    # Year selector for time-lapse
    years = sorted(df['year'].unique())
    selected_year = st.select_slider(
        "Select Year",
        options=years,
        value=years[-1]
    )

    # Filter data for selected year and neighborhood
    year_data = neighborhood_data[neighborhood_data['year'] == selected_year]

    # Create and display heatmap
    st.markdown("### Safety Score Heatmap")
    fig = create_heatmap(year_data)
    st.plotly_chart(fig, use_container_width=True)

    # Common violations table
    if selected_neighborhood != "All Neighborhoods":
        st.markdown("### Common Violations")
        violations = neighborhood_data.groupby('violation_code')['violation_description'].first().reset_index()
        violations['count'] = neighborhood_data.groupby('violation_code').size().values
        violations = violations.sort_values('count', ascending=False).head(5)

        st.dataframe(
            violations,
            column_config={
                "violation_code": "Code",
                "violation_description": "Description",
                "count": st.column_config.NumberColumn(
                    "Frequency",
                    help="Number of times this violation was recorded",
                )
            },
            hide_index=True,
        )