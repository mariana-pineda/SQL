# Databricks notebook source
import pandas as pd
import numpy as np

# Load the dataset
data_path = "/dbfs/databricks-datasets/wine-quality/winequality-white.csv"
df = pd.read_csv(data_path, sep=';')

# Replace 'quality' with 'high_quality'
df['high_quality'] = df['quality'] > 6
df.drop('quality', axis=1, inplace=True)

# Split the data into train, validation, and test sets
train_df = df.sample(frac=0.6, random_state=42)
remaining_df = df.drop(train_df.index)
validation_df = remaining_df.sample(frac=0.5, random_state=42)
test_df = remaining_df.drop(validation_df.index)

# Generate test data
def generate_test_data(df, num_records):
    test_data = []
    for _ in range(num_records):
        record = {}
        for column in df.columns:
            if df[column].dtype == 'bool':
                # Validate high_quality true/false condition
                record[column] = np.random.choice([True, False])
            else:
                # Validate numerical data range
                record[column] = np.random.uniform(df[column].min(), df[column].max())
        test_data.append(record)
    return test_data

# Generate 20-30 records for each condition
train_test_data = generate_test_data(train_df, 25)  # Validate training data conditions
validation_test_data = generate_test_data(validation_df, 25)  # Validate validation data conditions
test_test_data = generate_test_data(test_df, 25)  # Validate test data conditions

# Print the generated test data
print("Train Test Data:", train_test_data)
print("Validation Test Data:", validation_test_data)
print("Test Test Data:", test_test_data)
