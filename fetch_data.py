import pandas as pd
from pytrends.request import TrendReq
import time
import random
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_google_trends(origins: List[str], destinations: List[str], timeframe: str = 'today 3-m'):
    """
    Fetches Google Trends data for multiple origin-destination pairs
    Returns a combined DataFrame with all routes.
    """
    all_data = []
    
    for origin in origins:
        for destination in destinations:
            if origin == destination:
                continue
                
            try:
                pytrends = TrendReq(hl='en-US', tz=360)
                kw = f"{origin} {destination} flights"
                pytrends.build_payload([kw], geo='AU', timeframe=timeframe)
                
                df = pytrends.interest_over_time()
                if not df.empty:
                    df = df.reset_index()
                    df = df.rename(columns={kw: "trend_score"})
                    df['origin'] = origin
                    df['destination'] = destination
                    df['route'] = f"{origin}→{destination}"
                    all_data.append(df[['date', 'trend_score', 'origin', 'destination', 'route']])
                
                # Rate limiting
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                logger.error(f"Error fetching data for {origin}→{destination}: {e}")
                continue
    
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    else:
        return pd.DataFrame(columns=['date', 'trend_score', 'origin', 'destination', 'route'])

def get_australian_routes():
    """Returns popular Australian city pairs"""
    cities = ['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide', 'Gold Coast']
    return cities
