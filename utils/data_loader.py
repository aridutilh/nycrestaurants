import pandas as pd
from datetime import datetime, timedelta
import requests
import io
import streamlit as st

def load_nyc_restaurant_data():
    """Load NYC restaurant inspection data from the Open Data API"""
    url = "https://data.cityofnewyork.us/resource/43nn-pn8j.csv"

    try:
        # Read data directly from API
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Read CSV data
        df = pd.read_csv(io.StringIO(response.text))

        # Clean and process the data
        df['inspection_date'] = pd.to_datetime(df['inspection_date'], errors='coerce')

        # Drop rows with missing critical values
        df = df.dropna(subset=['latitude', 'longitude', 'score'])

        # Convert score to numeric, handling missing values
        df['score'] = pd.to_numeric(df['score'], errors='coerce')
        median_score = df['score'].median()
        df['score'] = df['score'].fillna(median_score)

        # Add year column for time-lapse
        df['year'] = df['inspection_date'].dt.year

        # Fill NA values in string columns with empty strings for better search
        string_columns = ['dba', 'building', 'street', 'grade']
        df[string_columns] = df[string_columns].fillna('')

        # Ensure all necessary columns exist
        required_columns = ['dba', 'building', 'street', 'score', 'grade', 
                          'latitude', 'longitude', 'year']

        if not all(col in df.columns for col in required_columns):
            missing_cols = [col for col in required_columns if col not in df.columns]
            raise ValueError(f"Missing required columns: {missing_cols}")

        return df

    except requests.RequestException as e:
        st.error(f"Error fetching data from API: {str(e)}")
        return pd.DataFrame()
    except ValueError as e:
        st.error(f"Error processing data: {str(e)}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return pd.DataFrame()

def filter_data_by_year(df, year):
    """Filter dataset by specific year"""
    return df[df['year'] == year]

def search_restaurants(df, query):
    """Search restaurants by name or address"""
    if df is None or df.empty:
        return pd.DataFrame()

    query = query.lower().strip()
    if not query:
        return pd.DataFrame()

    # Create a combined search field for better matching
    df['search_text'] = (
        df['dba'].str.lower() + ' ' + 
        df['building'].str.lower() + ' ' + 
        df['street'].str.lower()
    )

    # Search in the combined field
    mask = df['search_text'].str.contains(query, na=False)

    # Get unique restaurants (latest inspection for each)
    results = df[mask].sort_values('inspection_date', ascending=False)
    results = results.drop_duplicates(subset=['camis'])

    # Drop the temporary search column
    results = results.drop(columns=['search_text'])

    return results.head(50)  # Limit to 50 results for better performance