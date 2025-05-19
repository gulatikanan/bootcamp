"""Module: serialize.py
Author: Anurag"""

import yaml
from car import Car

car = Car("Tesla", "Model 3", 2022)

# Convert to YAML string
yaml_data = yaml.dump(car.__dict__)

# Save to file
with open("car.yaml", "w") as f:
    f.write(yaml_data)

print("✅ Car object serialized to YAML:")
print(yaml_data)
