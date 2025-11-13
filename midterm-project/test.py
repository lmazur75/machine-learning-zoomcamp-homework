import pickle
import pandas as pd


with open('model.bin', 'rb') as f_in:
    pipeline = pickle.load(f_in)

datapoint = {
    "engine_rpm": 1500,
    "fuel_pressure": 8.9,
    "lub_oil_temp": 79.6,
}


# Define all required features with default values
default_values = {
    'engine_rpm': 0,
    'lub_oil_pressure': 0.0,
    'fuel_pressure': 0.0,
    'coolant_pressure': 0.0,
    'lub_oil_temp': 0,
    'coolant_temp': 0.0
}

# Update defaults with provided values
default_values.update(datapoint)

# Create DataFrame from the complete dict
df = pd.DataFrame([default_values])

result = pipeline.predict_proba(df)[0, 1]
print(f'Probability of condition: {result:.3f}')