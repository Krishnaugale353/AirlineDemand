import gradio as gr
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from fetch_data import fetch_google_trends, get_australian_routes
from analyze import (compute_route_popularity, compute_trend_over_time, 
                    identify_seasonal_patterns, detect_demand_anomalies)
from ai_analyzer import AIAnalyzer

def create_dashboard():
    ai_analyzer = AIAnalyzer()
    
    def analyze_market_demand(cities_input, timeframe, analysis_type):
        """
        Main analysis function that processes the data and returns insights.
        """
        try:
            # Parse cities input
            if cities_input.strip():
                cities = [city.strip() for city in cities_input.split(',')]
            else:
                cities = get_australian_routes()
            
            # Fetch data
            df = fetch_google_trends(cities, cities, timeframe)
            
            if df.empty:
                return (
                    pd.DataFrame(), 
                    None, 
                    None,
                    "No data available for the selected criteria.",
                    ""
                )
            
            # Analyze data
            route_stats = compute_route_popularity(df)
            trend_data = compute_trend_over_time(df)
            seasonal_patterns = identify_seasonal_patterns(df)
            anomalies = detect_demand_anomalies(df)
            
            # Create visualizations
            trend_fig = px.line(trend_data, x='date', y='avg_trend', 
                               title='Average Search Trend Over Time')
            trend_fig.add_scatter(x=trend_data['date'], y=trend_data['trend_7d_ma'], 
                                 mode='lines', name='7-day Moving Average')
            
            route_fig = px.bar(route_stats.head(10), x='route', y='demand_score',
                              title='Top 10 Routes by Demand Score')
            route_fig.update_xaxes(tickangle=45)
            
            # Generate AI insights
            if analysis_type == "Full Analysis":
                ai_insights = ai_analyzer.analyze_demand_patterns(df, route_stats, seasonal_patterns, anomalies)
            else:
                ai_insights = ai_analyzer.generate_recommendations(route_stats)
            
            # Create summary text
            summary = f"""
            ## Analysis Summary
            - **Total Routes Analyzed**: {len(route_stats)}
            - **Date Range**: {df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}
            - **Peak Demand Day**: {seasonal_patterns.get('peak_day', 'Unknown')}
            - **Peak Demand Month**: {seasonal_patterns.get('peak_month', 'Unknown')}
            - **Anomalies Detected**: {len(anomalies)}
            
            ### Top 5 Routes by Demand Score:
            {route_stats.head(5)[['route', 'demand_score']].to_string(index=False)}
            """
            
            return route_stats, trend_fig, route_fig, summary, ai_insights
            
        except Exception as e:
            error_msg = f"Error in analysis: {str(e)}"
            return pd.DataFrame(), None, None, error_msg, ""
    
    # Create Gradio interface
    with gr.Blocks(title="Airline Market Demand Dashboard") as demo:
        gr.Markdown("# 🛫 Airline Market Demand Analysis Dashboard")
        gr.Markdown("Analyze flight search trends to understand market demand patterns for hostel business planning.")
        
        with gr.Row():
            with gr.Column(scale=1):
                cities_input = gr.Textbox(
                    label="Cities to Analyze (comma-separated)",
                    placeholder="Sydney, Melbourne, Brisbane (leave empty for all major cities)",
                    value=""
                )
                timeframe = gr.Dropdown(
                    choices=['today 1-m', 'today 3-m', 'today 12-m', 'today 5-y'],
                    value='today 3-m',
                    label="Analysis Timeframe"
                )
                analysis_type = gr.Radio(
                    choices=["Full Analysis", "Recommendations Only"],
                    value="Full Analysis",
                    label="Analysis Type"
                )
                analyze_btn = gr.Button("🔍 Analyze Market Demand", variant="primary")
            
            with gr.Column(scale=2):
                summary_output = gr.Markdown(label="Summary")
        
        with gr.Row():
            trend_chart = gr.Plot(label="Search Trends Over Time")
            route_chart = gr.Plot(label="Route Demand Ranking")
        
        with gr.Row():
            route_table = gr.Dataframe(label="Detailed Route Statistics")
        
        with gr.Row():
            ai_insights = gr.Markdown(label="AI-Generated Insights & Recommendations")
        
        # Event handlers
        analyze_btn.click(
            fn=analyze_market_demand,
            inputs=[cities_input, timeframe, analysis_type],
            outputs=[route_table, trend_chart, route_chart, summary_output, ai_insights]
        )
        
        # Example usage
        gr.Markdown("""
        ## How to Use:
        1. **Enter cities** you want to analyze (or leave empty for major Australian cities)
        2. **Select timeframe** for analysis
        3. **Choose analysis type** - Full Analysis or Recommendations Only
        4. Click **Analyze Market Demand**
        
        ## Business Applications:
        - **Expansion Planning**: Identify high-demand routes for new hostel locations
        - **Seasonal Planning**: Understand demand patterns for capacity management
        - **Marketing Timing**: Optimize advertising spend based on search trends
        - **Partnership Opportunities**: Connect with airlines on popular routes
        """)
    
    return demo