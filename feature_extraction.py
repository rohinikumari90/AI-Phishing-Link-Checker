import re
import pandas as pd
from urllib.parse import urlparse

# Load the popular domains list once when this module is imported —
# not inside the function, otherwise it would reload the CSV on every single call
try:
    _top_domains_df = pd.read_csv("Dataset/top_domains.csv")
    TOP_DOMAINS_SET = set(_top_domains_df['domain'].str.lower())
except FileNotFoundError:
    TOP_DOMAINS_SET = set()


def extract_features(url):
    # Default/fallback feature set, used if a URL is too malformed to parse
    default_features = {
        'url_length': 0, 'domain_length': 0, 'num_dots': 0, 'num_hyphens': 0,
        'num_at': 0, 'num_question_marks': 0, 'num_equal_signs': 0,
        'num_underscores': 0, 'num_ampersands': 0, 'num_digits': 0,
        'num_subdirs': 0, 'has_https': 0, 'has_ip': 0, 'is_shortened': 0,
        'num_suspicious_words': 0, 'num_subdomains': 0, 'digits_in_domain': 0,
        'is_popular_domain': 0
    }

    try:
        # Remember whether the ORIGINAL input used https, before we strip it
        original_has_https = url.lower().startswith('https://')

        # Normalize: strip scheme so lexical counts match the training data format
        clean_url = re.sub(r'^https?://', '', url, flags=re.IGNORECASE)
        clean_url = re.sub(r'^www\.', '', clean_url, flags=re.IGNORECASE)

        # Use clean_url (no scheme) for all lexical counting from here on
        url_for_parse = 'http://' + clean_url
        parsed = urlparse(url_for_parse)
        domain = parsed.netloc

        features = {}
        features['url_length'] = len(clean_url)
        features['domain_length'] = len(domain)
        features['num_dots'] = clean_url.count('.')
        features['num_hyphens'] = clean_url.count('-')
        features['num_at'] = clean_url.count('@')
        features['num_question_marks'] = clean_url.count('?')
        features['num_equal_signs'] = clean_url.count('=')
        features['num_underscores'] = clean_url.count('_')
        features['num_ampersands'] = clean_url.count('&')
        features['num_digits'] = sum(c.isdigit() for c in clean_url)
        features['num_subdirs'] = clean_url.count('/')
        features['has_https'] = 1 if original_has_https else 0

        ip_pattern = r'(([0-9]{1,3}\.){3}[0-9]{1,3})'
        features['has_ip'] = 1 if re.search(ip_pattern, domain) else 0

        # FIX: match against domain only, not the full URL, to avoid
        # substring false-matches (e.g. a path containing "t.co")
        shortening_services = ['bit.ly', 'tinyurl.com', 'goo.gl', 't.co', 'ow.ly', 'is.gd', 'buff.ly']
        features['is_shortened'] = 1 if domain.lower() in shortening_services else 0

        # FIX: check suspicious words only in domain, not full URL/path.
        # Legit sites use words like "verify"/"account" in paths all the time
        # (e.g. amazon.com/account/verify) — that shouldn't count against them.
        suspicious_words = ['login', 'verify', 'secure', 'account', 'update',
                             'confirm', 'banking', 'signin', 'password']
        features['num_suspicious_words'] = sum(word in domain.lower() for word in suspicious_words)

        # FIX: handle multi-part TLDs (.co.uk, .co.in, etc.) so they don't
        # get incorrectly counted as having an extra subdomain
        multi_part_tlds = ['co.uk', 'co.in', 'com.au', 'co.jp', 'org.uk',
                            'gov.in', 'ac.in', 'co.za', 'net.in']
        domain_parts = domain.split('.')
        is_multi_part = any(domain.endswith(tld) for tld in multi_part_tlds)
        base_parts = 3 if is_multi_part else 2
        features['num_subdomains'] = max(len(domain_parts) - base_parts, 0)

        features['digits_in_domain'] = sum(c.isdigit() for c in domain)

        # NEW: strong signal — is this domain in a well-known, popular domains list?
        # Phishing domains are almost never in top popularity rankings, while
        # legitimate sites (even with long/deep URLs) usually are.
        root_domain = '.'.join(domain_parts[-2:]) if len(domain_parts) >= 2 else domain
        features['is_popular_domain'] = 1 if root_domain.lower() in TOP_DOMAINS_SET else 0

        return features

    except Exception:
        return default_features