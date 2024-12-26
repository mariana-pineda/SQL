# Databricks notebook source
import pandas as pd
import numpy as np
from datetime import datetime

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

# Generate and display the test data
test_data_df = generate_test_data()
print(test_data_df)
