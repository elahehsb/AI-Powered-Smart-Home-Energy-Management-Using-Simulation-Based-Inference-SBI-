def optimize_energy_usage(appliance_usage, weather_factors):
    # Logic to optimize energy usage based on simulations
    optimized_usage = {}
    for appliance, usage in appliance_usage.items():
        if weather_factors['temperature'] > 30:  # e.g., if it's hot
            optimized_usage[appliance] = usage * 0.8  # reduce usage of energy-heavy appliances
        else:
            optimized_usage[appliance] = usage
    
    return optimized_usage
