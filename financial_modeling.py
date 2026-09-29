"""
Financial Modeling for Home Energy Management Advisor
Calculates ROI, payback periods, and financial benefits of energy improvements
"""

from typing import Dict, List
from datetime import datetime
from utils import format_currency


class FinancialModeling:
    """
    Financial analysis engine for energy-related investments
    """
    
    def __init__(self, electricity_rate_per_kwh=0.12):
        self.electricity_rate = electricity_rate_per_kwh
        self.inflation_rate = 0.025  # 2.5% annual inflation
        self.discount_rate = 0.05    # 5% discount rate for NPV calculations
    
    def calculate_appliance_roi(self, appliance_name: str, 
                               new_appliance_name: str, 
                               purchase_cost: float,
                               lifetime_years: int = 10) -> Dict:
        """
        Calculate ROI for replacing an appliance with a more efficient one
        """
        from knowledge_base import APPLIANCE_DATABASE
        
        if appliance_name not in APPLIANCE_DATABASE or new_appliance_name not in APPLIANCE_DATABASE:
            return {'error': 'Appliance not found in database'}
        
        old_appliance = APPLIANCE_DATABASE[appliance_name]
        new_appliance = APPLIANCE_DATABASE[new_appliance_name]
        
        # Calculate annual energy usage and costs
        old_power_kwh = old_appliance['power_watts'] / 1000
        new_power_kwh = new_appliance['power_watts'] / 1000
        
        daily_hours = old_appliance.get('usage_hours_per_day', 1)
        
        old_annual_energy = old_power_kwh * daily_hours * 365
        new_annual_energy = new_power_kwh * daily_hours * 365
        
        old_annual_cost = old_annual_energy * self.electricity_rate
        new_annual_cost = new_annual_energy * self.electricity_rate
        
        annual_savings = old_annual_cost - new_annual_cost
        
        # Calculate payback period
        if annual_savings > 0:
            simple_payback = purchase_cost / annual_savings
        else:
            simple_payback = float('inf')
        
        # Calculate NPV over lifetime
        npv = -purchase_cost  # Initial investment
        for year in range(1, lifetime_years + 1):
            # Account for inflation in energy costs
            energy_cost_factor = (1 + self.inflation_rate) ** year
            discounted_cash_flow = (annual_savings * energy_cost_factor) / ((1 + self.discount_rate) ** year)
            npv += discounted_cash_flow
        
        # Calculate IRR (simplified)
        if simple_payback != float('inf'):
            irr_approx = (annual_savings / purchase_cost) * 2  # Rough approximation
        else:
            irr_approx = 0
        
        return {
            'appliance_comparison': {
                'old': {
                    'name': appliance_name,
                    'power_watts': old_appliance['power_watts'],
                    'annual_energy_kwh': round(old_annual_energy, 2),
                    'annual_cost': round(old_annual_cost, 2)
                },
                'new': {
                    'name': new_appliance_name,
                    'power_watts': new_appliance['power_watts'],
                    'annual_energy_kwh': round(new_annual_energy, 2),
                    'annual_cost': round(new_annual_cost, 2)
                }
            },
            'investment': {
                'purchase_cost': round(purchase_cost, 2),
                'lifetime_years': lifetime_years
            },
            'financial_metrics': {
                'annual_savings': round(annual_savings, 2),
                'simple_payback_years': round(simple_payback, 2) if simple_payback != float('inf') else 'Infinite',
                'npv': round(npv, 2),
                'approximate_irr': round(irr_approx * 100, 2) if irr_approx != float('inf') else 0,
                'total_savings_over_lifetime': round(annual_savings * lifetime_years, 2)
            }
        }
    
    def calculate_solar_roi(self, system_size_kw: float, 
                          installation_cost: float,
                          annual_production_kwh: float,
                          lifetime_years: int = 25) -> Dict:
        """
        Calculate ROI for solar panel installation
        """
        # Calculate annual energy savings
        annual_value = annual_production_kwh * self.electricity_rate
        
        # Account for degradation (typically 0.5-1% per year)
        total_production = 0
        yearly_production = annual_production_kwh
        degradation_rate = 0.005  # 0.5% annual degradation
        
        for year in range(lifetime_years):
            total_production += yearly_production
            yearly_production *= (1 - degradation_rate)
        
        # Calculate total value over lifetime
        total_value = 0
        yearly_production = annual_production_kwh
        energy_cost_multiplier = 1
        
        for year in range(lifetime_years):
            yearly_value = yearly_production * self.electricity_rate * energy_cost_multiplier
            # Discount future cash flows
            present_value = yearly_value / ((1 + self.discount_rate) ** year)
            total_value += present_value
            # Account for inflation in electricity rates
            energy_cost_multiplier *= (1 + self.inflation_rate)
            yearly_production *= (1 - degradation_rate)
        
        # Calculate financial metrics
        simple_payback = installation_cost / annual_value if annual_value > 0 else float('inf')
        npv = total_value - installation_cost
        irr_approx = (annual_value / installation_cost) * 2 if annual_value > 0 else 0
        
        return {
            'investment': {
                'system_size_kw': system_size_kw,
                'installation_cost': round(installation_cost, 2),
                'annual_production_kwh': round(annual_production_kwh, 2),
                'lifetime_years': lifetime_years
            },
            'financial_metrics': {
                'annual_energy_value': round(annual_value, 2),
                'simple_payback_years': round(simple_payback, 2) if simple_payback != float('inf') else 'Infinite',
                'npv': round(npv, 2),
                'approximate_irr': round(irr_approx * 100, 2) if irr_approx != float('inf') else 0,
                'total_value_over_lifetime': round(total_value, 2),
                'total_cost_reduction': round(total_value, 2)  # Assuming equivalent value
            }
        }
    
    def calculate_battery_storage_roi(self, capacity_kwh: float,
                                    power_kw: float,
                                    installation_cost: float,
                                    efficiency: float = 0.9,
                                    cycles_per_year: int = 300,
                                    lifetime_years: int = 15) -> Dict:
        """
        Calculate ROI for battery storage system
        """
        # Calculate how much energy can be arbitrage'd
        # Energy arbitrage: charge during low-rate hours, discharge during high-rate hours
        # For simplicity, assume ₹0.10 price difference between low and high rate periods
        price_difference = 0.10  # ₹0.10/kWh difference
        annual_arbitrage_cycles = cycles_per_year
        energy_per_cycle = capacity_kwh * efficiency * 0.8  # 80% depth of discharge
        
        annual_arbitrage_value = annual_arbitrage_cycles * energy_per_cycle * price_difference
        
        # Calculate time-shifting value (using stored energy during peak demand)
        # Assume saving 20% on peak demand charges
        estimated_monthly_demand_charge = 100  # Placeholder
        monthly_savings = estimated_monthly_demand_charge * 0.2
        annual_demand_savings = monthly_savings * 12
        
        total_annual_value = annual_arbitrage_value + annual_demand_savings
        
        # Calculate financial metrics
        simple_payback = installation_cost / total_annual_value if total_annual_value > 0 else float('inf')
        
        # NPV calculation with inflation and discounting
        npv = -installation_cost
        for year in range(1, lifetime_years + 1):
            energy_cost_factor = (1 + self.inflation_rate) ** year
            annual_value_with_growth = total_annual_value * energy_cost_factor
            discounted_cash_flow = annual_value_with_growth / ((1 + self.discount_rate) ** year)
            npv += discounted_cash_flow
        
        irr_approx = (total_annual_value / installation_cost) * 2 if total_annual_value > 0 else 0
        
        return {
            'investment': {
                'capacity_kwh': capacity_kwh,
                'power_kw': power_kw,
                'installation_cost': round(installation_cost, 2),
                'efficiency': efficiency,
                'lifetime_years': lifetime_years
            },
            'financial_metrics': {
                'annual_arbitrage_value': round(annual_arbitrage_value, 2),
                'annual_demand_savings': round(annual_demand_savings, 2),
                'total_annual_value': round(total_annual_value, 2),
                'simple_payback_years': round(simple_payback, 2) if simple_payback != float('inf') else 'Infinite',
                'npv': round(npv, 2),
                'approximate_irr': round(irr_approx * 100, 2) if irr_approx != float('inf') else 0
            }
        }
    
    def calculate_program_roi(self, program_type: str, 
                            investment_amount: float,
                            annual_savings: float,
                            lifetime_years: int = 10) -> Dict:
        """
        Calculate ROI for various energy efficiency programs
        """
        # Calculate financial metrics
        simple_payback = investment_amount / annual_savings if annual_savings > 0 else float('inf')
        
        # NPV calculation
        npv = -investment_amount
        for year in range(1, lifetime_years + 1):
            energy_cost_factor = (1 + self.inflation_rate) ** year
            annual_value_with_growth = annual_savings * energy_cost_factor
            discounted_cash_flow = annual_value_with_growth / ((1 + self.discount_rate) ** year)
            npv += discounted_cash_flow
        
        # Calculate IRR approximation
        if investment_amount != 0:
            irr_approx = (annual_savings / investment_amount) * 2
        else:
            irr_approx = 0
        
        total_savings = annual_savings * lifetime_years
        
        return {
            'program': {
                'type': program_type,
                'investment_amount': round(investment_amount, 2),
                'annual_savings': round(annual_savings, 2),
                'lifetime_years': lifetime_years
            },
            'financial_metrics': {
                'simple_payback_years': round(simple_payback, 2) if simple_payback != float('inf') else 'Infinite',
                'npv': round(npv, 2),
                'approximate_irr': round(irr_approx * 100, 2),
                'total_savings_over_lifetime': round(total_savings, 2),
                'profit_margin': round((total_savings - investment_amount) / investment_amount * 100, 2) if investment_amount > 0 else 0
            }
        }
    
    def calculate_demand_charge_reduction(self, current_demand_kw: float,
                                        reduced_demand_kw: float,
                                        demand_charge_per_kw: float) -> Dict:
        """
        Calculate savings from demand charge reduction
        """
        monthly_savings = (current_demand_kw - reduced_demand_kw) * demand_charge_per_kw
        annual_savings = monthly_savings * 12
        
        return {
            'demand_analysis': {
                'current_demand_kw': current_demand_kw,
                'reduced_demand_kw': reduced_demand_kw,
                'demand_reduction_kw': round(current_demand_kw - reduced_demand_kw, 2)
            },
            'savings': {
                'monthly_savings': round(monthly_savings, 2),
                'annual_savings': round(annual_savings, 2)
            }
        }
    
    def compare_financing_options(self, equipment_cost: float,
                                loan_term_years: int = 5,
                                interest_rate: float = 0.04) -> Dict:
        """
        Compare different financing options for energy improvements
        """
        # Cash purchase
        cash_option = {
            'type': 'Cash Purchase',
            'initial_cost': equipment_cost,
            'monthly_payment': 0,
            'total_cost': equipment_cost,
            'interest_paid': 0
        }
        
        # Loan option
        monthly_payment = self._calculate_monthly_payment(equipment_cost, interest_rate, loan_term_years)
        total_loan_cost = monthly_payment * loan_term_years * 12
        interest_paid = total_loan_cost - equipment_cost
        
        loan_option = {
            'type': 'Financed Purchase',
            'initial_cost': 0,  # Assuming no down payment
            'monthly_payment': round(monthly_payment, 2),
            'total_cost': round(total_loan_cost, 2),
            'interest_paid': round(interest_paid, 2),
            'loan_term_years': loan_term_years,
            'interest_rate': interest_rate
        }
        
        # Lease option
        lease_payment_factor = 0.02  # 2% of equipment cost per month as lease payment
        monthly_lease = equipment_cost * lease_payment_factor
        total_lease_cost = monthly_lease * loan_term_years * 12
        
        lease_option = {
            'type': 'Lease',
            'initial_cost': 0,
            'monthly_payment': round(monthly_lease, 2),
            'total_cost': round(total_lease_cost, 2),
            'interest_paid': 0  # Lease is a rental, no interest in traditional sense
        }
        
        return {
            'financing_options': {
                'cash': cash_option,
                'loan': loan_option,
                'lease': lease_option
            },
            'recommendation': self._compare_options(cash_option, loan_option, lease_option)
        }
    
    def _calculate_monthly_payment(self, principal: float, annual_rate: float, years: int) -> float:
        """
        Calculate monthly loan payment
        """
        monthly_rate = annual_rate / 12
        num_payments = years * 12
        
        if monthly_rate == 0:
            return principal / num_payments
        
        monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** num_payments) / ((1 + monthly_rate) ** num_payments - 1)
        return monthly_payment
    
    def _compare_options(self, cash_option, loan_option, lease_option) -> str:
        """
        Compare financing options and provide recommendation
        """
        # Simple comparison based on total cost
        if cash_option['total_cost'] < loan_option['total_cost'] and cash_option['total_cost'] < lease_option['total_cost']:
            return "Cash purchase recommended - lowest total cost"
        elif loan_option['total_cost'] < lease_option['total_cost']:
            return "Loan financing recommended - good balance of cost and cash flow"
        else:
            return "Lease option recommended - lowest monthly payment"


# Utility functions for financial calculations

def calculate_present_value(future_value: float, discount_rate: float, years: int) -> float:
    """
    Calculate present value of a future amount
    """
    return future_value / ((1 + discount_rate) ** years)


def calculate_future_value(present_value: float, growth_rate: float, years: int) -> float:
    """
    Calculate future value of a present amount
    """
    return present_value * ((1 + growth_rate) ** years)


def calculate_annuity_payment(present_value: float, interest_rate: float, periods: int) -> float:
    """
    Calculate equal periodic payments for an annuity
    """
    if interest_rate == 0:
        return present_value / periods
    
    payment = present_value * (interest_rate * (1 + interest_rate) ** periods) / ((1 + interest_rate) ** periods - 1)
    return payment