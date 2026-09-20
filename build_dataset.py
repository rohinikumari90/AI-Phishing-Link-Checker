import pandas as pd
from feature_extraction import extract_features

# Load the sampled dataset
df = pd.read_csv("Dataset/sample_urls_augmented.csv")

print("Extracting features for", len(df), "URLs... this may take a moment")

# Apply extract_features to every URL and build a new DataFrame
feature_rows = df['url'].apply(extract_features)
features_df = pd.DataFrame(list(feature_rows))

# Attach the label back on
features_df['status'] = df['status'].values

print("Final feature dataset shape:", features_df.shape)
print(features_df.head())

# Save this — this is what we'll train the model on
features_df.to_csv("Dataset/features_dataset.csv", index=False)
print("Saved to Dataset/features_dataset.csv")