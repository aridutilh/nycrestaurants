import pandas as pd
from datetime import datetime, timedelta
import requests
import io
import streamlit as st
from utils.cache_manager import (
    is_cache_valid,
    load_from_cache,
    save_to_cache,
    get_cache_metadata
)

def load_nyc_restaurant_data():
    """Load NYC restaurant inspection data from cache or API"""
    # Check if we have valid cached data
    if is_cache_valid():
        cached_data = load_from_cache()
        if cached_data is not None:
            metadata = get_cache_metadata()
            return cached_data

    # Initialize empty list to store all dataframes
    all_data = []
    offset = 0
    page_size = 1000
    total_fetched = 0

    url = "https://data.cityofnewyork.us/resource/43nn-pn8j.csv"
    st.session_state.is_loading = True

    try:
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

            # If we got less than page_size records, we've reached the end
            if len(df_page) < page_size:
                break

            # Increment offset for next page
            offset += page_size

        # If we got no data at all, try loading from cache as fallback
        if not all_data:
            cached_data = load_from_cache()
            if cached_data is not None:
                st.warning("Failed to fetch fresh data, using cached data instead")
                return cached_data
            st.error("No data received from the API and no cache available")
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

        # Save the processed data to cache
        save_to_cache(df)

        return df
    finally:
        st.session_state.is_loading = False

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
    """Search restaurants using loaded data with improved error handling"""
    try:
        if df is None or df.empty:
            st.warning("No restaurant data available for search.")
            return pd.DataFrame()

        if not query:
            return pd.DataFrame()

        # Clean and normalize the search query
        query = query.lower().strip()

        # Handle special characters in search
        query = query.replace("'", "''")  # Escape single quotes

        # Search only in restaurant name (dba column)
        try:
            name_mask = df['dba'].str.lower().str.contains(query, na=False)
            results = df[name_mask].head(1000)  # Limit to 1000 results for performance
            return results.sort_values('inspection_date', ascending=False)

        except Exception as e:
            st.warning(f"Error searching restaurant names: {str(e)}")
            return pd.DataFrame()

    except Exception as e:
        st.error(f"Error during restaurant search: {str(e)}")
        return pd.DataFrame()

def filter_data_by_year(df, year):
    """Filter dataset by specific year"""
    return df[df['year'] == year]