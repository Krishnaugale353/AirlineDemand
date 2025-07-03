import pandas as pd
import numpy as np
from typing import Dict, List, Tuple

def compute_route_popularity(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns route-level statistics including average, peak, and volatility.
    """
    if df.empty:
        return pd.DataFrame()
    
    summary = df.groupby('route').agg({
        'trend_score': ['mean', 'max', 'std', 'count']
    }).round(2)
    
    summary.columns = ['avg_trend', 'peak_trend', 'volatility', 'data_points']
    summary = summary.reset_index()
    
    # Calculate demand score (weighted average of trend and consistency)
    summary['demand_score'] = (summary['avg_trend'] * 0.7 + 
                              summary['peak_trend'] * 0.2 + 
                              (100 - summary['volatility'].fillna(0)) * 0.1)
    
    return summary.sort_values('demand_score', ascending=False)

def compute_trend_over_time(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns aggregated trend score per date with moving averages.
    """
    if df.empty:
        return pd.DataFrame()
    
    trend = df.groupby('date')['trend_score'].agg(['mean', 'max', 'count']).reset_index()
    trend.columns = ['date', 'avg_trend', 'peak_trend', 'active_routes']
    
    # Add 7-day moving average
    trend['trend_7d_ma'] = trend['avg_trend'].rolling(window=7).mean()
    
    return trend

def identify_seasonal_patterns(df: pd.DataFrame) -> Dict:
    """
    Identifies seasonal patterns in the data.
    """
    if df.empty:
        return {}
    
    df['day_of_week'] = df['date'].dt.day_name()
    df['month'] = df['date'].dt.month_name()
    
    patterns = {
        'peak_day': df.groupby('day_of_week')['trend_score'].mean().idxmax(),
        'peak_month': df.groupby('month')['trend_score'].mean().idxmax(),
        'weekend_vs_weekday': df.groupby(df['date'].dt.dayofweek < 5)['trend_score'].mean().to_dict()
    }
    
    return patterns

def detect_demand_anomalies(df: pd.DataFrame) -> List[Dict]:
    """
    Detects unusual spikes or drops in demand.
    """
    if df.empty or len(df) < 14:
        return []
    
    # Calculate rolling statistics
    df['rolling_mean'] = df['trend_score'].rolling(window=7).mean()
    df['rolling_std'] = df['trend_score'].rolling(window=7).std()
    
    # Define anomalies as values beyond 2 standard deviations
    df['anomaly'] = (np.abs(df['trend_score'] - df['rolling_mean']) > 2 * df['rolling_std'])
    
    anomalies = []
    for _, row in df[df['anomaly']].iterrows():
        anomalies.append({
            'date': row['date'].strftime('%Y-%m-%d'),
            'route': row.get('route', 'Unknown'),
            'trend_score': row['trend_score'],
            'type': 'spike' if row['trend_score'] > row['rolling_mean'] else 'drop'
        })
    
    return anomalies