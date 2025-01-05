import os
import json
from datetime import datetime, timedelta
import pandas as pd

CACHE_DIR = "cache"
CACHE_FILE = os.path.join(CACHE_DIR, "restaurant_data.csv")
CACHE_META_FILE = os.path.join(CACHE_DIR, "cache_metadata.json")

def ensure_cache_dir():
    """Ensure cache directory exists"""
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

def is_cache_valid():
    """Check if cached data is still valid (less than 24 hours old)"""
    if not os.path.exists(CACHE_META_FILE):
        return False

    try:
        with open(CACHE_META_FILE, 'r') as f:
            metadata = json.load(f)

        last_updated = datetime.fromisoformat(metadata['last_updated'])
        return datetime.now() - last_updated < timedelta(hours=24)
    except Exception:
        return False

def save_to_cache(df):
    """Save DataFrame to cache with metadata"""
    ensure_cache_dir()

    # Save the DataFrame
    df.to_csv(CACHE_FILE, index=False)

    # Save metadata
    metadata = {
        'last_updated': datetime.now().isoformat(),
        'record_count': len(df),
        'unique_restaurants': len(df['camis'].unique())
    }

    with open(CACHE_META_FILE, 'w') as f:
        json.dump(metadata, f)

def load_from_cache():
    """Load DataFrame from cache if it exists"""
    if not os.path.exists(CACHE_FILE):
        return None

    try:
        df = pd.read_csv(CACHE_FILE)

        # Convert date columns back to datetime
        df['inspection_date'] = pd.to_datetime(df['inspection_date'])

        # Ensure numeric columns are properly typed
        df['score'] = pd.to_numeric(df['score'], errors='coerce')
        df['year'] = pd.to_numeric(df['year'], errors='coerce')

        return df
    except Exception:
        return None

def get_cache_metadata():
    """Get cache metadata if available"""
    if not os.path.exists(CACHE_META_FILE):
        return None

    try:
        with open(CACHE_META_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return None