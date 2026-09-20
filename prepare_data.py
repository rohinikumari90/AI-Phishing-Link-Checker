import pandas as pd

# Load full dataset
df = pd.read_csv("Dataset/new_data_urls.csv")

# Take equal samples from each class for balance
phishing = df[df['status'] == 0].sample(n=12500, random_state=42)
legit = df[df['status'] == 1].sample(n=12500, random_state=42)

# Combine and shuffle
sample_df = pd.concat([phishing, legit]).sample(frac=1, random_state=42).reset_index(drop=True)

print("Sampled shape:", sample_df.shape)
print(sample_df['status'].value_counts())

# Save it for the next step
sample_df.to_csv("Dataset/sample_urls.csv", index=False)
print("Saved to Dataset/sample_urls.csv")