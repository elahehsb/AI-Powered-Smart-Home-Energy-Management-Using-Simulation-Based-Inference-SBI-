import numpy as np

class SmartHomeSimulator:
    def __init__(self, appliance_power, weather_factors, user_behavior):
        self.appliance_power = appliance_power  # power consumption of appliances in watts
        self.weather_factors = weather_factors  # e.g., temperature, humidity
        self.user_behavior = user_behavior  # e.g., time spent at home, appliance usage patterns

    def simulate_energy_usage(self, days=30):
        daily_energy_usage = []
        for _ in range(days):
            day_usage = 0
            for appliance, power in self.appliance_power.items():
                usage_hours = np.random.normal(loc=self.user_behavior[appliance], scale=1.0)
                day_usage += power * max(0, usage_hours)  # energy in watt-hours
            weather_effect = np.random.normal(loc=self.weather_factors['temperature'], scale=2.0)
            day_usage += weather_effect * 0.1  # add weather impact on energy usage
            daily_energy_usage.append(day_usage)
        
        return np.array(daily_energy_usage)

    def simulate_costs(self, energy_usage, price_per_kwh=0.1):
        return energy_usage * price_per_kwh / 1000  # convert watt-hours to kWh and calculate cost
