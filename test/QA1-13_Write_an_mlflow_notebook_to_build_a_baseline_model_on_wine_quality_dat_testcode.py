# Databricks notebook source
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Load the dataset
file_path = "/dbfs/databricks-datasets/wine-quality/winequality-white.csv"
data = pd.read_csv(file_path, sep=';')

# Add a timestamp column
data['timestamp'] = datetime.now()

# Transform the "quality" column to "high_quality"
data['high_quality'] = data['quality'] > 6

# Split the data into train, validate, and test sets
train_data = data.sample(frac=0.6, random_state=42)
remaining_data = data.drop(train_data.index)
validate_data = remaining_data.sample(frac=0.5, random_state=42)
test_data = remaining_data.drop(validate_data.index)

# Prepare features and target
features = ['fixed_acidity', 'volatile_acidity', 'citric_acid', 'residual_sugar', 'chlorides',
            'free_sulfur_dioxide', 'total_sulfur_dioxide', 'density', 'pH', 'sulphates', 'alcohol']
X_train = train_data[features]
y_train = train_data['high_quality']
X_validate = validate_data[features]
y_validate = validate_data['high_quality']
X_test = test_data[features]
y_test = test_data['high_quality']

# Train the Random Forest model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Validate the model
y_validate_pred = model.predict(X_validate)
validate_accuracy = accuracy_score(y_validate, y_validate_pred)

# Test the model
y_test_pred = model.predict(X_test)
test_accuracy = accuracy_score(y_test, y_test_pred)

# Log results
print(f"Validation Accuracy: {validate_accuracy}")
print(f"Test Accuracy: {test_accuracy}")

# Generate test data
def generate_test_data():
    test_data_records = []

    # Condition: Quality > 6 (high_quality = True)
    for _ in range(10):
        record = {
            'fixed_acidity': np.random.uniform(5, 10),
            'volatile_acidity': np.random.uniform(0.1, 0.5),
            'citric_acid': np.random.uniform(0, 0.5),
            'residual_sugar': np.random.uniform(1, 10),
            'chlorides': np.random.uniform(0.01, 0.1),
            'free_sulfur_dioxide': np.random.uniform(10, 50),
            'total_sulfur_dioxide': np.random.uniform(50, 150),
            'density': np.random.uniform(0.990, 1.000),
            'pH': np.random.uniform(2.8, 3.5),
            'sulphates': np.random.uniform(0.3, 1.0),
            'alcohol': np.random.uniform(9, 14),
            'quality': np.random.randint(7, 10),  # high_quality = True
            'timestamp': datetime.now(),
            'high_quality': True
        }
        test_data_records.append(record)

    # Condition: Quality <= 6 (high_quality = False)
    for _ in range(10):
        record = {
            'fixed_acidity': np.random.uniform(5, 10),
            'volatile_acidity': np.random.uniform(0.1, 0.5),
            'citric_acid': np.random.uniform(0, 0.5),
            'residual_sugar': np.random.uniform(1, 10),
            'chlorides': np.random.uniform(0.01, 0.1),
            'free_sulfur_dioxide': np.random.uniform(10, 50),
            'total_sulfur_dioxide': np.random.uniform(50, 150),
            'density': np.random.uniform(0.990, 1.000),
            'pH': np.random.uniform(2.8, 3.5),
            'sulphates': np.random.uniform(0.3, 1.0),
            'alcohol': np.random.uniform(9, 14),
            'quality': np.random.randint(3, 7),  # high_quality = False
            'timestamp': datetime.now(),
            'high_quality': False
        }
        test_data_records.append(record)

    return pd.DataFrame(test_data_records)

# Generate and validate the test data
test_data_df = generate_test_data()
X_test_generated = test_data_df[features]
y_test_generated = test_data_df['high_quality']
y_test_generated_pred = model.predict(X_test_generated)

# Compare expected and actual outcomes
for i, (expected, actual) in enumerate(zip(y_test_generated, y_test_generated_pred)):
    assert expected == actual, f"Test case {i} failed: expected {expected}, got {actual}"

print("All test cases passed.")
