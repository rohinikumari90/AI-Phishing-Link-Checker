from flask import Flask, render_template, request
import joblib
import pandas as pd
from feature_extraction import extract_features
import re

app = Flask(__name__)

model = joblib.load("Models/phishing_model.pkl")

PHISHING_LABEL = 0
LEGIT_LABEL = 1

TRUSTED_DOMAINS = {
    "google.com", "youtube.com", "facebook.com", "wikipedia.org", "amazon.com",
    "twitter.com", "instagram.com", "linkedin.com", "microsoft.com", "apple.com",
    "netflix.com", "reddit.com", "github.com", "stackoverflow.com", "yahoo.com",
    "gmail.com", "outlook.com", "office.com", "flipkart.com",
    "irctc.co.in", "gov.in", "rbi.org.in",
}

def get_base_domain(url):
    clean = re.sub(r'^https?://', '', url, flags=re.IGNORECASE)
    clean = re.sub(r'^www\.', '', clean, flags=re.IGNORECASE)
    domain = clean.split('/')[0]
    return domain.lower()

def build_explanations(features, is_trusted):
    """Human-readable reasons behind the prediction, for the UI breakdown."""
    explanations = []

    if is_trusted:
        explanations.append({"icon": "✅", "text": "This domain is in our verified trusted list", "type": "good"})
        return explanations

    if features.get('is_popular_domain'):
        explanations.append({"icon": "✅", "text": "Domain found in list of popular, well-known websites", "type": "good"})
    else:
        explanations.append({"icon": "⚠️", "text": "Domain not found in popular websites list", "type": "warn"})

    if features.get('has_https'):
        explanations.append({"icon": "✅", "text": "Uses HTTPS (secure connection)", "type": "good"})
    else:
        explanations.append({"icon": "⚠️", "text": "Does not use HTTPS", "type": "warn"})

    if features.get('has_ip'):
        explanations.append({"icon": "🚨", "text": "URL uses a raw IP address instead of a domain name", "type": "bad"})

    if features.get('is_shortened'):
        explanations.append({"icon": "🚨", "text": "URL uses a link-shortening service", "type": "bad"})

    sw = features.get('num_suspicious_words', 0)
    if sw > 0:
        explanations.append({"icon": "⚠️", "text": f"Domain contains {sw} suspicious keyword(s) like 'login', 'verify', 'secure'", "type": "warn"})

    if features.get('num_hyphens', 0) >= 3:
        explanations.append({"icon": "⚠️", "text": f"Domain has {features['num_hyphens']} hyphens — common in fake/lookalike domains", "type": "warn"})

    if features.get('url_length', 0) > 75:
        explanations.append({"icon": "⚠️", "text": "URL is unusually long", "type": "warn"})

    if features.get('num_subdomains', 0) >= 3:
        explanations.append({"icon": "⚠️", "text": f"URL has {features['num_subdomains']} subdomains — unusual for legitimate sites", "type": "warn"})

    if not explanations:
        explanations.append({"icon": "ℹ️", "text": "No strong signals detected either way", "type": "neutral"})

    return explanations

@app.route("/", methods=["GET", "POST"])
def home():

    result = ""
    confidence = None
    explanations = None
    checked_url = None

    if request.method == "POST":
        url = request.form["url"]
        checked_url = url
        print("User Entered:", url)

        base_domain = get_base_domain(url)
        is_trusted = base_domain in TRUSTED_DOMAINS

        if is_trusted:
            result = "This URL looks LEGITIMATE (verified trusted domain)"
            confidence = 99.9
            features = {}
        else:
            features = extract_features(url)
            features_df = pd.DataFrame([features])

            proba = model.predict_proba(features_df)[0]
            class_list = list(model.classes_)
            phishing_idx = class_list.index(PHISHING_LABEL)
            phishing_prob = proba[phishing_idx]

            if phishing_prob > 0.75:
                result = "WARNING: This URL looks like PHISHING"
                confidence = round(phishing_prob * 100, 2)
            elif phishing_prob > 0.5:
                result = "SUSPICIOUS: Please verify this URL before trusting it"
                confidence = round(phishing_prob * 100, 2)
            else:
                result = "This URL looks LEGITIMATE"
                confidence = round((1 - phishing_prob) * 100, 2)

        explanations = build_explanations(features, is_trusted)

    return render_template(
        "index.html",
        result=result,
        confidence=confidence,
        explanations=explanations,
        checked_url=checked_url
    )

if __name__ == "__main__":
    app.run(debug=True)