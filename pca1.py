import pandas as pd
import numpy as np

# Example dataset: House price related
# - Size: Positive relation (bigger house → higher price)
# - Distance_to_city: Negative relation (farther → lower price)
# - House_number: Random noise → no relation
data = {
    'House_Size_sqft':      [1000, 1500, 2000, 2500, 3000],
    'Distance_to_City_km':  [5, 10, 15, 20, 25],
    'House_Number':         [7, 21, 13, 44, 2],  # Random numbers (no real pattern)
    'Price_in_lakhs':       [50, 70, 90, 110, 130]  # House prices
}

df = pd.DataFrame(data)

print("Dataset:")
print(df)

# 1️⃣ Covariance Matrix
cov_matrix = df.cov()
print("\nCovariance Matrix:")
print(cov_matrix)

# 2️⃣ Pearson Correlation Matrix
pearson_corr = df.corr(method='pearson')
print("\nPearson Correlation Matrix:")
print(pearson_corr)

# 3️⃣ Spearman's Rank Correlation Matrix
spearman_corr = df.corr(method='spearman')
print("\nSpearman's Rank Correlation Matrix:")
print(spearman_corr)

# Extract for Price_in_lakhs vs each feature
features = ['House_Size_sqft', 'Distance_to_City_km', 'House_Number']
print("\nSpecific Relationships with Price_in_lakhs:")
for feature in features:
    cov = np.cov(df[feature], df['Price_in_lakhs'])[0, 1]
    pearson = df[feature].corr(df['Price_in_lakhs'], method='pearson')
    spearman = df[feature].corr(df['Price_in_lakhs'], method='spearman')
    print(f"{feature} -> Cov: {cov:.2f}, Pearson: {pearson:.3f}, Spearman: {spearman:.3f}")
