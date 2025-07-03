import os
import openai
import pandas as pd
from typing import Dict, List
import json
from dotenv import load_dotenv

load_dotenv()

class AIAnalyzer:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    
    def analyze_demand_patterns(self, df: pd.DataFrame, route_stats: pd.DataFrame, 
                               seasonal_patterns: Dict, anomalies: List[Dict]) -> str:
        """
        Comprehensive AI analysis of demand patterns.
        """
        try:
            # Prepare data summary
            data_summary = {
                'total_routes': len(route_stats),
                'date_range': f"{df['date'].min()} to {df['date'].max()}",
                'top_routes': route_stats.head(5)[['route', 'demand_score']].to_dict('records'),
                'seasonal_patterns': seasonal_patterns,
                'anomalies_count': len(anomalies),
                'recent_anomalies': anomalies[-3:] if anomalies else []
            }
            
            prompt = f"""
            Analyze the following airline search demand data for Australia and provide insights:

            Data Summary:
            {json.dumps(data_summary, indent=2, default=str)}

            Please provide:
            1. Key demand trends and patterns
            2. Seasonal insights
            3. Route recommendations for hostel operators
            4. Potential business opportunities
            5. Risk factors or concerning trends

            Format your response as a structured analysis with clear sections.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"AI analysis unavailable: {str(e)}"
    
    def generate_recommendations(self, top_routes: pd.DataFrame, user_location: str = None) -> str:
        """
        Generate personalized recommendations for hostel operators.
        """
        try:
            routes_data = top_routes.head(10).to_dict('records')
            
            prompt = f"""
            Based on these high-demand flight routes in Australia, provide specific recommendations 
            for hostel operators:

            Top Routes: {json.dumps(routes_data, indent=2)}
            User Location: {user_location or 'Australia (general)'}

            Provide:
            1. Which cities to consider for hostel expansion
            2. Seasonal capacity planning advice
            3. Marketing timing recommendations
            4. Partnership opportunities with airlines/travel agencies
            5. Pricing strategy suggestions

            Keep recommendations practical and actionable.
            """
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Recommendations unavailable: {str(e)}"