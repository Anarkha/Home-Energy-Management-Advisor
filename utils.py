"""
Utilities for Home Energy Management Advisor
Includes API clients, data fetchers, and helper functions
"""

try:
    import json
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

from datetime import datetime, timedelta
from typing import Dict, List, Optional


class ElectricityRateAPI:
    """
    Class to handle electricity rate API integration
    This includes real-time pricing and utility rate information
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.base_url = "https://api.utilityrates.com"  # Placeholder - would use real API
    
    def get_current_rate(self, zip_code: str = None, utility_id: str = None) -> Dict:
        """
        Get current electricity rate based on location/utility
        For demo purposes, we'll return sample data
        Max rate capped at ₹15/kWh
        """
        # In a real implementation, this would fetch from an actual API
        # For now, we'll return sample data based on some default inputs
        base_rate = 0.15  # ₹0.15 per kWh
        peak_rate = 0.20
        off_peak_rate = 0.10
        shoulder_rate = 0.15
        
        # Apply maximum rate limit
        current_rate = min(base_rate, 15)
        peak_rate = min(peak_rate, 15)
        off_peak_rate = min(off_peak_rate, 15)
        shoulder_rate = min(shoulder_rate, 15)
        
        return {
            'current_rate': current_rate,  # ₹0.15 per kWh (capped at ₹15)
            'rate_type': 'time_of_use',
            'peak_rate': peak_rate,
            'off_peak_rate': off_peak_rate,
            'shoulder_rate': shoulder_rate,
            'updated_at': datetime.now().isoformat(),
            'utility_company': 'Demo Utility Co.',
            'location': zip_code or '94105'
        }
    
    def get_rate_forecast(self, hours: int = 24) -> List[Dict]:
        """
        Get forecasted rates for the next specified hours
        """
        forecast = []
        now = datetime.now()
        
        for i in range(hours):
            hour = now + timedelta(hours=i)
            
            # Define time-based rates
            hour_of_day = hour.hour
            if 6 <= hour_of_day < 9 or 17 <= hour_of_day < 20:  # Peak hours
                rate = 0.20
            elif 22 <= hour_of_day or hour_of_day < 6:  # Off-peak hours
                rate = 0.10
            else:  # Standard hours
                rate = 0.15
            
            # Apply maximum rate limit
            rate = min(rate, 15)
            
            forecast.append({
                'time': hour.isoformat(),
                'rate': rate,
                'period': 'peak' if rate == 0.20 else 'off_peak' if rate == 0.10 else 'standard'
            })
        
        return forecast


class WeatherAPI:
    """
    Class to handle weather API integration
    Used for HVAC load prediction and seasonal adjustments
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    def get_current_weather(self, city: str, country_code: str = 'US') -> Dict:
        """
        Get current weather information
        For demo purposes, we'll return sample data
        """
        # In a real implementation:
        # url = f"{self.base_url}/weather?q={city},{country_code}&appid={self.api_key}&units=imperial"
        # response = requests.get(url)
        # return response.json()
        
        # Sample data for demo
        return {
            'temperature': 72,  # in Fahrenheit
            'humidity': 50,
            'weather_condition': 'Partly Cloudy',
            'location': city,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'high': 78,
            'low': 65
        }
    
    def get_forecast(self, city: str, days: int = 5) -> List[Dict]:
        """
        Get weather forecast for next few days
        """
        forecast = []
        base_temp = 72
        for i in range(days):
            day = datetime.now() + timedelta(days=i)
            temp = base_temp + (i % 7) - 3  # Simple variation
            forecast.append({
                'date': day.strftime('%Y-%m-%d'),
                'high': temp + 3,
                'low': temp - 4,
                'condition': 'Sunny' if i % 3 == 0 else 'Cloudy' if i % 3 == 1 else 'Partly Cloudy'
            })
        return forecast


class CarbonIntensityAPI:
    """
    Class to handle carbon intensity API integration
    Helps recommend times with lower environmental impact
    """
    
    def __init__(self):
        self.base_url = "https://api.carbonintensity.com"  # Placeholder
    
    def get_carbon_intensity(self) -> Dict:
        """
        Get current carbon intensity of electricity generation
        For demo purposes, we'll return sample data
        """
        return {
            'intensity': 200,  # grams CO2/kWh
            'index': 'moderate',  # low, moderate, high
            'updated_at': datetime.now().isoformat(),
            'recommendation': 'High intensity - consider delaying non-essential usage'
        }
    
    def get_intensity_forecast(self, hours: int = 24) -> List[Dict]:
        """
        Get forecasted carbon intensity for next hours
        """
        forecast = []
        now = datetime.now()
        
        for i in range(hours):
            hour = now + timedelta(hours=i)
            # Simulate changing carbon intensity
            intensity = 200 + (i * 2) % 50 - 25  # Varying intensity
            index = 'low' if intensity < 175 else 'moderate' if intensity < 225 else 'high'
            
            forecast.append({
                'time': hour.isoformat(),
                'intensity': intensity,
                'index': index
            })
        
        return forecast


def calculate_load_factor(temperature: float, season: str) -> float:
    """
    Calculate HVAC load factor based on temperature and season
    """
    # Basic model: higher load when temperature deviates from comfort zone
    comfort_zone = 72  # degrees F
    
    if season.lower() == 'summer':
        # More cooling needed when it's hotter
        if temperature > comfort_zone:
            return max(1.0, 1.0 + (temperature - comfort_zone) * 0.05)
        else:
            return max(0.5, 1.0 - (comfort_zone - temperature) * 0.02)
    elif season.lower() == 'winter':
        # More heating needed when it's colder
        if temperature < comfort_zone:
            return max(1.0, 1.0 + (comfort_zone - temperature) * 0.05)
        else:
            return max(0.5, 1.0 - (temperature - comfort_zone) * 0.02)
    else:
        # Spring/fall - moderate usage
        diff = abs(temperature - comfort_zone)
        return 1.0 + (diff * 0.01)


def get_season() -> str:
    """
    Determine the current season based on the month
    """
    month = datetime.now().month
    if month in [12, 1, 2]:
        return 'winter'
    elif month in [3, 4, 5]:
        return 'spring'
    elif month in [6, 7, 8]:
        return 'summer'
    else:
        return 'fall'


def format_currency(amount: float) -> str:
    """Format a currency amount"""
    return f"₹{amount:.2f}"


def format_energy(energy_kwh: float) -> str:
    """Format energy amount"""
    return f"{energy_kwh:.2f} kWh"


def format_percentage(percentage: float) -> str:
    """Format percentage"""
    return f"{percentage:.1f}%"