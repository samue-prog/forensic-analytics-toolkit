import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest

# 1. GENERATE SYNTHETIC FORENSIC DATA
# In a real scenario, you would load a CSV file here: pd.read_csv('../data/transactions.csv')
def generate_sample_data(n_samples=1000):
    np.random.seed(42)
    
    # Normal transactions (98% of data)
    normal_amounts = np.random.normal(50, 20, int(n_samples * 0.98))
    normal_times = np.random.uniform(0, 24, int(n_samples * 0.98))
    
    # Anomalous transactions (2% of data - high amounts or weird hours)
    fraud_amounts = np.random.normal(2000, 500, int(n_samples * 0.02))
    fraud_times = np.random.uniform(2, 4, int(n_samples * 0.02)) # Transactions at 3 AM
    
    df = pd.DataFrame({
        'amount': np.concatenate([normal_amounts, fraud_amounts]),
        'hour_of_day': np.concatenate([normal_times, fraud_times])
    })
    return df

# 2. INITIALIZE ANALYSIS
print("--- Initializing Credit Card Anomaly Detection ---")
data = generate_sample_data()

# 3. APPLY ISOLATION FOREST MODEL
# This is a standard ML algorithm that "isolates" outliers from the main cluster
model = IsolationForest(contamination=0.02, random_state=42)
data['anomaly_score'] = model.fit_predict(data[['amount', 'hour_of_day']])

# Mapping: Isolation Forest returns -1 for anomalies and 1 for normal data
data['is_anomaly'] = data['anomaly_score'].map({1: 'Normal', -1: 'Suspicious'})

# 4. FORENSIC SUMMARY
anomalies = data[data['is_anomaly'] == 'Suspicious']
print(f"Total Transactions Analyzed: {len(data)}")
print(f"Suspicious Patterns Identified: {len(anomalies)}")
print("\nTop 5 High-Risk Transactions:")
print(anomalies.sort_values(by='amount', ascending=False).head())

# 5. VISUALIZATION (Optional - helpful for reports)
plt.figure(figsize=(10, 6))
sns.scatterplot(data=data, x='hour_of_day', y='amount', hue='is_anomaly', palette={'Normal': 'blue', 'Suspicious': 'red'})
plt.title('Financial Forensics: Transaction Anomaly Mapping')
plt.xlabel('Hour of Day (24h)')
plt.ylabel('Transaction Amount ($)')
plt.show()
