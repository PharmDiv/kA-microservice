import json

# Define a function to extract reference values
def extract_reference_values(data):
    reference_values = []  # To store the extracted reference values

    if isinstance(data, dict):
        for key, value in data.items():
            if key == "reference":
                reference_values.append(value)
            elif isinstance(value, (dict, list)):
                reference_values.extend(extract_reference_values(value))
    elif isinstance(data, list):
        for item in data:
            reference_values.extend(extract_reference_values(item))

    return reference_values