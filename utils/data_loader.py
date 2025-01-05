import pandas as pd
from datetime import datetime, timedelta
import requests
import io
import streamlit as st

def load_nyc_restaurant_data():
    """Load NYC restaurant inspection data from the Open Data API"""
    url = "https://data.cityofnewyork.us/resource/43nn-pn8j.csv"

    # Initialize empty list to store all dataframes
    all_data = []
    offset = 0
    page_size = 1000
    total_fetched = 0

    while True:
        # Set query parameters for pagination
        query_params = {
            '$limit': page_size,
            '$offset': offset,
            '$order': 'inspection_date DESC',
            '$where': 'inspection_date IS NOT NULL'
        }

        # Fetch page of data
        df_page = fetch_data(url, query_params)

        # If page is empty or error occurred, break the loop
        if df_page.empty:
            break

        all_data.append(df_page)
        total_fetched += len(df_page)

        # Update progress message
        st.info(f"Loading restaurants... Retrieved {total_fetched:,} records so far")

        # If we got less than page_size records, we've reached the end
        if len(df_page) < page_size:
            break

        # Increment offset for next page
        offset += page_size

    # If we got no data at all, return empty DataFrame
    if not all_data:
        st.error("No data received from the API")
        return pd.DataFrame()

    # Combine all pages into single DataFrame
    df = pd.concat(all_data, ignore_index=True)

    # Clean and process the combined data
    df['inspection_date'] = pd.to_datetime(df['inspection_date'], errors='coerce')
    df = df.dropna(subset=['latitude', 'longitude'])  # Only drop rows missing coordinates

    # Convert score to numeric, handling missing values
    df['score'] = pd.to_numeric(df['score'], errors='coerce')
    median_score = df['score'].median()
    df['score'] = df['score'].fillna(median_score)

    # Add year column for time-lapse
    df['year'] = df['inspection_date'].dt.year

    # Fill NA values in string columns with empty strings
    string_columns = ['dba', 'building', 'street', 'grade']
    df[string_columns] = df[string_columns].fillna('')

    # Remove duplicate records keeping the latest inspection for each restaurant
    df = df.sort_values('inspection_date', ascending=False).drop_duplicates(subset='camis')

    # Log the final number of unique restaurants
    st.success(f"Successfully loaded {len(df):,} unique restaurants from the API")

    return df

def fetch_data(url, query_params=None):
    """Fetch data from NYC Open Data API with optional query parameters"""
    try:
        # Make API request with query parameters if provided
        response = requests.get(url, params=query_params)
        response.raise_for_status()

        # Read CSV data
        return pd.read_csv(io.StringIO(response.text))

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
        '$limit': 1000  # Increased from 50 to 1000 for more comprehensive search results
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