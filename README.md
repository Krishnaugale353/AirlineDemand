# Airline Market Demand Dashboard

A comprehensive web application for analyzing airline booking market demand trends using Google Trends data and AI-powered insights.

## Features

- **Multi-route Analysis**: Analyze multiple origin-destination pairs simultaneously
- **Advanced Analytics**: Route popularity, seasonal patterns, anomaly detection
- **AI-Powered Insights**: Comprehensive market analysis and business recommendations
- **Interactive Dashboard**: User-friendly interface with charts and tables
- **Business-Focused**: Specifically designed for hostel operators and travel businesses

## Setup Instructions

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

4. **Access the dashboard**:
   Open your browser and navigate to `http://localhost:8000`

## Usage

1. Enter cities you want to analyze (or leave empty for major Australian cities)
2. Select your preferred analysis timeframe
3. Choose between Full Analysis or Recommendations Only
4. Click "Analyze Market Demand" to generate insights

## API Endpoints

- `GET /health` - Health check endpoint
- Web interface available at root path `/`

## Business Applications

- **Expansion Planning**: Identify high-demand routes for new hostel locations
- **Seasonal Planning**: Understand demand patterns for capacity management
- **Marketing Timing**: Optimize advertising spend based on search trends
- **Partnership Opportunities**: Connect with airlines on popular routes
