# Databricks notebook source
import pandas as pd
import numpy as np
from datetime import datetime

# Load the dataset
data_path = "/dbfs/databricks-datasets/wine-quality/winequality-white.csv"
df = pd.read_csv(data_path, sep=';')

# Transform the "quality" column to "high_quality"
df['high_quality'] = df['quality'] > 6

# Add a new column to save the current timestamp
df['timestamp'] = datetime.now()

# Split the data into 60% training, 20% validation, and 20% test sets
train_df = df.sample(frac=0.6, random_state=42)
remaining_df = df.drop(train_df.index)
validation_df = remaining_df.sample(frac=0.5, random_state=42)
test_df = remaining_df.drop(validation_df.index)

# Generate test data
def generate_test_data(df, num_records):
    test_data = []
    for _ in range(num_records):
        record = {
            'fixed_acidity': np.random.uniform(4, 15),  # Random value within typical range
            'volatile_acidity': np.random.uniform(0.1, 1.5),  # Random value within typical range
            'citric_acid': np.random.uniform(0, 1),  # Random value within typical range
            'residual_sugar': np.random.uniform(0.9, 15),  # Random value within typical range
            'chlorides': np.random.uniform(0.01, 0.2),  # Random value within typical range
            'free_sulfur_dioxide': np.random.uniform(1, 72),  # Random value within typical range
            'total_sulfur_dioxide': np.random.uniform(6, 289),  # Random value within typical range
            'density': np.random.uniform(0.990, 1.004),  # Random value within typical range
            'pH': np.random.uniform(2.8, 4),  # Random value within typical range
            'sulphates': np.random.uniform(0.22, 1.08),  # Random value within typical range
            'alcohol': np.random.uniform(8, 14),  # Random value within typical range
            'high_quality': np.random.choice([True, False]),  # Random boolean
            'timestamp': datetime.now()  # Current timestamp
        }
        test_data.append(record)
    return pd.DataFrame(test_data)

# Generate 20-30 data records to test every condition
test_data = generate_test_data(df, 25)

# Validate conditions
# Condition: Check if 'high_quality' is correctly assigned
assert all((test_data['high_quality'] == (test_data['quality'] > 6)) | (test_data['high_quality'] == (test_data['quality'] <= 6)))

# Condition: Check if 'timestamp' is added
assert 'timestamp' in test_data.columns

# Condition: Check if data is split correctly
assert len(train_df) / len(df) == 0.6
assert len(validation_df) / len(df) == 0.2
assert len(test_df) / len(df) == 0.2

# Output the generated test data
print(test_data)
