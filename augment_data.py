import pandas as pd

trusted_domains = [
    "google.com", "youtube.com", "facebook.com", "wikipedia.org", "amazon.com",
    "twitter.com", "instagram.com", "linkedin.com", "microsoft.com", "apple.com",
    "netflix.com", "reddit.com", "github.com", "stackoverflow.com", "yahoo.com",
    "bing.com", "wordpress.com", "adobe.com", "paypal.com", "ebay.com",
    "cnn.com", "bbc.com", "nytimes.com", "espn.com", "dropbox.com",
    "spotify.com", "twitch.tv", "pinterest.com", "quora.com", "medium.com",
    "salesforce.com", "zoom.us", "slack.com", "shopify.com", "whatsapp.com",
    "office.com", "live.com", "outlook.com", "irctc.co.in", "gov.in",
    "rbi.org.in", "nic.in", "uidai.gov.in", "flipkart.com", "myntra.com",
    "zomato.com", "swiggy.com", "hdfcbank.com", "icicibank.com", "sbi.co.in",
    "axisbank.com", "python.org", "mozilla.org", "w3schools.com", "geeksforgeeks.org",
    "leetcode.com", "coursera.org", "udemy.com", "wikipedia.org", "gmail.com",
]

realistic_paths = [
    "", "", "",  # bare domain, repeated to weight it more
    "/", "/index.html", "/home",
    "/search?q=weather", "/products/item123", "/watch?v=abc123",
    "/user/profile", "/login", "/about-us", "/contact", "/blog/post-1",
    "/news/latest", "/help/support", "/account/settings"
]

rows = []
for domain in trusted_domains:
    for path in realistic_paths:
        rows.append({"url": domain + path, "status": 1})
        rows.append({"url": "https://" + domain + path, "status": 1})
        rows.append({"url": "https://www." + domain + path, "status": 1})

trusted_df = pd.DataFrame(rows)

existing = pd.read_csv("Dataset/sample_urls.csv")
combined = pd.concat([existing, trusted_df], ignore_index=True).drop_duplicates(subset='url')

combined.to_csv("Dataset/sample_urls_augmented.csv", index=False)
print("New combined dataset shape:", combined.shape)
print("Legitimate count:", (combined['status'] == 1).sum())
print("Phishing count:", (combined['status'] == 0).sum())
print("Saved to Dataset/sample_urls_augmented.csv")