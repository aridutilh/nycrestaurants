import plotly.express as px
import plotly.graph_objects as go

def create_heatmap(df):
    """Create a heatmap of restaurant safety scores"""
    fig = px.density_mapbox(
        df,
        lat='latitude',
        lon='longitude',
        z='score',
        radius=20,
        center=dict(lat=40.7128, lon=-74.0060),
        zoom=10,
        mapbox_style="carto-positron",
        color_continuous_scale="Reds",
        opacity=0.7,
        title="NYC Restaurant Safety Scores Heatmap"
    )
    
    fig.update_layout(
        mapbox_style="carto-positron",
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
