import requests
import pandas as pd

print("Downloading Tranco top domains list...")
url = "https://tranco-list.eu/top-1m.csv.zip"
response = requests.get(url)

with open("top-1m.csv.zip", "wb") as f:
    f.write(response.content)

import zipfile
with zipfile.ZipFile("top-1m.csv.zip", "r") as z:
    z.extractall(".")

# Load and keep only top 100,000 for speed — plenty for our use case
df = pd.read_csv("top-1m.csv", header=None, names=["rank", "domain"])
df_top = df.head(100000)
df_top.to_csv("Dataset/top_domains.csv", index=False)
print("Saved top 100,000 domains to Dataset/top_domains.csv")