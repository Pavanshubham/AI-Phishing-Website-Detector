from flask import Flask, request, render_template_string
import joblib
import numpy as np
from feature_extractor import extract_features

app = Flask(__name__)

model = joblib.load("model.pkl")

html = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Phishing Detector</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-dark text-light">

<div class="container mt-5">
    <div class="card shadow-lg p-4 bg-secondary">
        <h2 class="text-center mb-4">🔐 AI-Based Phishing Website Detector</h2>

        <form method="post">
            <div class="mb-3">
                <label class="form-label">Enter Website URL</label>
                <input type="text" name="url" class="form-control" placeholder="https://example.com" required>
            </div>

            <div class="text-center">
                <button type="submit" class="btn btn-warning px-4">Check Website</button>
            </div>
        </form>

        {% if prediction %}
        <div class="mt-4 text-center">
            <h4>Result:</h4>
            <div class="alert {% if 'Legitimate' in prediction %}alert-success{% else %}alert-danger{% endif %}">
                <strong>{{ prediction }}</strong>
            </div>
        </div>
        {% endif %}

    </div>
</div>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    prediction = None
    if request.method == "POST":
        url = request.form["url"]
        features = extract_features(url)
        features = np.array([features])
        result = model.predict(features)[0]

        if result == 1:
            prediction = "Legitimate Website 🟢"
        else:
            prediction = "Phishing Website 🔴"

    return render_template_string(html, prediction=prediction)

import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
