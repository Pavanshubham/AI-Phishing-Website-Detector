import re
import whois
import requests
from urllib.parse import urlparse
from datetime import datetime


def extract_features(url):
    features = []

    parsed = urlparse(url)
    domain = parsed.netloc

    # 1. IP Address
    if re.search(r'\d+\.\d+\.\d+\.\d+', domain):
        features.append(1)
    else:
        features.append(-1)

    # 2. URL Length
    if len(url) < 54:
        features.append(-1)
    else:
        features.append(1)

    # 3. @ Symbol
    if "@" in url:
        features.append(1)
    else:
        features.append(-1)

    # 4. Double Slash Redirect
    if url.count("//") > 1:
        features.append(1)
    else:
        features.append(-1)

    # 5. Prefix-Suffix (- in domain)
    if "-" in domain:
        features.append(1)
    else:
        features.append(-1)

    # 6. Subdomain count
    if domain.count(".") > 1:
        features.append(1)
    else:
        features.append(-1)

    # 7. SSL check
    if parsed.scheme == "https":
        features.append(1)
    else:
        features.append(-1)

    # 8. HTTPS token misuse
    if "https" in domain:
        features.append(1)
    else:
        features.append(-1)

    # 9. Domain Age
    try:
        w = whois.whois(domain)
        creation_date = w.creation_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        age = (datetime.now() - creation_date).days

        if age > 180:
            features.append(1)
        else:
            features.append(-1)
    except:
        features.append(-1)

    # 10. DNS Record
    try:
        requests.get(url, timeout=3)
        features.append(1)
    except:
        features.append(-1)

    return features