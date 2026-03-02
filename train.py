import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load dataset
data = pd.read_csv("phishing.csv")

# Drop index column
data = data.drop("index", axis=1)

# Select important features only
selected_features = [
    'having_IPhaving_IP_Address',
    'URLURL_Length',
    'having_At_Symbol',
    'double_slash_redirecting',
    'Prefix_Suffix',
    'having_Sub_Domain',
    'SSLfinal_State',
    'HTTPS_token',
    'age_of_domain',
    'DNSRecord'
]

X = data[selected_features]
y = data['Result']

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Test
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("New Model Accuracy:", accuracy)

# Save new model
joblib.dump(model, "model.pkl")

print("New Model Saved ✅")