# Databricks notebook source
import pandas as pd
import numpy as np
from datetime import datetime

# Load the dataset
data_path = "/dbfs/databricks-datasets/wine-quality/winequality-white.csv"
df = pd.read_csv(data_path, sep=';')

# Transform the "quality" column to "high_quality"
df['high_quality'] = df['quality'] > 6

# Add a new column to save the timestamp
df['timestamp'] = datetime.now()

# Generate test data
np.random.seed(42)  # For reproducibility

# Generate 20-30 data records to test every condition
test_data = []

for i in range(25):
    # Randomly generate feature values
    fixed_acidity = np.random.uniform(4, 15)
    volatile_acidity = np.random.uniform(0.1, 1.5)
    citric_acid = np.random.uniform(0, 1)
    residual_sugar = np.random.uniform(0.5, 15)
    chlorides = np.random.uniform(0.01, 0.2)
    free_sulfur_dioxide = np.random.uniform(1, 72)
    total_sulfur_dioxide = np.random.uniform(6, 289)
    density = np.random.uniform(0.990, 1.004)
    pH = np.random.uniform(2.8, 4)
    sulphates = np.random.uniform(0.22, 1.08)
    alcohol = np.random.uniform(8, 14)
    
    # Randomly assign quality and calculate high_quality
    quality = np.random.randint(3, 9)
    high_quality = quality > 6
    
    # Add timestamp
    timestamp = datetime.now()
    
    # Append the generated record to test_data
    test_data.append({
        'fixed_acidity': fixed_acidity,
        'volatile_acidity': volatile_acidity,
        'citric_acid': citric_acid,
        'residual_sugar': residual_sugar,
        'chlorides': chlorides,
        'free_sulfur_dioxide': free_sulfur_dioxide,
        'total_sulfur_dioxide': total_sulfur_dioxide,
        'density': density,
        'pH': pH,
        'sulphates': sulphates,
        'alcohol': alcohol,
        'quality': quality,  # This is for reference, not used in training
        'high_quality': high_quality,  # Condition: quality > 6
        'timestamp': timestamp  # Condition: Add timestamp
    })

# Convert test_data to DataFrame
test_df = pd.DataFrame(test_data)

# Display the generated test data
test_df.head()
