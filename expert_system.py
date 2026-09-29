"""
Expert System for Home Energy Management Advisor
Core logic for analyzing user inputs and generating personalized recommendations
"""

from knowledge_base import (
    APPLIANCE_DATABASE, 
    UTILITY_RATES, 
    EFFICIENCY_OPTIONS, 
    STRATEGIES, 
    CARBON_INTENSITY_LEVELS,
    ENVIRONMENTAL_FACTORS,
    HOME_CHARACTERISTICS,
    EFFICIENCY_STANDARDS,
    STRATEGIES as COMPLEX_STRATEGIES
)
from strategies import get_cost_savings_recommendations, get_peak_hour_recommendations, get_efficiency_recommendations


class HomeEnergyExpertSystem:
    """
    Expert system for home energy management that provides personalized recommendations
    based on appliance usage, electricity rates, and household characteristics
    """
    
    def __init__(self, electricity_rate_per_kwh=0.12):
        """
        Initialize the expert system with default electricity rate
        :param electricity_rate_per_kwh: Cost per kWh in rupees (default ₹0.12)
        """
        self.electricity_rate_per_kwh = electricity_rate_per_kwh
        self.appliance_database = APPLIANCE_DATABASE
        self.utility_rates = UTILITY_RATES
        self.efficiency_options = EFFICIENCY_OPTIONS
        self.strategies = COMPLEX_STRATEGIES
        self.carbon_intensity_levels = CARBON_INTENSITY_LEVELS
        self.environmental_factors = ENVIRONMENTAL_FACTORS
        self.home_characteristics = HOME_CHARACTERISTICS
        self.efficiency_standards = EFFICIENCY_STANDARDS
        
        # Complex multi-factor rule weights
        self.rule_weights = {
            'cost_impact': 0.3,        # Financial impact weight
            'efficiency_impact': 0.25, # Energy efficiency weight
            'environmental_impact': 0.2, # Environmental impact weight
            'complexity_impact': 0.15, # Implementation complexity weight
            'time_impact': 0.1,        # Time to implement weight
        }
        
        # Initialize complex state for recommendations
        self.recommendation_factors = {
            'appliance_synergies': {},      # How appliances interact
            'time_dependent_loads': [],     # Loads that can be shifted
            'seasonal_variations': {},      # How usage changes by season
            'home_characteristics': {},     # Home-specific factors
            'utility_restrictions': [],     # Utility-specific constraints
            'dependency_chains': [],        # Interdependent recommendations
        }
        
    def calculate_annual_cost(self, appliance_name, hours_per_day=None, age_factor=None, seasonal_factor=None, home_characteristics=None, 
                              usage_pattern_multiplier=1.0, weather_dependence=None):
        """
        Calculate annual energy cost for an appliance with comprehensive factors
        :param appliance_name: Name of the appliance from the database
        :param hours_per_day: Override default daily usage hours
        :param age_factor: Multiplier based on appliance age
        :param seasonal_factor: Multiplier based on season
        :param home_characteristics: Home-specific factors affecting usage
        :param usage_pattern_multiplier: Multiplier based on usage patterns
        :param weather_dependence: How weather affects the appliance's usage
        :return: Annual cost in rupees
        """
        if appliance_name not in self.appliance_database:
            return 0
            
        appliance = self.appliance_database[appliance_name]
        power_kwh = appliance['power_watts'] / 1000  # Convert to kilowatts
        
        # Use provided hours or default from database
        daily_hours = hours_per_day if hours_per_day is not None else appliance['usage_hours_per_day']
        
        # Calculate base annual energy
        annual_hours = daily_hours * 365
        annual_energy_kwh = power_kwh * annual_hours
        
        # Apply complex multipliers
        multiplier = 1.0
        
        # Apply age factor if provided
        if age_factor:
            multiplier *= age_factor
        elif 'age_factor' in appliance:
            # Default to new appliance factor
            multiplier *= appliance['age_factor'].get('new', 1.0)
        
        # Apply seasonal factor if provided
        if seasonal_factor:
            multiplier *= seasonal_factor
        elif 'seasonal_factor' in appliance:
            multiplier *= appliance['seasonal_factor']
        
        # Apply usage pattern multiplier
        multiplier *= usage_pattern_multiplier
        
        # Apply home characteristics if provided
        if home_characteristics:
            # Apply insulation factor if applicable to HVAC
            if appliance_name in ['air_conditioner', 'heater', 'heat_pump', 'evaporative_cooler']:
                insulation_factor = home_characteristics.get('insulation_quality', {}).get('factor', 1.0)
                multiplier *= insulation_factor
                
                # Apply window efficiency if applicable
                window_factor = home_characteristics.get('window_efficiency', {}).get('factor', 1.0)
                multiplier *= window_factor
        
        # Apply weather dependence if provided
        if weather_dependence:
            multiplier *= weather_dependence
        
        # Include standby power consumption
        standby_kwh = (appliance.get('standby_watts', 0) / 1000) * 24 * 365  # Always on standby
        
        # Calculate final cost
        base_cost = annual_energy_kwh * multiplier * self.electricity_rate_per_kwh
        standby_cost = standby_kwh * self.electricity_rate_per_kwh
        total_cost = base_cost + standby_cost
        
        return round(total_cost, 2)
        
    def get_appliance_info(self, appliance_name):
        """
        Get detailed information about an appliance from the knowledge base
        :param appliance_name: Name of the appliance
        :return: Dictionary with appliance information
        """
        return self.appliance_database.get(appliance_name, {})
        
    def analyze_appliance_efficiency(self, appliance_name, appliance_age='new', home_characteristics=None, 
                                   weather_conditions=None, usage_frequency='regular'):
        """
        Analyze the efficiency of an appliance with comprehensive factors
        :param appliance_name: Name of the appliance
        :param appliance_age: Age category of appliance (new, 5_years, 10_years, 15_years)
        :param home_characteristics: Dict containing home characteristics
        :param weather_conditions: Current weather conditions
        :param usage_frequency: How frequently the appliance is used (regular, occasional, intensive)
        :return: Comprehensive efficiency analysis as a string
        """
        if appliance_name not in self.appliance_database:
            return f"Appliance '{appliance_name}' not found in the database."
            
        appliance = self.appliance_database[appliance_name]
        efficiency_rating = appliance['efficiency_rating']
        
        # Calculate base annual cost
        base_annual_cost = self.calculate_annual_cost(appliance_name)
        
        # Calculate cost with age factor
        age_factor = appliance['age_factor'].get(appliance_age, 1.0)
        annual_cost_with_age = self.calculate_annual_cost(
            appliance_name, 
            age_factor=age_factor, 
            home_characteristics=home_characteristics
        )
        
        # Apply weather and usage modifiers
        usage_multipliers = {
            'regular': 1.0,
            'occasional': 0.7,
            'intensive': 1.3
        }
        usage_multiplier = usage_multipliers.get(usage_frequency, 1.0)
        
        seasonal_factor = appliance.get('seasonal_factor', 1.0)
        
        # Calculate environmental impact
        annual_energy_kwh = (appliance['power_watts'] / 1000) * appliance['usage_hours_per_day'] * 365
        age_adjusted_energy = annual_energy_kwh * age_factor * usage_multiplier * seasonal_factor
        
        # Apply complex analysis
        efficiency_score = self._calculate_efficiency_score(appliance, annual_cost_with_age, home_characteristics)
        
        # Determine optimal usage times
        optimal_times = self._determine_optimal_usage_times(appliance_name, home_characteristics)
        
        analysis = f"Comprehensive Analysis for {appliance_name.title()}:\n"
        analysis += f"  Power: {appliance['power_watts']} watts\n"
        analysis += f"  Usage: {appliance['usage_hours_per_day']} hours/day\n"
        analysis += f"  Efficiency Rating: {efficiency_rating}\n"
        analysis += f"  Base Annual Cost: ₹{base_annual_cost}\n"
        analysis += f"  Annual Cost with Age Factor: ₹{annual_cost_with_age}\n"
        analysis += f"  Annual Cost with All Factors: ₹{annual_cost_with_age * usage_multiplier}\n"
        analysis += f"  Age Factor Applied: {age_factor} (for {appliance_age.replace('_', ' ')} appliance)\n"
        analysis += f"  Usage Multiplier: {usage_multiplier} (for {usage_frequency} usage)\n"
        analysis += f"  Seasonal Factor: {seasonal_factor}\n"
        analysis += f"  Standby Power: {appliance.get('standby_watts', 0)} watts\n"
        analysis += f"  Load Shifting Possible: {appliance.get('load_shifting_possible', False)}\n"
        analysis += f"  Smart Features: {', '.join(appliance.get('smart_features', []))}\n"
        analysis += f"  Lifespan: {appliance.get('lifespan_years', 'Unknown')} years\n"
        analysis += f"  Maintenance Frequency: {appliance.get('maintenance_frequency', 'Unknown')}\n"
        analysis += f"  Description: {appliance['description']}\n"
        analysis += f"  Efficiency Score: {efficiency_score:.2f}/10\n"
        
        # Calculate optimal usage times
        analysis += f"  Optimal Usage Times: {', '.join(optimal_times) if optimal_times else 'Any time'}\n"
        
        # Complex efficiency guidance with multiple factors
        recommendations = []
        
        if efficiency_rating == 'very_low':
            recommendations.append("This appliance is very inefficient. Immediate replacement recommended.")
        elif efficiency_rating == 'low':
            recommendations.append("This appliance is inefficient. Replacement recommended.")
        elif efficiency_rating == 'medium':
            recommendations.append("This appliance has moderate efficiency. Upgrades may be beneficial.")
        elif efficiency_rating == 'high':
            recommendations.append("This appliance is quite efficient. Consider maintenance updates.")
        elif efficiency_rating == 'very_high':
            recommendations.append("This appliance is very efficient. Keep using optimally.")
        
        # Additional age-based recommendations
        if age_factor > 1.2:
            recommendations.append(f"This appliance's efficiency has degraded significantly due to age. Replacement may be cost-effective.")
        elif age_factor > 1.1:
            recommendations.append(f"Efficiency has decreased due to age. Consider timing for replacement.")
        
        # Load shifting recommendations
        if appliance.get('load_shifting_possible', False):
            recommendations.append("This appliance's usage can be shifted to off-peak hours to save costs.")
        
        # Maintenance recommendations
        maintenance_freq = appliance.get('maintenance_frequency', 'as_needed')
        if maintenance_freq != 'as_needed':
            recommendations.append(f"Follow the maintenance schedule: {maintenance_freq}")
        
        # Smart features recommendations
        smart_features = appliance.get('smart_features', [])
        if smart_features:
            if 'energy_monitoring' not in smart_features:
                recommendations.append("Consider upgrading to a model with energy monitoring capabilities.")
            if 'scheduling' not in smart_features and appliance.get('load_shifting_possible', False):
                recommendations.append("Scheduling features would help optimize usage timing.")
        else:
            recommendations.append("Smart features could improve efficiency and control.")
        
        # Environmental recommendations
        annual_co2_emissions = self._calculate_co2_emissions(age_adjusted_energy)
        analysis += f"  Annual CO2 Emissions: {annual_co2_emissions:.2f} kg\n"
        
        analysis += "\n  Recommendations:\n"
        for rec in recommendations:
            analysis += f"    - {rec}\n"
            
        return analysis
        
    def _calculate_efficiency_score(self, appliance, annual_cost, home_characteristics):
        """
        Calculate a comprehensive efficiency score based on multiple factors
        """
        # Base score from rating
        rating_scores = {
            'very_low': 1,
            'low': 3,
            'medium': 5,
            'high': 8,
            'very_high': 10
        }
        
        base_score = rating_scores.get(appliance['efficiency_rating'], 5)
        
        # Adjust for power-to-usage ratio (watts per hour of use)
        power_per_use = appliance['power_watts'] / max(appliance['usage_hours_per_day'], 0.1)
        
        # Normalize power per use score (lower is better)
        if power_per_use <= 100:
            power_score = 10
        elif power_per_use <= 500:
            power_score = 7
        elif power_per_use <= 1000:
            power_score = 5
        elif power_per_use <= 2000:
            power_score = 3
        else:
            power_score = 1
            
        # Adjust for annual cost (lower is better)
        cost_score = max(0, 10 - (annual_cost / 100))  # Each ₹100 adds 1 point to deduction
        if annual_cost > 500:
            cost_score = max(1, cost_score)
        
        # Adjust for load shifting capability
        load_shifting_score = 3 if appliance.get('load_shifting_possible', False) else 0
        
        # Adjust for smart features
        smart_features = appliance.get('smart_features', [])
        smart_feature_score = len(smart_features) * 0.5
        if 'energy_monitoring' in smart_features:
            smart_feature_score += 1.0
        if 'scheduling' in smart_features:
            smart_feature_score += 1.0
            
        # Calculate weighted score
        total_score = (
            (base_score * 0.3) + 
            (power_score * 0.25) + 
            (cost_score * 0.2) + 
            (load_shifting_score * 0.15) +
            (smart_feature_score * 0.1)
        )
        
        return min(10, max(0, total_score))  # Cap at 10, floor at 0
    
    def _calculate_co2_emissions(self, annual_energy_kwh):
        """
        Calculate approximate CO2 emissions based on energy usage
        Using average US grid factor of 0.371 kg CO2/kWh
        """
        # Use more realistic US average grid factor
        co2_per_kwh = 0.371  # kg CO2 per kWh
        return annual_energy_kwh * co2_per_kwh

    def _determine_optimal_usage_times(self, appliance_name, home_characteristics=None):
        """
        Determine optimal usage times based on complex factors
        """
        if appliance_name not in self.appliance_database:
            return []
        
        appliance = self.appliance_database[appliance_name]
        if not appliance.get('load_shifting_possible', False):
            return []
        
        # In a complex system, this would check detailed utility rates by time and day
        # For this example, we'll return a list based on general principles
        optimal_times = []
        
        # High energy appliances should use off-peak when possible
        if appliance['power_watts'] > 1000:
            optimal_times.append("Off-peak hours (9PM-7AM)")
        
        # If the appliance benefits from weather (like clothes drying)
        if 'dehumidifier' in appliance_name or 'evaporative_cooler' in appliance_name:
            weather_optimal = "When humidity conditions are favorable"
            optimal_times.append(weather_optimal)
        
        # If the user has solar (this would be determined from home characteristics)
        if home_characteristics and home_characteristics.get('has_solar', False):
            optimal_times.append("During solar production hours (10AM-4PM)")
        
        return optimal_times or ["Any time (no specific optimal period)"]
        
    def analyze_home_energy_usage(self, appliances_list, home_size_sqft=2000, home_characteristics=None, 
                                 seasonal_factor=1.0, weather_conditions=None, electricity_source='mixed'):
        """
        Analyze total energy usage for a list of appliances with comprehensive factors
        :param appliances_list: List of tuples (appliance_name, [optional daily_hours], [optional age])
        :param home_size_sqft: Size of the home in square feet
        :param home_characteristics: Home-specific characteristics
        :param seasonal_factor: Seasonal adjustment factor
        :param weather_conditions: Current weather conditions
        :param electricity_source: Source of electricity (affects environmental impact)
        :return: Dictionary with comprehensive analysis results
        """
        total_annual_cost = 0
        appliance_details = []
        total_co2_emissions = 0
        peak_demand_estimate = 0
        
        for item in appliances_list:
            if isinstance(item, tuple) and len(item) >= 2:
                appliance_name = item[0]
                daily_hours = item[1]
                
                # Extract age if provided (3rd element) or default to 'new'
                if len(item) >= 3:
                    appliance_age = item[2]
                else:
                    appliance_age = 'new'
            else:
                appliance_name = item if isinstance(item, str) else item[0]
                daily_hours = None
                appliance_age = 'new'
                
            if appliance_name in self.appliance_database:
                # Calculate cost with complex factors
                age_factor = self.appliance_database[appliance_name]['age_factor'].get(appliance_age, 1.0)
                
                # Apply weather dependence if applicable
                weather_dependence = 1.0
                if weather_conditions and appliance_name in ['air_conditioner', 'heater', 'heat_pump', 'evaporative_cooler']:
                    # Simplified weather dependence - adjust based on temperature difference from comfort zone
                    comfort_zone = 72  # degrees F
                    current_temp = weather_conditions.get('temperature', 72)
                    if 'air_conditioner' in appliance_name or 'evaporative_cooler' in appliance_name:
                        if current_temp > comfort_zone:
                            # More cooling needed when it's hotter
                            weather_dependence = 1.0 + max(0, (current_temp - comfort_zone) * 0.02)
                    elif 'heater' in appliance_name:
                        if current_temp < comfort_zone:
                            # More heating needed when it's colder
                            weather_dependence = 1.0 + max(0, (comfort_zone - current_temp) * 0.02)
                
                annual_cost = self.calculate_annual_cost(
                    appliance_name, 
                    hours_per_day=daily_hours,
                    age_factor=age_factor,
                    seasonal_factor=seasonal_factor,
                    home_characteristics=home_characteristics,
                    weather_dependence=weather_dependence
                )
                
                # Calculate CO2 emissions
                appliance = self.appliance_database[appliance_name]
                base_energy = (appliance['power_watts'] / 1000) * (daily_hours or appliance['usage_hours_per_day']) * 365
                adjusted_energy = base_energy * age_factor * seasonal_factor * weather_dependence
                co2_emissions = self._calculate_co2_emissions(adjusted_energy)
                
                # Estimate peak demand contribution
                power_kw = appliance['power_watts'] / 1000
                peak_demand_factor = self._get_peak_demand_factor(appliance_name, appliance.get('usage_pattern', 'continuous'))
                peak_contribution = power_kw * peak_demand_factor
                peak_demand_estimate += peak_contribution
                
                appliance_detail = {
                    'name': appliance_name,
                    'annual_cost': annual_cost,
                    'co2_emissions': co2_emissions,
                    'info': self.get_appliance_info(appliance_name),
                    'age_factor': age_factor,
                    'seasonal_factor': seasonal_factor,
                    'efficiency_score': self._calculate_efficiency_score(appliance, annual_cost, home_characteristics),
                    'peak_contribution_kw': peak_contribution,
                    'weather_dependence': weather_dependence,
                    'optimal_usage_times': self._determine_optimal_usage_times(appliance_name, home_characteristics)
                }
                
                appliance_details.append(appliance_detail)
                total_annual_cost += annual_cost
                total_co2_emissions += co2_emissions
        
        # Sort by annual cost (descending)
        appliance_details.sort(key=lambda x: x['annual_cost'], reverse=True)
        
        # Generate comprehensive analysis with multiple perspectives
        analysis = self._generate_comprehensive_energy_analysis(
            appliance_details, 
            total_annual_cost, 
            total_co2_emissions,
            home_size_sqft,
            home_characteristics or {},
            peak_demand_estimate
        )
        
        return {
            'total_annual_cost': round(total_annual_cost, 2),
            'total_co2_emissions': round(total_co2_emissions, 2),
            'estimated_peak_demand_kw': round(peak_demand_estimate, 2),
            'cost_per_sqft': round(total_annual_cost / home_size_sqft, 4) if home_size_sqft > 0 else 0,
            'co2_per_sqft': round(total_co2_emissions / home_size_sqft, 4) if home_size_sqft > 0 else 0,
            'appliance_details': appliance_details,
            'analysis': analysis
        }
    
    def _get_peak_demand_factor(self, appliance_name, usage_pattern):
        """
        Determine how much an appliance contributes to peak demand based on usage pattern
        """
        pattern_factors = {
            'peak': 1.0,  # Used during peak hours
            'continuous': 0.8,  # Always on, so often during peak
            'intermittent': 0.6,  # Sometimes during peak
            'scheduled': 0.5,  # Can be scheduled to avoid peak
            'morning': 0.3,  # Early morning, less likely peak
            'evening': 0.7,  # Evening can overlap with peak
            'overnight': 0.1,  # Mostly off-peak hours
            'on_demand': 0.4,  # Can be shifted based on need
            'humidity_dependent': 0.6,  # Depends on weather/season
            'winter': 0.5,  # Seasonal use
        }
        return pattern_factors.get(usage_pattern, 0.5)
    
    def _generate_comprehensive_energy_analysis(self, appliance_details, total_annual_cost, total_co2_emissions, 
                                              home_size_sqft, home_characteristics, peak_demand_estimate):
        """
        Generate a comprehensive multi-perspective analysis of home energy usage
        """
        analysis = f"Comprehensive Home Energy Usage Analysis\n"
        analysis += f"Total Annual Energy Cost: ₹{total_annual_cost}\n"
        analysis += f"Total CO2 Emissions: {total_co2_emissions:.2f} kg\n"
        analysis += f"Estimated Peak Demand: {peak_demand_estimate:.2f} kW\n"
        analysis += f"Home Size: {home_size_sqft} sq ft\n"
        analysis += f"Cost per Square Foot: ₹{total_annual_cost/home_size_sqft:.3f}\n"
        analysis += f"CO2 per Square Foot: {total_co2_emissions/home_size_sqft:.3f} kg\n\n"
        
        # Add home characteristics analysis
        analysis += "Home Characteristics:\n"
        if home_characteristics:
            for category, value in home_characteristics.items():
                if isinstance(value, dict) and 'description' in value:
                    analysis += f"  {category.title()}: {value.get('description', 'Unknown')}\n"
                else:
                    analysis += f"  {category.title()}: {value}\n"
        else:
            analysis += "  No specific home characteristics provided\n"
        
        # Add efficiency tier analysis
        analysis += f"\nEfficiency Tier Distribution:\n"
        very_efficient = len([a for a in appliance_details if a['efficiency_score'] >= 8])
        efficient = len([a for a in appliance_details if 6 <= a['efficiency_score'] < 8])
        moderate = len([a for a in appliance_details if 4 <= a['efficiency_score'] < 6])
        inefficient = len([a for a in appliance_details if a['efficiency_score'] < 4])
        
        analysis += f"  Very Efficient (8-10): {very_efficient} appliances\n"
        analysis += f"  Efficient (6-7.9): {efficient} appliances\n"
        analysis += f"  Moderate (4-5.9): {moderate} appliances\n"
        analysis += f"  Inefficient (0-3.9): {inefficient} appliances\n\n"
        
        # Top energy consumers
        analysis += f"Top 5 Energy Consumers:\n"
        for i, appliance in enumerate(appliance_details[:5], 1):
            percentage = (appliance['annual_cost'] / total_annual_cost) * 100
            co2_percentage = (appliance['co2_emissions'] / total_co2_emissions * 100) if total_co2_emissions > 0 else 0
            analysis += f"  {i}. {appliance['name'].title()}: ₹{appliance['annual_cost']} ({percentage:.1f}%), {appliance['co2_emissions']:.1f}kg CO2 ({co2_percentage:.1f}%)\n"
        
        # Peak demand analysis
        analysis += f"\nPeak Demand Analysis:\n"
        analysis += f"  Estimated Peak Demand: {peak_demand_estimate:.2f} kW\n"
        if peak_demand_estimate > 10:
            analysis += f"  High peak demand - consider load management strategies\n"
        else:
            analysis += f"  Manageable peak demand\n"
        
        # Environmental impact summary
        analysis += f"\nEnvironmental Impact Summary:\n"
        analysis += f"  Total Annual CO2 Emissions: {total_co2_emissions:.2f} kg\n"
        analysis += f"  Equivalent to {total_co2_emissions / 4800:.2f} cars driven 1 year (approx.)\n"  # Updated per-car estimate
        
        # Age-related efficiency degradation
        total_efficiency_loss = 0
        affected_appliances = []
        for appliance in appliance_details:
            age_factor = appliance['age_factor']
            if age_factor > 1.1:  # More than 10% degradation
                loss = (age_factor - 1.0) * appliance['annual_cost']
                total_efficiency_loss += loss
                affected_appliances.append((appliance['name'], loss))
        
        if affected_appliances:
            analysis += f"\nEfficiency Loss Due to Age:\n"
            analysis += f"  Total Additional Cost: ₹{total_efficiency_loss:.2f} annually\n"
            analysis += f"  Affected Appliances:\n"
            for name, loss in sorted(affected_appliances, key=lambda x: x[1], reverse=True):
                analysis += f"    - {name}: ₹{loss:.2f} annually\n"
        
        # Load shifting opportunities
        shift_opportunities = [a for a in appliance_details if a['info'].get('load_shifting_possible', False)]
        if shift_opportunities:
            analysis += f"\nLoad Shifting Opportunities:\n"
            analysis += f"  Appliances that can shift usage: {len(shift_opportunities)}\n"
            for appliance in shift_opportunities[:5]:  # Top 5
                analysis += f"    - {appliance['name']}: {', '.join(appliance['optimal_usage_times'])}\n"
        
        return analysis
    
    def _evaluate_time_of_use_optimization(self, appliances_list, home_characteristics=None):
        """
        Evaluate complex time-of-use optimization opportunities
        """
        optimization_opportunities = []
        
        for item in appliances_list:
            appliance_name = item[0] if isinstance(item, tuple) else item
            daily_hours = item[1] if isinstance(item, tuple) and len(item) > 1 else self.appliance_database[appliance_name]['usage_hours_per_day']
            
            if appliance_name in self.appliance_database:
                appliance = self.appliance_database[appliance_name]
                
                if appliance.get('load_shifting_possible', False):
                    # Calculate potential savings from time shifting
                    power_kwh = appliance['power_watts'] / 1000
                    annual_energy = power_kwh * daily_hours * 365
                    
                    # Find best rate periods for shifting
                    potential_savings = self._calculate_time_shifting_savings(
                        appliance_name, 
                        annual_energy, 
                        home_characteristics
                    )
                    
                    if potential_savings > 5:  # Only include if significant savings
                        optimization_opportunities.append({
                            'appliance': appliance_name,
                            'potential_savings': potential_savings,
                            'description': f"Can shift {appliance_name} usage to save ₹{potential_savings:.2f} annually",
                            'complexity': 'low' if 'scheduling' in appliance.get('smart_features', []) else 'medium'
                        })
        
        return optimization_opportunities
    
    def _calculate_time_shifting_savings(self, appliance_name, annual_energy, home_characteristics):
        """
        Calculate potential savings from time shifting based on complex rate structures
        """
        # A more realistic calculation would use the complex utility rates
        # For now, we'll use a simplified approach but with multiple rate periods
        peak_cost = annual_energy * self.electricity_rate_per_kwh * 1.5  # Assume peak rate
        off_peak_cost = annual_energy * self.electricity_rate_per_kwh * 0.5  # Off-peak rate
        
        return peak_cost - off_peak_cost
    
    def generate_recommendations(self, appliances_list, peak_hours_usage=None, home_size_sqft=2000, 
                               home_characteristics=None, electricity_source='mixed', weather_conditions=None):
        """
        Generate highly personalized energy saving recommendations with complex multi-factor analysis
        :param appliances_list: List of appliances in use
        :param peak_hours_usage: Information about peak hour usage
        :param home_size_sqft: Home size in square feet
        :param home_characteristics: Home-specific characteristics
        :param electricity_source: Source of electricity (affects environmental impact)
        :param weather_conditions: Current weather conditions
        :return: Dictionary with comprehensive recommendations
        """
        # Calculate baseline analysis
        baseline_analysis = self.analyze_home_energy_usage(
            appliances_list, home_size_sqft, home_characteristics, 
            weather_conditions=weather_conditions, electricity_source=electricity_source
        )
        
        # Get standard recommendations
        cost_savings = get_cost_savings_recommendations(appliances_list, self.appliance_database, self.electricity_rate_per_kwh)
        peak_hour = get_peak_hour_recommendations(appliances_list, peak_hours_usage, self.utility_rates, self.appliance_database)
        efficiency = get_efficiency_recommendations(appliances_list, self.appliance_database)
        
        # Apply complex multi-factor analysis
        complex_recommendations = self._generate_complex_recommendations(
            appliances_list, baseline_analysis, home_characteristics, weather_conditions
        )
        
        # Add time-of-use optimization
        time_optimization = self._evaluate_time_of_use_optimization(appliances_list, home_characteristics)
        
        # Calculate environmental recommendations based on electricity source
        environmental_recommendations = self._generate_environmental_recommendations(
            appliances_list, electricity_source, baseline_analysis['total_co2_emissions']
        )
        
        # Calculate demand reduction recommendations
        demand_recommendations = self._generate_demand_reduction_recommendations(
            appliances_list, baseline_analysis['estimated_peak_demand_kw']
        )
        
        # Combine all recommendations with priority scoring
        all_recommendations = {
            'cost_savings': self._prioritize_recommendations(cost_savings, 'cost'),
            'peak_hour': self._prioritize_recommendations(peak_hour, 'time'),
            'efficiency': self._prioritize_recommendations(efficiency, 'efficiency'),
            'complex_analysis': complex_recommendations,
            'time_optimization': time_optimization,
            'environmental': environmental_recommendations,
            'demand_reduction': demand_recommendations,
            'general_strategies': self._apply_general_strategies(appliances_list, home_characteristics)
        }
        
        # Calculate comprehensive potential savings
        potential_savings = self._calculate_total_potential_savings(all_recommendations)
        
        return {
            'recommendations': all_recommendations,
            'potential_annual_savings': round(potential_savings, 2),
            'potential_co2_reduction': self._estimate_co2_reduction(all_recommendations),
            'priority_score': self._calculate_recommendation_priority(all_recommendations),
            'dependency_chains': self._identify_dependency_chains(all_recommendations),
            'summary': f"Potential to save ₹{round(potential_savings, 2)} annually with {self._estimate_co2_reduction(all_recommendations):.1f} kg CO2 reduction"
        }
    
    def _generate_complex_recommendations(self, appliances_list, baseline_analysis, home_characteristics, weather_conditions):
        """
        Generate complex recommendations based on multi-factor analysis
        """
        recommendations = []
        
        # Analyze appliance synergies and interactions
        appliance_synergies = self._analyze_appliance_synergies(appliances_list, home_characteristics)
        
        # Check for high-impact combinations
        hvac_appliances = []
        for item in appliances_list:
            appliance_name = item[0] if isinstance(item, tuple) else item
            if any(hvac in appliance_name for hvac in ['air_conditioner', 'heater', 'heat_pump', 'evaporative_cooler']):
                hvac_appliances.append(appliance_name)
        
        if len(hvac_appliances) > 1:
            # Multiple HVAC systems may be inefficient
            recommendations.append({
                'type': 'hvac_duplication',
                'message': f'Multiple HVAC systems detected ({", ".join(hvac_appliances)}) - consider optimizing system usage to avoid redundancy',
                'priority': 'high',
                'potential_savings': 150,
                'implementation_complexity': 'medium',
                'category': 'hvac'
            })
        
        # Analyze age-related degradation patterns
        old_appliances = []
        for item in appliances_list:
            appliance_name = item[0] if isinstance(item, tuple) else item
            appliance_age = item[2] if isinstance(item, tuple) and len(item) > 2 else 'new'
            
            if appliance_name in self.appliance_database:
                age_factor = self.appliance_database[appliance_name]['age_factor'].get(appliance_age, 1.0)
                if age_factor > 1.25:  # Significant degradation
                    old_appliances.append({
                        'appliance': appliance_name,
                        'age_factor': age_factor,
                        'info': self.appliance_database[appliance_name]
                    })
        
        if old_appliances:
            total_potential_savings = 0
            for old_appliance in old_appliances:
                # Calculate potential savings from replacement
                current_cost = self.calculate_annual_cost(old_appliance['appliance'])
                # Estimate new appliance cost at 1.0 factor
                new_cost = current_cost / old_appliance['age_factor']
                potential_savings = current_cost - new_cost
                total_potential_savings += potential_savings
            
            recommendations.append({
                'type': 'age_efficiency_degradation',
                'message': f'Age-related efficiency degradation affecting {len(old_appliances)} appliances causing ₹{total_potential_savings:.2f} in excess costs',
                'priority': 'medium',
                'potential_savings': total_potential_savings,
                'appliances_affected': [oa['appliance'] for oa in old_appliances],
                'implementation_complexity': 'high',
                'category': 'efficiency'
            })
        
        # Analyze standby power consumption
        total_standby = sum(
            self.appliance_database[item[0] if isinstance(item, tuple) else item].get('standby_watts', 0)
            for item in appliances_list
            if (item[0] if isinstance(item, tuple) else item) in self.appliance_database
        )
        
        standby_annual_cost = (total_standby / 1000) * 24 * 365 * self.electricity_rate_per_kwh
        if standby_annual_cost > 50:  # More than ₹50/year in standby
            recommendations.append({
                'type': 'phantom_load',
                'message': f'High standby power consumption ({total_standby}W) costing ₹{standby_annual_cost:.2f} annually',
                'priority': 'medium',
                'potential_savings': standby_annual_cost * 0.8,  # Could eliminate 80% with smart plugs
                'implementation_complexity': 'low',
                'category': 'standby'
            })
        
        # Analyze seasonal patterns and suggest adjustments
        if weather_conditions:
            temp = weather_conditions.get('temperature', 72)
            season = self._get_current_season()
            
            if season == 'summer' and temp > 80:
                ac_appliances = [item[0] if isinstance(item, tuple) else item for item in appliances_list 
                                if 'air_conditioner' in (item[0] if isinstance(item, tuple) else item)]
                if ac_appliances:
                    recommendations.append({
                        'type': 'cooling_optimization',
                        'message': f'High cooling demand detected. Consider running AC during cooler parts of the day to reduce strain and costs',
                        'priority': 'high',
                        'potential_savings': len(ac_appliances) * 50,
                        'implementation_complexity': 'medium',
                        'category': 'seasonal'
                    })
        
        return recommendations
    
    def _analyze_appliance_synergies(self, appliances_list, home_characteristics):
        """
        Analyze potential synergies between appliances
        """
        synergies = []
        
        # Check for water heating and HVAC interactions
        has_water_heater = any(
            'water_heater' in (item[0] if isinstance(item, tuple) else item)
            for item in appliances_list
        )
        
        has_hvac = any(
            appliance_name in ['air_conditioner', 'heater', 'heat_pump', 'evaporative_cooler']
            for item in appliances_list
            for appliance_name in [item[0] if isinstance(item, tuple) else item]
        )
        
        if has_water_heater and has_hvac:
            synergies.append({
                'type': 'water_heating_hvac',
                'description': 'Water heating and HVAC may have synergistic efficiency opportunities',
                'opportunities': ['scheduling coordination', 'energy source optimization'],
                'estimated_savings': 75
            })
        
        # Check for laundry and water heating synergy
        has_washer = any(
            'washing_machine' in (item[0] if isinstance(item, tuple) else item)
            for item in appliances_list
        )
        
        if has_washer and has_water_heater:
            synergies.append({
                'type': 'laundry_water_heating',
                'description': 'Washing machine and water heater can be coordinated for efficiency',
                'opportunities': ['run washer with water heater in off-peak hours'],
                'estimated_savings': 30
            })
        
        return synergies
    
    def _generate_environmental_recommendations(self, appliances_list, electricity_source, baseline_co2):
        """
        Generate environmental impact recommendations
        """
        recommendations = []
        
        # Calculate environmental factor based on electricity source
        env_factor = self.environmental_factors.get(electricity_source, self.environmental_factors['natural_gas'])
        
        # High CO2 impact appliances
        high_impact_appliances = []
        for item in appliances_list:
            appliance_name = item[0] if isinstance(item, tuple) else item
            
            if appliance_name in self.appliance_database:
                appliance = self.appliance_database[appliance_name]
                power_kwh = appliance['power_watts'] / 1000
                annual_hours = appliance['usage_hours_per_day'] * 365
                annual_energy = power_kwh * annual_hours
                co2_impact = annual_energy * env_factor['factor']
                
                if co2_impact > 500:  # High impact threshold
                    high_impact_appliances.append({
                        'appliance': appliance_name,
                        'co2_impact': co2_impact,
                        'energy_kwh': annual_energy
                    })
        
        if high_impact_appliances:
            recommendations.append({
                'type': 'high_co2_impact',
                'message': f'High environmental impact from {len(high_impact_appliances)} appliances: ' + 
                          ', '.join([h['appliance'] for h in high_impact_appliances]),
                'priority': 'high',
                'co2_reduction_potential': sum(h['co2_impact'] for h in high_impact_appliances) * 0.3,  # 30% reduction potential
                'implementation_complexity': 'medium',
                'category': 'environmental'
            })
        
        # Renewable energy recommendation
        total_annual_kwh = sum(
            (self.appliance_database[item[0] if isinstance(item, tuple) else item]['power_watts'] / 1000) * 
            self.appliance_database[item[0] if isinstance(item, tuple) else item]['usage_hours_per_day'] * 365
            for item in appliances_list
            if (item[0] if isinstance(item, tuple) else item) in self.appliance_database
        )
        
        if total_annual_kwh > 8000:  # High energy usage
            recommendations.append({
                'type': 'renewable_energy',
                'message': 'High energy usage makes renewable energy investment potentially cost-effective',
                'priority': 'medium',
                'estimated_co2_reduction': total_annual_kwh * env_factor['factor'] * 0.8,  # 80% reduction
                'implementation_complexity': 'high',
                'category': 'renewable'
            })
        
        # Time-of-use recommendations for environmental benefit
        time_sensitive_appliances = [
            item[0] if isinstance(item, tuple) else item
            for item in appliances_list
            if (item[0] if isinstance(item, tuple) else item) in self.appliance_database
            and self.appliance_database[(item[0] if isinstance(item, tuple) else item)].get('load_shifting_possible', False)
        ]
        
        if time_sensitive_appliances:
            recommendations.append({
                'type': 'time_based_environmental',
                'message': f'Schedule {len(time_sensitive_appliances)} appliances during times of cleaner energy generation',
                'priority': 'medium',
                'estimated_co2_reduction': len(time_sensitive_appliances) * 50,  # Estimate
                'implementation_complexity': 'low',
                'category': 'scheduling'
            })
        
        return recommendations
    
    def _generate_demand_reduction_recommendations(self, appliances_list, peak_demand_kw):
        """
        Generate recommendations to reduce peak demand
        """
        recommendations = []
        
        if peak_demand_kw > 15:  # High peak demand
            recommendations.append({
                'type': 'peak_demand_reduction',
                'message': f'High estimated peak demand of {peak_demand_kw:.2f} kW. Consider load management strategies.',
                'priority': 'high',
                'potential_savings': 100,  # From reduced demand charges
                'implementation_complexity': 'medium',
                'category': 'demand'
            })
        
        # Identify high-demand appliances during peak times
        high_demand_appliances = []
        for item in appliances_list:
            appliance_name = item[0] if isinstance(item, tuple) else item
            if appliance_name in self.appliance_database:
                power_kw = self.appliance_database[appliance_name]['power_watts'] / 1000
                if power_kw > 2 and self.appliance_database[appliance_name].get('load_shifting_possible', False):
                    high_demand_appliances.append(appliance_name)
        
        if high_demand_appliances:
            recommendations.append({
                'type': 'high_demand_shifting',
                'message': f'Consider shifting high-demand appliances ({", ".join(high_demand_appliances)}) to off-peak hours',
                'priority': 'high',
                'potential_savings': len(high_demand_appliances) * 75,
                'implementation_complexity': 'medium',
                'category': 'demand'
            })
        
        return recommendations
    
    def _apply_general_strategies(self, appliances_list, home_characteristics):
        """
        Apply general strategies based on the appliance list and home characteristics
        """
        strategy_recommendations = []
        
        # Identify applicable strategies
        for strategy_key, strategy in self.strategies.items():
            applicable_appliances = []
            for item in appliances_list:
                appliance_name = item[0] if isinstance(item, tuple) else item
                if appliance_name in strategy['appliances_affected']:
                    applicable_appliances.append(appliance_name)
            
            if applicable_appliances and strategy['savings_potential'] > 10:
                strategy_recommendations.append({
                    'strategy': strategy_key,
                    'name': strategy['name'],
                    'description': strategy['description'],
                    'appliances_affected': applicable_appliances,
                    'savings_potential': strategy['savings_potential'],
                    'complexity': strategy['complexity'],
                    'message': f"{strategy['name']}: {strategy['description']} for {', '.join(applicable_appliances[:3])}",
                    'priority': 'high' if strategy['savings_potential'] > 20 else 'medium'
                })
        
        return strategy_recommendations
    
    def _prioritize_recommendations(self, recommendations, category):
        """
        Prioritize recommendations using complex multi-factor scoring
        """
        for rec in recommendations:
            # Calculate priority score based on multiple factors
            cost_factor = rec.get('potential_savings', 0) / 100  # Normalize by ₹100
            effort_factor = 1.0 if rec.get('priority') == 'high' else 0.7 if rec.get('priority') == 'medium' else 0.4
            impact_factor = 0.5  # Default impact
            
            # Calculate weighted priority score
            priority_score = (
                (cost_factor * self.rule_weights['cost_impact']) +
                (effort_factor * self.rule_weights['complexity_impact']) +
                (impact_factor * self.rule_weights['efficiency_impact'])
            )
            
            rec['priority_score'] = priority_score
        
        # Sort by priority score (descending)
        recommendations.sort(key=lambda x: x.get('priority_score', 0), reverse=True)
        return recommendations
    
    def _calculate_total_potential_savings(self, all_recommendations):
        """
        Calculate total potential savings across all recommendation categories
        """
        total_savings = 0
        
        for category in all_recommendations.values():
            if isinstance(category, list):
                for rec in category:
                    if isinstance(rec, dict):
                        total_savings += rec.get('potential_savings', 0)
        
        return total_savings
    
    def _estimate_co2_reduction(self, all_recommendations):
        """
        Estimate potential CO2 reduction from all recommendations
        """
        total_reduction = 0
        
        for category in all_recommendations.values():
            if isinstance(category, list):
                for rec in category:
                    if isinstance(rec, dict):
                        # Look for co2 reduction in various keys
                        reduction = (rec.get('co2_reduction_potential', 0) or 
                                   rec.get('estimated_co2_reduction', 0) or
                                   rec.get('co2_reduction', 0))
                        total_reduction += reduction
                    elif isinstance(rec, dict) and 'environmental' in str(rec):
                        # Handle complex environmental rec objects
                        pass  # Handled in other parts
        
        return total_reduction
    
    def _calculate_recommendation_priority(self, all_recommendations):
        """
        Calculate an overall priority score for the recommendation set
        """
        total_priority = 0
        count = 0
        
        for category in all_recommendations.values():
            if isinstance(category, list):
                for rec in category:
                    if isinstance(rec, dict):
                        total_priority += rec.get('priority_score', rec.get('potential_savings', 0) / 100)
                        count += 1
        
        return total_priority / count if count > 0 else 0
    
    def _identify_dependency_chains(self, all_recommendations):
        """
        Identify dependencies between recommendations (e.g., thermostat before HVAC efficiency)
        """
        dependencies = []
        
        # Check for common dependencies
        has_smart_thermostat = any(
            'smart_thermostat' in (rec.get('type', '') or rec.get('appliance', ''))
            for category in all_recommendations.values()
            if isinstance(category, list)
            for rec in category
            if isinstance(rec, dict)
        )
        
        has_hvac = any(
            'hvac' in (rec.get('type', '') or rec.get('category', ''))
            for category in all_recommendations.values()
            if isinstance(category, list)
            for rec in category
            if isinstance(rec, dict)
        )
        
        if has_hvac and not has_smart_thermostat:
            dependencies.append({
                'dependency': 'smart_thermostat_before_hvac',
                'message': 'Install smart thermostat before implementing HVAC efficiency measures',
                'priority': 'high'
            })
        
        return dependencies
    
    def get_time_based_recommendations(self, appliance_name, current_usage_time='peak', home_characteristics=None, weather_conditions=None):
        """
        Get sophisticated time-based recommendations considering multiple factors
        :param appliance_name: Name of the appliance
        :param current_usage_time: Current usage time ('peak', 'standard', 'off_peak')
        :param home_characteristics: Home-specific characteristics
        :param weather_conditions: Current weather conditions
        :return: Time-based recommendation with multiple considerations
        """
        if appliance_name not in self.appliance_database:
            return "Appliance not found in database."
            
        appliance = self.appliance_database[appliance_name]
        power_kwh = appliance['power_watts'] / 1000
        daily_hours = appliance['usage_hours_per_day']
        seasonal_factor = appliance.get('seasonal_factor', 1.0)
        
        # Calculate usage profile complexity
        load_shiftable = appliance.get('load_shifting_possible', False)
        smart_features = appliance.get('smart_features', [])
        
        if not load_shiftable:
            return f"Usage of {appliance_name} cannot be shifted to different times for cost savings."
        
        # Calculate current cost
        current_cost = self._calculate_time_based_cost(appliance_name, current_usage_time, home_characteristics)
        
        # Check for weather-sensitive appliances
        weather_sensitive = 'air_conditioner' in appliance_name or 'heater' in appliance_name or 'evaporative_cooler' in appliance_name
        if weather_sensitive and weather_conditions:
            temp = weather_conditions.get('temperature', 72)
            if 'air_conditioner' in appliance_name and temp > 90:
                # High cooling demand - recommend avoiding highest peak hours if possible
                pass
        
        # Calculate costs for all possible time periods
        time_costs = {}
        for rate_period, rate_info in self.utility_rates.items():
            if rate_info.get('season', 'all') == 'all' or rate_info.get('season') == self._get_current_season():
                # Calculate cost for this time period
                rate_multiplier = rate_info['multiplier']
                adjusted_cost = power_kwh * daily_hours * 365 * seasonal_factor * self.electricity_rate_per_kwh * rate_multiplier
                time_costs[rate_period] = adjusted_cost
        
        # Find best alternative option
        if time_costs:
            best_period = min(time_costs, key=time_costs.get)
            best_cost = time_costs[best_period]
            potential_savings = current_cost - best_cost
            
            if potential_savings > 0:
                # Detailed time-based recommendation
                recommendation = f"For {appliance_name}, you could save ₹{potential_savings:.2f} annually by shifting usage to the {best_period.replace('_', ' ').title()} period."
                
                # Add smart feature consideration
                if 'scheduling' in smart_features:
                    recommendation += f" With smart scheduling features, this optimization can be automated."
                
                # Add weather consideration if applicable
                if weather_sensitive and weather_conditions:
                    temp = weather_conditions.get('temperature', 72)
                    if 'air_conditioner' in appliance_name and temp > 90:
                        recommendation += f" However, during extreme heat, cooling needs may override cost savings."
                    elif 'heater' in appliance_name and temp < 40:
                        recommendation += f" During extreme cold, heating needs may override cost savings."
                
                # Add implementation complexity
                if 'scheduling' in smart_features:
                    implementation = "Easy implementation with scheduling feature."
                elif 'timer' in smart_features:
                    implementation = "Moderate implementation with timer feature."
                else:
                    implementation = "Requires manual timing adjustment or smart device."
                
                return f"{recommendation} ({implementation})"
            else:
                return f"Current usage time for {appliance_name} appears to be optimal."
        else:
            return f"Could not determine optimal time for {appliance_name} due to insufficient rate information."
    
    def _calculate_time_based_cost(self, appliance_name, usage_time, home_characteristics=None):
        """
        Calculate time-based cost using complex rate structures
        """
        appliance = self.appliance_database[appliance_name]
        power_kwh = appliance['power_watts'] / 1000
        daily_hours = appliance['usage_hours_per_day']
        seasonal_factor = appliance.get('seasonal_factor', 1.0)
        
        # For this example, we'll use simplified calculation
        # In a real system, this would use the complex utility rates
        if usage_time == 'peak':
            rate_multiplier = 1.5
        elif usage_time == 'off_peak':
            rate_multiplier = 0.5
        else:  # standard
            rate_multiplier = 1.0
        
        return power_kwh * daily_hours * 365 * seasonal_factor * self.electricity_rate_per_kwh * rate_multiplier
    
    def _get_current_season(self):
        """
        Determine the current season for utility rate selection
        """
        from datetime import datetime
        month = datetime.now().month
        if month in [12, 1, 2]:
            return 'winter'
        elif month in [6, 7, 8]:
            return 'summer'
        else:
            return 'shoulder'  # Spring/fall
    
    def _calculate_complex_efficiency_score(self, appliance, home_characteristics, usage_pattern):
        """
        Calculate a complex efficiency score based on multiple factors
        """
        # This would incorporate complex calculations based on
        # appliance characteristics, home characteristics, and usage patterns
        base_score = self._calculate_efficiency_score(appliance, 0, home_characteristics)  # Placeholder
        return base_score
