import re
import random
import json

def load_sensitive_data_patterns():
    with open('sensitive_data_patterns.json') as file:
        return json.load(file)

def mask_sensitive_data(data, sensitive_data_patterns):
    masked_output = list(data)  # Convert to a list for faster replacement

    for pattern_data in sensitive_data_patterns:
        pattern = re.compile(pattern_data['pattern'])
        sensitivity_level = pattern_data['sensitivity']
        for i, char in enumerate(masked_output):
            match = pattern.search(''.join(masked_output[i:]))  # Search for a match from the current position
            if match:
                start, end = match.start() + i, match.end() + i
                if sensitivity_level == 'high':
                    masked_output[start:end] = ['*'] * (end - start)
                else:
                    sample = random.sample(masked_output[start:end], end - start)
                    masked_output[start:end] = sample

    return ''.join(masked_output)  # Convert the list back to a string

user_paragraph = input("Enter the paragraph containing sensitive data: ")
sensitive_data_patterns = load_sensitive_data_patterns()
masked_output = mask_sensitive_data(user_paragraph, sensitive_data_patterns)

print("Masked Output:")
print(masked_output)
