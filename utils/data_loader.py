import pandas as pd
from datetime import datetime, timedelta
import requests
import io

def load_nyc_restaurant_data():
    """Load NYC restaurant inspection data from the Open Data API"""
    url = "https://data.cityofnewyork.us/resource/43nn-pn8j.csv"
    
    try:
        # Read data directly from API
        df = pd.read_csv(url)
        
        # Clean and process the data
        df['inspection_date'] = pd.to_datetime(df['inspection_date'])
        df = df.dropna(subset=['latitude', 'longitude', 'score'])
        
        # Convert score to numeric, replacing missing values with median
        df['score'] = pd.to_numeric(df['score'], errors='coerce')
        df['score'].fillna(df['score'].median(), inplace=True)
        
        # Add year column for time-lapse
        df['year'] = df['inspection_date'].dt.year
        
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

def filter_data_by_year(df, year):
    """Filter dataset by specific year"""
    return df[df['year'] == year]

def search_restaurants(df, query):
    """Search restaurants by name or address"""
    query = query.lower()
    mask = (df['dba'].str.lower().str.contains(query, na=False) |
            df['building'].str.lower().str.contains(query, na=False) |
            df['street'].str.lower().str.contains(query, na=False))
    return df[mask].drop_duplicates(subset=['camis'])
