# Home Energy Management Advisor

An advanced expert system that helps households reduce electricity costs and save energy through personalized recommendations based on appliance usage, real-time electricity rates, weather data, and comprehensive financial modeling.

## Overview

The Home Energy Management Advisor is an AI expert system that:
- Analyzes home appliance energy usage with real-time data integration
- Provides personalized cost-saving recommendations
- Suggests optimal usage times based on time-of-use rates and carbon intensity
- Recommends energy-efficient upgrades with detailed financial analysis
- Helps implement sustainable home energy practices
- Includes a web dashboard for interactive analysis

## Features

- **Comprehensive Appliance Database**: Includes power consumption data for 30+ common household appliances
- **Real-Time Data Integration**: Connects with utility rate APIs, weather services, and carbon intensity data
- **Time-of-Use Analysis**: Recommends shifting usage to optimal hours based on dynamic rates
- **Advanced Analytics**: Load forecasting, usage pattern analysis, and appliance health monitoring
- **Financial Modeling**: ROI calculations, payback periods, and NPV analysis for upgrades and renewable energy
- **Efficiency Recommendations**: Detailed upgrade suggestions with cost-benefit analysis
- **Web Dashboard**: Interactive interface with visualizations and real-time data
- **Environmental Impact**: Carbon intensity tracking and eco-friendly recommendations
- **Cost Analysis**: Calculates annual energy costs for each appliance with detailed breakdowns
- **Personalized Advice**: Provides tailored recommendations based on user's specific setup

## Enhanced Capabilities

### Real-Time Data Integration
- Electricity rate APIs for current and forecasted rates
- Weather API integration for HVAC load prediction
- Carbon intensity tracking for environmental optimization

### Advanced Analytics
- Energy usage forecasting based on weather and historical patterns
- Load profiling and peak demand analysis
- Appliance efficiency degradation tracking
- Usage pattern recognition

### Financial Modeling
- Appliance upgrade ROI calculations with payback periods and NPV
- Solar panel investment analysis
- Battery storage financial modeling
- Financing option comparisons
- Demand charge reduction analysis

### Web Dashboard
- Interactive energy analysis with charts and graphs
- Real-time electricity rate visualization
- Weather-based usage predictions
- Financial analysis of upgrades
- Carbon intensity tracking

## How It Works

1. The system collects information about appliances in your home and their usage patterns
2. It integrates real-time data on electricity rates, weather, and carbon intensity
3. It analyzes energy consumption and costs using built-in knowledge base
4. It runs advanced analytics and financial models to identify opportunities
5. It generates personalized recommendations to save energy and reduce costs
6. It provides actionable advice on when and how to use appliances efficiently

## Usage

### Basic Usage (CLI)
```bash
python main.py
```
Follow the interactive prompts to enter appliance data and receive recommendations.

### Advanced Usage (Programmatic)
```bash
python advanced_example.py
```
This demonstrates all advanced features with simulated real-time data.

### Web Dashboard
```bash
python web_interface.py
```
Then visit http://localhost:5000 to access the interactive dashboard.

## Architecture

- `knowledge_base.py`: Contains appliance data, energy usage patterns, and utility rate information
- `expert_system.py`: Core logic for analyzing inputs and generating recommendations
- `strategies.py`: Cost-saving and efficiency recommendation algorithms
- `utils.py`: API clients and utility functions for real-time data
- `advanced_analytics.py`: Advanced analytics and forecasting algorithms
- `financial_modeling.py`: Financial analysis and ROI calculations
- `cli_interface.py`: Command-line interface for user interaction
- `web_interface.py`: Flask-based web dashboard
- `main.py`: Entry point for the basic application
- `example_usage.py`: Basic usage examples
- `advanced_example.py`: Advanced features demonstration

## Example Analysis

The system can identify:
- Highest energy-consuming appliances
- Opportunities to shift usage to optimal times
- Appliances that would benefit from efficiency upgrades
- Potential annual savings with detailed financial analysis
- Environmental impact and carbon footprint
- Investment opportunities with ROI calculations

## Customization

The knowledge base can be extended with additional appliances and updated energy consumption data. The system supports custom electricity rates, weather data sources, and usage patterns. APIs can be configured with real credentials for production use.

## About Expert Systems

This project demonstrates how modern rule-based expert systems can integrate with real-time data, advanced analytics, and financial modeling to provide sophisticated decision support. By encoding energy efficiency expertise and combining it with current data, users can make informed decisions about their home energy consumption.

## Dependencies

This project requires Python 3.x with the following packages:
- Flask (for web dashboard)
- requests (for API integration)

Install dependencies with:
```bash
pip install -r requirements.txt
```