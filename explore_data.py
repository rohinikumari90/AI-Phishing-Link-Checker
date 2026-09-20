import pandas as pd

# Load the dataset
df = pd.read_csv("Dataset/new_data_urls.csv")

# 1. Basic shape and preview
print("Shape:", df.shape)
print(df.head())

# 2. Check column names
print("Columns:", df.columns.tolist())

# 3. Check for missing values
print("Missing values:\n", df.isnull().sum())

# 4. Check class balance
print("Class balance:\n", df['status'].value_counts())