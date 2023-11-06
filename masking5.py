import random
import re
import json
with open('sensitive_data_patterns.json') as f:
    classifications = json.load(f)
class MetaLearner:
    def __init__(self):
        self.trained = False

    def is_trained(self):
        return self.trained

    def train(self, data, classifications):
        self.trained = True

    def predict(self, classification):
        return "dynamic" if classification["sensitivity"] == "low" else "adaptive"
meta_learner = MetaLearner()
def dynamic_mask(data):

    jumbled_data = ''.join(random.sample(data, len(data)))
    return jumbled_data
def adaptive_mask(data):

    masked_data = '*' * len(data)
    return masked_data
def mask_data(data, classifications):
    if not meta_learner.is_trained():
        meta_learner.train(data, classifications)
    replacements = []
    classifications.sort(key=lambda c: len(c["pattern"]), reverse=True)

    for match in re.finditer("|".join([c["pattern"] for c in classifications]), data):
        original_text = match.group(0)
        classification = next(c for c in classifications if re.match(c["pattern"], original_text))
        masking_algorithm = meta_learner.predict(classification)
        if masking_algorithm == "dynamic":
            masked_text = dynamic_mask(original_text)
        else:
            masked_text = adaptive_mask(original_text)

        replacements.append((match.start(), match.end(), masked_text))

    replacements.sort(key=lambda x: x[0], reverse=True)
    for start, end, masked_text in replacements:
        data = data[:start] + masked_text + data[end:]

    return data

sample_data = "Sensitive data here: 123456789012, and an email: example@example.com"

masked_data = mask_data(sample_data, classifications)

print(masked_data)
