import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Load dataset
products = pd.read_csv('products.csv')

# Preprocess data
products = products.dropna()
X = products.drop('Profit', axis=1)
y = products['Profit']

# Split data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Predict profit for test set
y_pred = model.predict(X_test)

# Print results
print('Predicted profit:', y_pred)