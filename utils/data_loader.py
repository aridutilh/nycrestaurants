import pandas as pd
from datetime import datetime, timedelta
import requests
import io
import streamlit as st

def load_nyc_restaurant_data():
    """Load NYC restaurant inspection data from the Open Data API"""
    url = "https://data.cityofnewyork.us/resource/43nn-pn8j.csv"
    return fetch_data(url)

def fetch_data(url, query_params=None):
    """Fetch data from NYC Open Data API with optional query parameters"""
    try:
        # Make API request with query parameters if provided
        response = requests.get(url, params=query_params)
        response.raise_for_status()

        # Read CSV data
        df = pd.read_csv(io.StringIO(response.text))

        if df.empty:
            return pd.DataFrame()

        # Clean and process the data
        df['inspection_date'] = pd.to_datetime(df['inspection_date'], errors='coerce')
        df = df.dropna(subset=['latitude', 'longitude', 'score'])

        # Convert score to numeric, handling missing values
        df['score'] = pd.to_numeric(df['score'], errors='coerce')
        median_score = df['score'].median()
        df['score'] = df['score'].fillna(median_score)

        # Add year column for time-lapse
        df['year'] = df['inspection_date'].dt.year

        # Fill NA values in string columns with empty strings
        string_columns = ['dba', 'building', 'street', 'grade']
        df[string_columns] = df[string_columns].fillna('')

        return df

    except requests.RequestException as e:
        st.error(f"Error fetching data from API: {str(e)}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return pd.DataFrame()

def search_restaurants(df, query):
    """Search restaurants using direct API query"""
    if not query:
        return pd.DataFrame()

    # API endpoint for searching
    base_url = "https://data.cityofnewyork.us/resource/43nn-pn8j.csv"

    # Construct API query parameters
    query = query.lower().strip()
    query_params = {
        '$where': f"lower(dba) like '%{query}%' OR lower(building) like '%{query}%' OR lower(street) like '%{query}%'",
        '$order': 'inspection_date DESC',
        '$limit': 50
    }

    # Fetch fresh data from API with search parameters
    results = fetch_data(base_url, query_params)

    if not results.empty:
        # Get unique restaurants (latest inspection for each)
        results = results.drop_duplicates(subset=['camis'])

    return results

def filter_data_by_year(df, year):
    """Filter dataset by specific year"""
    return df[df['year'] == year]