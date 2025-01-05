import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_heatmap(df):
    """Create a heatmap of restaurant safety scores with neighborhood-specific scaling"""
    if df.empty:
        return go.Figure()

    # Create base figure
    fig = go.Figure()

    # Process each neighborhood separately
    for neighborhood in df['boro'].unique():
        neighborhood_data = df[df['boro'] == neighborhood]

        # Skip if no data for this neighborhood
        if neighborhood_data.empty:
            continue

        # Normalize scores within this neighborhood
        min_score = neighborhood_data['score'].min()
        max_score = neighborhood_data['score'].max()
        normalized_scores = (neighborhood_data['score'] - min_score) / (max_score - min_score)

        # Add trace for this neighborhood
        fig.add_trace(
            go.Densitymapbox(
                lat=neighborhood_data['latitude'],
                lon=neighborhood_data['longitude'],
                z=normalized_scores,  # Use normalized scores for coloring
                radius=20,
                colorscale="Reds",
                showscale=False,  # Hide individual scales
                name=neighborhood,
                hoverinfo="text",  # Show only custom text on hover
                hovertext=[
                    f"{name}<br>Score: {score}" 
                    for name, score in zip(neighborhood_data['dba'], neighborhood_data['score'])
                ],
            )
        )

    # Update layout
    fig.update_layout(
        mapbox=dict(
            style="carto-positron",
            center=dict(lat=40.7128, lon=-74.0060),
            zoom=10
        ),
        showlegend=True,
        legend_title_text="Neighborhoods",
        margin={"r":0,"t":0,"l":0,"b":0},
        height=600
    )

    return fig

def create_restaurant_map(row):
    """Create a map for a single restaurant"""
    fig = go.Figure(
        go.Scattermapbox(
            lat=[row['latitude']],
            lon=[row['longitude']],
            mode='markers',
            marker=go.scattermapbox.Marker(size=14, color='#D73502'),
            text=[row['dba']],
        )
    )

    fig.update_layout(
        mapbox=dict(
            style="carto-positron",
            center=dict(lat=row['latitude'], lon=row['longitude']),
            zoom=15
        ),
        margin={"r":0,"t":0,"l":0,"b":0},
        height=400
    )

    return fig