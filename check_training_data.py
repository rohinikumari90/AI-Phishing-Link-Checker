import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

df = pd.read_csv("Dataset/features_dataset.csv")

print("Average feature values by class:\n")
print(df.groupby('status')[['url_length', 'num_subdirs', 'has_https', 'num_dots', 'domain_length']].mean())

print("\n\nSample of LEGITIMATE (status=1) rows:")
print(df[df['status'] == 1][['url_length', 'num_subdirs', 'has_https', 'num_dots']].head(10))

print("\nSample of PHISHING (status=0) rows:")
print(df[df['status'] == 0][['url_length', 'num_subdirs', 'has_https', 'num_dots']].head(10))

print("\n\nHow many LEGITIMATE rows have num_subdirs == 0?")
print((df[df['status'] == 1]['num_subdirs'] == 0).sum(), "out of", len(df[df['status'] == 1]))

print("\nHow many PHISHING rows have num_subdirs == 0?")
print((df[df['status'] == 0]['num_subdirs'] == 0).sum(), "out of", len(df[df['status'] == 0]))

print("\n\nHow many LEGITIMATE rows have has_https == 1?")
print((df[df['status'] == 1]['has_https'] == 1).sum(), "out of", len(df[df['status'] == 1]))

print("\nHow many PHISHING rows have has_https == 1?")
print((df[df['status'] == 0]['has_https'] == 1).sum(), "out of", len(df[df['status'] == 0]))