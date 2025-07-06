import json
import pandas as pd

# Load JSON file
with open("./cleaned_data.json") as f:
    data = json.load(f)
"""
oos_val, val, train, oos_test, test, oos_train
"""

# Convert to DataFrame
df = pd.DataFrame(data, columns=["text", "label"])

label_count = 0
for label in df['label'].unique():
    print(label)
    label_count+=1
print(label_count)
