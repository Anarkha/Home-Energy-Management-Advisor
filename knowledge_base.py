"""
Knowledge Base for Home Energy Management Advisor
Contains appliance data, energy usage patterns, and utility rate information
"""

# Appliance database with typical power consumption values (in watts)
APPLIANCE_DATABASE = {
    # Kitchen appliances
    'refrigerator': {
        'power_watts': 150,
        'usage_hours_per_day': 24,
        'usage_pattern': 'continuous',
        'efficiency_rating': 'medium',
        'cost_per_year': 90,
        'description': 'Maintains food at safe temperatures',
        'seasonal_factor': 1.1,  # Uses more in summer
        'age_factor': {'new': 1.0, '5_years': 1.1, '10_years': 1.2, '15_years': 1.3},
        'load_shifting_possible': False,
        'smart_features': ['energy_monitoring'],
        'lifespan_years': 12,
        'maintenance_frequency': 'yearly',
        'standby_watts': 2
    },
    'oven': {
        'power_watts': 2400,
        'usage_hours_per_day': 1,
        'usage_pattern': 'intermittent',
        'efficiency_rating': 'medium',
        'cost_per_year': 100,
        'description': 'Electric oven for cooking',
        'seasonal_factor': 1.0,
        'age_factor': {'new': 1.0, '5_years': 1.05, '10_years': 1.1, '15_years': 1.2},
        'load_shifting_possible': True,
        'smart_features': ['timer', 'remote_control'],
        'lifespan_years': 15,
        'maintenance_frequency': 'biyearly',
        'standby_watts': 5
    },
    'microwave': {
        'power_watts': 1000,
        'usage_hours_per_day': 0.5,
        'usage_pattern': 'intermittent',
        'efficiency_rating': 'high',
        'cost_per_year': 20,
        'description': 'Quick cooking and reheating',
        'seasonal_factor': 1.0,
        'age_factor': {'new': 1.0, '5_years': 1.03, '10_years': 1.07, '15_years': 1.15},
        'load_shifting_possible': True,
        'smart_features': ['sensor_cooking', 'pre_programmed_settings'],
        'lifespan_years': 9,
        'maintenance_frequency': 'as_needed',
        'standby_watts': 3
    },
    'dishwasher': {
        'power_watts': 1800,
        'usage_hours_per_day': 1,
        'usage_pattern': 'scheduled',
        'efficiency_rating': 'high',
        'cost_per_year': 70,
        'description': 'Automatic dish cleaning',
        'seasonal_factor': 1.0,
        'age_factor': {'new': 1.0, '5_years': 1.05, '10_years': 1.15, '15_years': 1.3},
        'load_shifting_possible': True,
        'smart_features': ['eco_mode', 'delay_start', 'energy_monitoring'],
        'lifespan_years': 10,
        'maintenance_frequency': 'quarterly',
        'standby_watts': 1
    },
    'coffee_maker': {
        'power_watts': 900,
        'usage_hours_per_day': 0.5,
        'usage_pattern': 'morning',
        'efficiency_rating': 'medium',
        'cost_per_year': 15,
        'description': 'Brews coffee',
        'seasonal_factor': 1.0,
        'age_factor': {'new': 1.0, '5_years': 1.05, '10_years': 1.1, '15_years': 1.2},
        'load_shifting_possible': False,
        'smart_features': ['timer', 'auto_shutoff'],
        'lifespan_years': 5,
        'maintenance_frequency': 'monthly',
        'standby_watts': 4
    },
    'toaster': {
        'power_watts': 1200,
        'usage_hours_per_day': 0.25,
        'usage_pattern': 'morning',
        'efficiency_rating': 'medium',
        'cost_per_year': 10,
        'description': 'Toasts bread',
        'seasonal_factor': 1.0,
        'age_factor': {'new': 1.0, '5_years': 1.05, '10_years': 1.1, '15_years': 1.2},
        'load_shifting_possible': True,
        'smart_features': [],
        'lifespan_years': 6,
        'maintenance_frequency': 'as_needed',
        'standby_watts': 0.5
    },
    
    # Laundry appliances
    'washing_machine': {
        'power_watts': 500,
        'usage_hours_per_day': 1,
        'usage_pattern': 'scheduled',
        'efficiency_rating': 'high',
        'cost_per_year': 50,
        'description': 'Cleans clothes',
        'seasonal_factor': 1.0,
        'age_factor': {'new': 1.0, '5_years': 1.05, '10_years': 1.15, '15_years': 1.3},
        'load_shifting_possible': True,
        'smart_features': ['eco_mode', 'delay_start', 'energy_monitoring'],
        'lifespan_years': 11,
        'maintenance_frequency': 'quarterly',
        'standby_watts': 1
    },
    'dryer': {
        'power_watts': 3000,
        'usage_hours_per_day': 1,
        'usage_pattern': 'scheduled',
        'efficiency_rating': 'low',
        'cost_per_year': 150,
        'description': 'Dries clothes (electric)',
        'seasonal_factor': 1.0,
        'age_factor': {'new': 1.0, '5_years': 1.05, '10_years': 1.15, '15_years': 1.3},
        'load_shifting_possible': True,
        'smart_features': ['moisture_sensor', 'delay_start'],
        'lifespan_years': 13,
        'maintenance_frequency': 'quarterly',
        'standby_watts': 2
    },
    'clothes_washer': {
        'power_watts': 500,
        'usage_hours_per_day': 1,
        'usage_pattern': 'scheduled',
        'efficiency_rating': 'high',
        'cost_per_year': 50,
        'description': 'Energy efficient clothes washer',
        'seasonal_factor': 1.0,
        'age_factor': {'new': 1.0, '5_years': 1.05, '10_years': 1.15, '15_years': 1.3},
        'load_shifting_possible': True,
        'smart_features': ['eco_mode', 'delay_start', 'energy_monitoring'],
        'lifespan_years': 11,
        'maintenance_frequency': 'quarterly',
        'standby_watts': 1
    },
    
    # HVAC and climate control
    'air_conditioner': {
        'power_watts': 3500,
        'usage_hours_per_day': 8,
        'usage_pattern': 'peak',
        'efficiency_rating': 'medium',
        'cost_per_year': 400,
        'description': 'Central air conditioning',
        'seasonal_factor': 1.8,  # Much higher in summer
        'age_factor': {'new': 1.0, '5_years': 1.1, '10_years': 1.25, '15_years': 1.5},
        'load_shifting_possible': True,
        'smart_features': ['programmable_thermostat', 'zoning', 'energy_monitoring'],
        'lifespan_years': 15,
        'maintenance_frequency': 'yearly',
        'standby_watts': 5
    },
    'heater': {
        'power_watts': 1500,
        'usage_hours_per_day': 10,
        'usage_pattern': 'winter',
        'efficiency_rating': 'medium',
        'cost_per_year': 600,
        'description': 'Electric space heater',
        'seasonal_factor': 2.0,  # Much higher in winter
        'age_factor': {'new': 1.0, '5_years': 1.1, '10_years': 1.25, '15_years': 1.5},
        'load_shifting_possible': True,
        'smart_features': ['programmable_thermostat', 'timer'],
        'lifespan_years': 12,
        'maintenance_frequency': 'yearly',
        'standby_watts': 1
    },
    'heat_pump': {
        'power_watts': 2000,
        'usage_hours_per_day': 8,
        'usage_pattern': 'variable',
        'efficiency_rating': 'high',
        'cost_per_year': 300,
        'description': 'Energy efficient heating/cooling',
        'seasonal_factor': 1.2,  # More efficient but still seasonal
        'age_factor': {'new': 1.0, '5_years': 1.05, '10_years': 1.15, '15_years': 1.3},
        'load_shifting_possible': True,
        'smart_features': ['dual_fuel', 'zoning', 'energy_monitoring'],
        'lifespan_years': 16,
        'maintenance_frequency': 'yearly',
        'standby_watts': 3
    },
    'evaporative_cooler': {
        'power_watts': 750,
        'usage_hours_per_day': 12,
        'usage_pattern': 'daytime',
        'efficiency_rating': 'high',
        'cost_per_year': 80,
        'description': 'Evaporative cooler (swamp cooler) - more efficient in dry climates',
        'seasonal_factor': 1.5,
        'age_factor': {'new': 1.0, '5_years': 1.05, '10_years': 1.15, '15_years': 1.25},
        'load_shifting_possible': True,
        'smart_features': ['humidity_sensing', 'timer'],
        'lifespan_years': 15,
        'maintenance_frequency': 'monthly',
        'standby_watts': 2
    },
    
    # Electronics
    'television': {
        'power_watts': 100,
        'usage_hours_per_day': 4,
        'usage_pattern': 'evening',
        'efficiency_rating': 'high',
        'cost_per_year': 30,
        'description': 'Entertainment display',
        'seasonal_factor': 1.0,
        'age_factor': {'new': 1.0, '5_years': 1.1, '10_years': 1.3, '15_years': 1.5},
        'load_shifting_possible': True,
        'smart_features': ['power_saving_mode', 'auto_shutoff'],
        'lifespan_years': 7,
        'maintenance_frequency': 'as_needed',
        'standby_watts': 2
    },
    'computer_laptop': {
        'power_watts': 60,
        'usage_hours_per_day': 6,
        'usage_pattern': 'daytime',
        'efficiency_rating': 'high',
        'cost_per_year': 25,
        'description': 'Personal computing device',
        'seasonal_factor': 1.0,
        'age_factor': {'new': 1.0, '5_years': 1.1, '10_years': 1.2, '15_years': 1.4},
        'load_shifting_possible': True,
        'smart_features': ['power_management', 'sleep_modes'],
        'lifespan_years': 4,
        'maintenance_frequency': 'yearly',
        'standby_watts': 1
    },
    'computer_desktop': {
        'power_watts': 300,
        'usage_hours_per_day': 8,
        'usage_pattern': 'daytime',
        'efficiency_rating': 'medium',
        'cost_per_year': 100,
        'description': 'Personal computer',
        'seasonal_factor': 1.0,
        'age_factor': {'new': 1.0, '5_years': 1.05, '10_years': 1.2, '15_years': 1.4},
        'load_shifting_possible': True,
        'smart_features': ['power_management', 'sleep_modes'],
        'lifespan_years': 6,
        'maintenance_frequency': 'yearly',
        'standby_watts': 5
    },
    'game_console': {
        'power_watts': 200,
        'usage_hours_per_day': 2,
        'usage_pattern': 'evening',
        'efficiency_rating': 'medium',
        'cost_per_year': 50,
        'description': 'Gaming entertainment system',
        'seasonal_factor': 1.0,
        'age_factor': {'new': 1.0, '5_years': 1.05, '10_years': 1.15, '15_years': 1.3},
        'load_shifting_possible': True,
        'smart_features': ['auto_shutoff', 'sleep_mode'],
        'lifespan_years': 5,
        'maintenance_frequency': 'as_needed',
        'standby_watts': 8
    },
    'router': {
        'power_watts': 12,
        'usage_hours_per_day': 24,
        'usage_pattern': 'continuous',
        'efficiency_rating': 'medium',
        'cost_per_year': 10,
        'description': 'Network router',
        'seasonal_factor': 1.0,
        'age_factor': {'new': 1.0, '5_years': 1.05, '10_years': 1.1, '15_years': 1.2},
        'load_shifting_possible': False,
        'smart_features': [],
        'lifespan_years': 5,
        'maintenance_frequency': 'as_needed',
        'standby_watts': 12
    },
    
    # Lighting
    'led_bulb': {
        'power_watts': 10,
        'usage_hours_per_day': 6,
        'usage_pattern': 'evening',
        'efficiency_rating': 'very_high',
        'cost_per_year': 5,
        'description': 'Energy efficient LED lighting',
        'seasonal_factor': 1.2,  # More lighting needed in winter
        'age_factor': {'new': 1.0, '5_years': 1.0, '10_years': 1.01, '15_years': 1.02},  # Very stable
        'load_shifting_possible': True,
        'smart_features': ['dimming', 'scheduling', 'color_control'],
        'lifespan_years': 20,
        'maintenance_frequency': 'rarely',
        'standby_watts': 0
    },
    'incandescent_bulb': {
        'power_watts': 60,
        'usage_hours_per_day': 6,
        'usage_pattern': 'evening',
        'efficiency_rating': 'very_low',
        'cost_per_year': 30,
        'description': 'Traditional lighting (inefficient)',
        'seasonal_factor': 1.2,  # More lighting needed in winter
        'age_factor': {'new': 1.0, '5_years': 1.0, '10_years': 1.02, '15_years': 1.05},  # Stable but inefficient
        'load_shifting_possible': True,
        'smart_features': [],
        'lifespan_years': 1,
        'maintenance_frequency': 'yearly',
        'standby_watts': 0
    },
    'smart_led_bulb': {
        'power_watts': 9,
        'usage_hours_per_day': 6,
        'usage_pattern': 'evening',
        'efficiency_rating': 'very_high',
        'cost_per_year': 6,
        'description': 'Smart LED lighting with app control',
        'seasonal_factor': 1.2,  # More lighting needed in winter
        'age_factor': {'new': 1.0, '5_years': 1.0, '10_years': 1.01, '15_years': 1.02},  # Very stable
        'load_shifting_possible': True,
        'smart_features': ['dimming', 'scheduling', 'color_control', 'motion_sensor', 'app_control'],
        'lifespan_years': 20,
        'maintenance_frequency': 'rarely',
        'standby_watts': 0.5
    },
    
    # Other appliances
    'dishwasher': {
        'power_watts': 1800,
        'usage_hours_per_day': 1,
        'usage_pattern': 'scheduled',
        'efficiency_rating': 'high',
        'cost_per_year': 70,
        'description': 'Automatic dish cleaning',
        'seasonal_factor': 1.0,
        'age_factor': {'new': 1.0, '5_years': 1.05, '10_years': 1.15, '15_years': 1.3},
        'load_shifting_possible': True,
        'smart_features': ['eco_mode', 'delay_start', 'energy_monitoring'],
        'lifespan_years': 10,
        'maintenance_frequency': 'quarterly',
        'standby_watts': 1
    },
    'water_heater': {
        'power_watts': 4000,
        'usage_hours_per_day': 2,
        'usage_pattern': 'morning_evening',
        'efficiency_rating': 'medium',
        'cost_per_year': 350,
        'description': 'Electric water heating',
        'seasonal_factor': 1.1,  # More hot water in winter
        'age_factor': {'new': 1.0, '5_years': 1.05, '10_years': 1.2, '15_years': 1.4},
        'load_shifting_possible': True,
        'smart_features': ['scheduling', 'temperature_control', 'energy_monitoring'],
        'lifespan_years': 10,
        'maintenance_frequency': 'yearly',
        'standby_watts': 50  # High standby losses
    },
    'tankless_water_heater': {
        'power_watts': 0,  # Only when in use
        'usage_hours_per_day': 1,  # But high power when used
        'usage_pattern': 'on_demand',
        'efficiency_rating': 'high',
        'cost_per_year': 250,
        'description': 'Instant hot water heater - only uses power when hot water is needed',
        'seasonal_factor': 1.05,
        'age_factor': {'new': 1.0, '5_years': 1.02, '10_years': 1.05, '15_years': 1.1},
        'load_shifting_possible': True,
        'smart_features': ['scheduling', 'temperature_control', 'energy_monitoring'],
        'lifespan_years': 20,
        'maintenance_frequency': 'yearly',
        'standby_watts': 0
    },
    'pool_pump': {
        'power_watts': 2500,
        'usage_hours_per_day': 8,
        'usage_pattern': 'daytime',
        'efficiency_rating': 'low',
        'cost_per_year': 450,
        'description': 'Pool circulation pump',
        'seasonal_factor': 1.5,  # Only used in warm months
        'age_factor': {'new': 1.0, '5_years': 1.1, '10_years': 1.25, '15_years': 1.5},
        'load_shifting_possible': True,
        'smart_features': ['scheduling', 'variable_speed'],
        'lifespan_years': 8,
        'maintenance_frequency': 'seasonally',
        'standby_watts': 1
    },
    'electric_vehicle_charger': {
        'power_watts': 7200,
        'usage_hours_per_day': 8,
        'usage_pattern': 'overnight',
        'efficiency_rating': 'high',
        'cost_per_year': 600,
        'description': 'Electric vehicle charging station',
        'seasonal_factor': 1.0,
        'age_factor': {'new': 1.0, '5_years': 1.0, '10_years': 1.0, '15_years': 1.0},  # No degradation
        'load_shifting_possible': True,
        'smart_features': ['scheduling', 'energy_monitoring', 'load_balancing'],
        'lifespan_years': 10,
        'maintenance_frequency': 'yearly',
        'standby_watts': 1
    },
    'electric_vehicle_charger_smart': {
        'power_watts': 7200,
        'usage_hours_per_day': 8,
        'usage_pattern': 'overnight',
        'efficiency_rating': 'very_high',
        'cost_per_year': 600,
        'description': 'Smart electric vehicle charging station with scheduling',
        'seasonal_factor': 1.0,
        'age_factor': {'new': 1.0, '5_years': 1.0, '10_years': 1.0, '15_years': 1.0},
        'load_shifting_possible': True,
        'smart_features': ['scheduling', 'energy_monitoring', 'load_balancing', 'renewable_energy_aware'],
        'lifespan_years': 10,
        'maintenance_frequency': 'yearly',
        'standby_watts': 0.5
    },
    'air_purifier': {
        'power_watts': 50,
        'usage_hours_per_day': 20,
        'usage_pattern': 'continuous',
        'efficiency_rating': 'medium',
        'cost_per_year': 40,
        'description': 'Air purification system',
        'seasonal_factor': 1.3,  # More needed during allergy seasons
        'age_factor': {'new': 1.0, '5_years': 1.1, '10_years': 1.25, '15_years': 1.4},
        'load_shifting_possible': True,
        'smart_features': ['air_quality_sensing', 'scheduling', 'speed_control'],
        'lifespan_years': 5,
        'maintenance_frequency': 'quarterly',
        'standby_watts': 1
    },
    'dehumidifier': {
        'power_watts': 300,
        'usage_hours_per_day': 12,
        'usage_pattern': 'humidity_dependent',
        'efficiency_rating': 'medium',
        'cost_per_year': 120,
        'description': 'Dehumidifier for moisture control',
        'seasonal_factor': 1.4,  # More needed in humid seasons
        'age_factor': {'new': 1.0, '5_years': 1.1, '10_years': 1.2, '15_years': 1.3},
        'load_shifting_possible': True,
        'smart_features': ['humidity_sensing', 'scheduling', 'energy_monitoring'],
        'lifespan_years': 8,
        'maintenance_frequency': 'quarterly',
        'standby_watts': 2
    },
    'humidifier': {
        'power_watts': 150,
        'usage_hours_per_day': 10,
        'usage_pattern': 'winter',
        'efficiency_rating': 'medium',
        'cost_per_year': 45,
        'description': 'Humidifier for adding moisture to air',
        'seasonal_factor': 1.5,  # Used mainly in dry winter
        'age_factor': {'new': 1.0, '5_years': 1.05, '10_years': 1.15, '15_years': 1.3},
        'load_shifting_possible': True,
        'smart_features': ['humidity_sensing', 'scheduling'],
        'lifespan_years': 6,
        'maintenance_frequency': 'quarterly',
        'standby_watts': 1
    }
}

# Detailed utility rate information with time-of-use complexity
UTILITY_RATES = {
    'summer_peak_hours': {
        'season': 'summer',
        'start': 15,  # 3 PM
        'end': 20,    # 8 PM
        'multiplier': 2.0,  # 200% of base rate during highest demand
        'days': 'weekday',
        'description': 'Critical peak hours with highest rates'
    },
    'summer_shoulder_hours': {
        'season': 'summer', 
        'start': 11,  # 11 AM
        'end': 15,    # 3 PM
        'multiplier': 1.5,  # 150% of base rate
        'days': 'weekday',
        'description': 'Shoulder hours with moderate rates'
    },
    'summer_off_peak_hours': {
        'season': 'summer',
        'start': 20,  # 8 PM
        'end': 7,     # 7 AM
        'multiplier': 0.5,  # 50% of base rate
        'days': 'all',
        'description': 'Off-peak hours with lowest rates'
    },
    'winter_peak_hours': {
        'season': 'winter',
        'start': 17,  # 5 PM
        'end': 21,    # 9 PM
        'multiplier': 1.8,  # 180% of base rate
        'days': 'weekday',
        'description': 'Winter peak with high heating demand'
    },
    'winter_off_peak_hours': {
        'season': 'winter',
        'start': 21,  # 9 PM
        'end': 6,     # 6 AM
        'multiplier': 0.6,  # 60% of base rate
        'days': 'all',
        'description': 'Winter off-peak hours'
    },
    'weekend_all_hours': {
        'season': 'all',
        'start': 0,   # Midnight
        'end': 24,    # Next midnight
        'multiplier': 0.8,  # 80% of base rate on weekends
        'days': 'weekend',
        'description': 'Reduced weekend rates'
    }
}

# Efficiency improvement options with detailed metrics
EFFICIENCY_OPTIONS = {
    'led_retrofit': {
        'cost': 50,
        'savings_percentage': 80,
        'description': 'Replace incandescent bulbs with LED',
        'installation_time': '1 hour',
        'payback_period': '6 months',
        'lifespan': 15,  # years
        'maintenance': 'rare'
    },
    'smart_thermostat': {
        'cost': 250,
        'savings_percentage': 15,
        'description': 'Programmable thermostat for HVAC',
        'installation_time': '2 hours',
        'payback_period': '1 year',
        'lifespan': 10,
        'maintenance': 'software updates'
    },
    'energy_star_appliance': {
        'cost': 800,  # varies by appliance
        'savings_percentage': 25,
        'description': 'Replace with ENERGY STAR certified model',
        'installation_time': 'varies',
        'payback_period': '3 years',
        'lifespan': 12,
        'maintenance': 'standard'
    },
    'solar_panels': {
        'cost': 20000,
        'savings_percentage': 70,
        'description': 'Install solar panels for renewable energy',
        'installation_time': '1 day',
        'payback_period': '7 years',
        'lifespan': 25,
        'maintenance': 'annual'
    },
    'tankless_water_heater': {
        'cost': 1000,
        'savings_percentage': 30,
        'description': 'Replace tank water heater with tankless',
        'installation_time': '1 day',
        'payback_period': '4 years',
        'lifespan': 20,
        'maintenance': 'annual'
    },
    'duct_sealing': {
        'cost': 500,
        'savings_percentage': 20,
        'description': 'Seal air ducts to prevent energy loss',
        'installation_time': '1 day',
        'payback_period': '2 years',
        'lifespan': 15,
        'maintenance': 'as needed'
    },
    'smart_plugs': {
        'cost': 25,
        'savings_percentage': 10,
        'description': 'Smart plugs to eliminate phantom loads',
        'installation_time': '10 minutes',
        'payback_period': '6 months',
        'lifespan': 5,
        'maintenance': 'software updates'
    }
}

# Complex cost-saving strategies with dependencies
STRATEGIES = {
    'time_based_optimization': {
        'name': 'Time-based optimization',
        'description': 'Shift high-energy usage to off-peak hours',
        'complexity': 'medium',
        'implementation_time': 'immediate',
        'savings_potential': 15,
        'dependencies': ['smart_scheduling'],
        'appliances_affected': ['water_heater', 'dishwasher', 'washing_machine', 'electric_vehicle_charger']
    },
    'appliance_upgrade': {
        'name': 'Appliance upgrade',
        'description': 'Replace inefficient appliances with ENERGY STAR models',
        'complexity': 'high',
        'implementation_time': '1-3 months',
        'savings_potential': 25,
        'dependencies': ['budget', 'installation'],
        'appliances_affected': ['refrigerator', 'washer', 'dryer', 'air_conditioner']
    },
    'smart_home_automation': {
        'name': 'Smart home automation',
        'description': 'Use smart devices to optimize usage patterns',
        'complexity': 'high',
        'implementation_time': '2-4 weeks',
        'savings_potential': 20,
        'dependencies': ['smart_devices', 'wifi'],
        'appliances_affected': ['thermostat', 'lighting', 'plugs']
    },
    'insulation_improvement': {
        'name': 'Insulation and weatherization',
        'description': 'Seal air leaks and improve insulation',
        'complexity': 'medium',
        'implementation_time': '1-2 weeks',
        'savings_potential': 20,
        'dependencies': ['construction', 'weather'],
        'appliances_affected': ['heater', 'air_conditioner']
    },
    'phantom_load_reduction': {
        'name': 'Phantom load reduction',
        'description': 'Unplug devices when not in use or use smart power strips',
        'complexity': 'low',
        'implementation_time': 'immediate',
        'savings_potential': 10,
        'dependencies': ['smart_plugs'],
        'appliances_affected': ['electronics', 'chargers']
    },
    'hvac_optimization': {
        'name': 'HVAC system optimization',
        'description': 'Optimize heating and cooling system operation',
        'complexity': 'medium',
        'implementation_time': '1-2 weeks',
        'savings_potential': 18,
        'dependencies': ['thermostat', 'filter_maintenance'],
        'appliances_affected': ['heater', 'air_conditioner', 'heat_pump']
    },
    'water_heating_efficiency': {
        'name': 'Water heating efficiency',
        'description': 'Optimize water heater temperature and insulation',
        'complexity': 'low',
        'implementation_time': '1 day',
        'savings_potential': 12,
        'dependencies': ['temperature_control'],
        'appliances_affected': ['water_heater']
    }
}

# Energy efficiency standards and ratings
EFFICIENCY_STANDARDS = {
    'ENERGY_STAR': {
        'minimum_savings': 10,
        'verification': 'certified',
        'label_validity': '5 years',
        'rebate_eligible': True
    },
    'ENERGY_STAR_CERTIFIED': {
        'minimum_savings': 15,
        'verification': 'verified',
        'label_validity': '3 years',
        'rebate_eligible': True
    },
    'ENERGY_STAR_PLUS': {
        'minimum_savings': 20,
        'verification': 'enhanced',
        'label_validity': '3 years',
        'rebate_eligible': True
    }
}

# Carbon intensity thresholds
CARBON_INTENSITY_LEVELS = {
    'very_low': {'max': 100, 'color': 'green', 'description': 'Very clean energy source'},
    'low': {'max': 200, 'color': 'lightgreen', 'description': 'Clean energy source'},
    'moderate': {'max': 400, 'color': 'yellow', 'description': 'Mixed energy source'},
    'high': {'max': 600, 'color': 'orange', 'description': 'Carbon intensive energy'},
    'very_high': {'max': 1000, 'color': 'red', 'description': 'Very carbon intensive energy'}
}

# Environmental impact factors
ENVIRONMENTAL_FACTORS = {
    'coal_generation': {'factor': 0.95, 'description': 'Coal power plant emissions'},
    'natural_gas': {'factor': 0.45, 'description': 'Natural gas power plant emissions'},
    'nuclear': {'factor': 0.03, 'description': 'Nuclear power emissions'},
    'hydroelectric': {'factor': 0.02, 'description': 'Hydroelectric power emissions'},
    'wind': {'factor': 0.015, 'description': 'Wind power emissions'},
    'solar': {'factor': 0.035, 'description': 'Solar power emissions'}
}

# Home characteristics database
HOME_CHARACTERISTICS = {
    'insulation_quality': {
        'poor': {'factor': 1.5, 'description': 'Poor insulation, high energy loss'},
        'average': {'factor': 1.0, 'description': 'Average insulation'},
        'good': {'factor': 0.8, 'description': 'Good insulation, low energy loss'},
        'excellent': {'factor': 0.6, 'description': 'Excellent insulation, very low energy loss'}
    },
    'window_efficiency': {
        'single_pane': {'factor': 1.4, 'description': 'Single pane windows, high heat loss'},
        'double_pane': {'factor': 1.0, 'description': 'Double pane windows, standard efficiency'},
        'triple_pane': {'factor': 0.7, 'description': 'Triple pane windows, high efficiency'},
        'low_e': {'factor': 0.6, 'description': 'Low-E coating windows, very high efficiency'}
    },
    'home_age': {
        'pre_1950': {'factor': 1.8, 'description': 'Pre-1950 home, typically poor insulation'},
        '1950_1980': {'factor': 1.4, 'description': '1950-1980 home, moderate insulation'},
        '1980_2000': {'factor': 1.1, 'description': '1980-2000 home, better insulation'},
        '2000_2010': {'factor': 0.9, 'description': '2000-2010 home, good insulation'},
        '2010_present': {'factor': 0.7, 'description': '2010-present home, excellent insulation'}
    }
}

# Utility rate information
UTILITY_RATES = {
    'peak_hours': {
        'start': 16,  # 4 PM
        'end': 21,    # 9 PM
        'multiplier': 1.5  # 150% of base rate
    },
    'off_peak_hours': {
        'start': 21,  # 9 PM
        'end': 7,     # 7 AM
        'multiplier': 0.5  # 50% of base rate
    },
    'standard_hours': {
        'start': 7,   # 7 AM
        'end': 16,    # 4 PM
        'multiplier': 1.0  # 100% of base rate
    }
}

# Efficiency improvement options
EFFICIENCY_OPTIONS = {
    'led_retrofit': {
        'cost': 50,
        'savings_percentage': 80,
        'description': 'Replace incandescent bulbs with LED'
    },
    'smart_thermostat': {
        'cost': 200,
        'savings_percentage': 15,
        'description': 'Programmable thermostat for HVAC'
    },
    'energy_star_appliance': {
        'cost': 500,  # varies by appliance
        'savings_percentage': 20,
        'description': 'Replace with ENERGY STAR certified model'
    },
    'solar_panels': {
        'cost': 15000,
        'savings_percentage': 50,
        'description': 'Install solar panels for renewable energy'
    }
}