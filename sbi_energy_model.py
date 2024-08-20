import torch
import pyro
import pyro.distributions as dist
from pyro.infer import SVI, Trace_ELBO
from pyro.optim import Adam

# Define the probabilistic model for energy optimization
def energy_model(data):
    appliance_usage_effect = pyro.sample("appliance_usage_effect", dist.Normal(0.0, 1.0))
    weather_effect = pyro.sample("weather_effect", dist.Normal(0.0, 1.0))

    with pyro.plate("data", len(data)):
        observed_energy = pyro.sample(
            "obs_energy",
            dist.Normal(
                appliance_usage_effect * data['appliance_usage'] +
                weather_effect * data['weather_factors'],
                0.1
            ),
            obs=data['energy_usage']
        )

# Define the guide (variational distribution)
def energy_guide(data):
    appliance_usage_loc = pyro.param("appliance_usage_loc", torch.tensor(0.0))
    appliance_usage_scale = pyro.param("appliance_usage_scale", torch.tensor(1.0))
    weather_effect_loc = pyro.param("weather_effect_loc", torch.tensor(0.0))
    weather_effect_scale = pyro.param("weather_effect_scale", torch.tensor(1.0))

    pyro.sample("appliance_usage_effect", dist.Normal(appliance_usage_loc, appliance_usage_scale))
    pyro.sample("weather_effect", dist.Normal(weather_effect_loc, weather_effect_scale))

# Generate synthetic energy data
def generate_energy_data():
    return {
        'appliance_usage': np.random.normal(0, 1, 100),
        'weather_factors': np.random.normal(0, 1, 100),
        'energy_usage': np.random.normal(0.5, 0.1, 100)
    }

data = generate_energy_data()
data_tensor = {key: torch.tensor(val, dtype=torch.float32) for key, val in data.items()}

# Run inference
optimizer = Adam({"lr": 0.01})
svi = SVI(energy_model, energy_guide, optimizer, loss=Trace_ELBO())

n_steps = 1000
for step in range(n_steps):
    loss = svi.step(data_tensor)
    if step % 100 == 0:
        print(f"Step {step} : Loss = {loss}")

# Extract inferred parameters
inferred_params = {
    "appliance_usage_effect": pyro.param("appliance_usage_loc").item(),
    "weather_effect": pyro.param("weather_effect_loc").item(),
}

print(f"Inferred parameters: {inferred_params}")
