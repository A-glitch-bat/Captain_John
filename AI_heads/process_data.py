import json
import pandas as pd

# Load JSON file
with open("./datasets/data_oos_plus.json") as f:
    data = json.load(f)
"""
oos_val, val, train, oos_test, test, oos_train
"""
samples = data["train"]

# Convert to DataFrame
df = pd.DataFrame(samples, columns=["text", "label"])

label_map = {}
for label in df['label'].unique():
    print(f"\nCurrent label: {label}")
    action = input("Keep (k), Rename (r), or Remove (x)? ").strip().lower()
    if action == "k" or action == "y":
        label_map[label] = label
    elif action == "x" or action == "n":
        label_map[label] = None
    else:
        print("Invalid input, skipping.")

# Apply mapping
def remap_label(row):
    mapped = label_map.get(row['label'])
    return mapped

df['new_label'] = df.apply(remap_label, axis=1)
df_cleaned = df[df['new_label'].notna()][['text', 'new_label']]
df_cleaned.columns = ['text', 'label']

# Convert to JSON format
final_data = df_cleaned.values.tolist()

# Save to new JSON file
with open("cleaned_data.json", "w") as f:
    json.dump(final_data, f, indent=2)

print("✅ Cleaned data saved to cleaned_data.json")
