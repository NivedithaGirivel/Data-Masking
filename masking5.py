import random
import re
import json

# Load sensitive data patterns from a JSON file
with open('sensitive_data_patterns.json') as f:
    classifications = json.load(f)

# MetaLearner class to determine the masking algorithm based on data sensitivity
class MetaLearner:
    def __init__(self):
        self.trained = False

    def is_trained(self):
        return self.trained

    def train(self, data, classifications):
        # Your learning logic can be added here if needed
        self.trained = True

    def predict(self, classification):
        return "dynamic" if classification["sensitivity"] == "low" else "adaptive"

# Initialize MetaLearner
meta_learner = MetaLearner()

# Dynamic masking algorithm
def dynamic_mask(data):
    jumbled_data = ''.join(random.sample(data, len(data)))
    return jumbled_data

# Adaptive masking algorithm
def adaptive_mask(data):
    masked_data = '*' * len(data)
    return masked_data

# Mask the data based on sensitivity level
def mask_data(data, classifications):
    if not meta_learner.is_trained():
        meta_learner.train(data, classifications)

    replacements = []
    classifications.sort(key=lambda c: len(c["pattern"]), reverse=True)

    for match in re.finditer("|".join([c["pattern"] for c in classifications]), data):
        original_text = match.group(0)
        classification = next(c for c in classifications if re.match(c["pattern"], original_text))
        masking_algorithm = meta_learner.predict(classification)

        if username in ["user1", "user2", "user3"] and classification["sensitivity"] == "high":
            masked_text = adaptive_mask(original_text)
        elif username not in ["user1", "user2", "user3"] and classification["sensitivity"] == "low":
            masked_text=dynamic_mask(original_text)
        else :
            masked_text = original_text if masking_algorithm == "dynamic" else adaptive_mask(original_text)

        replacements.append((match.start(), match.end(), masked_text))

    replacements.sort(key=lambda x: x[0], reverse=True)

    for start, end, masked_text in replacements:
        data = data[:start] + masked_text + data[end:]

    return data

# User authentication
username = input("Enter Username: ")

# Get user input for data to be masked
sample_data = input("Enter the Data: ")

# Check user access and mask the data accordingly
if username in ["user1", "user2", "user3", "admin"]:
    # Admin sees unmasked original data
    if username == "admin":
        print("Original Data:")
        print(sample_data)
    else:
        # Mask the data for other authorized users
        masked_data = mask_data(sample_data, classifications)

        # Users "user1", "user2", and "user3" see only high-sensitive data adaptively masked
        if username in ["user1", "user2", "user3"]:
            print("Original Data (High Sensitive Data Adaptively Masked):")
            print(masked_data)
        else:
            print("Access Denied")
else:
    # Mask the entire sensitive data for unauthorized users
    masked_data = mask_data(sample_data, classifications)
    print("Masked Data:")
    print(masked_data)
