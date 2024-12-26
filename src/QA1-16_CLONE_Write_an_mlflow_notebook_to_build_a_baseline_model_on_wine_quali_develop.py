# Databricks notebook source
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import mlflow
import mlflow.sklearn

# Load the dataset
data_path = "/dbfs/databricks-datasets/wine-quality/winequality-white.csv"
df = pd.read_csv(data_path, sep=';')

# Transform the "quality" column to "high_quality"
df['high_quality'] = df['quality'] > 6

# Add a new column to save the timestamp
df['timestamp'] = datetime.now()

# Split the data
train, temp = train_test_split(df, test_size=0.4, random_state=42)
validate, test = train_test_split(temp, test_size=0.5, random_state=42)

# Prepare the data for training
X_train = train.drop(['quality', 'high_quality', 'timestamp'], axis=1)
y_train = train['high_quality']

X_validate = validate.drop(['quality', 'high_quality', 'timestamp'], axis=1)
y_validate = validate['high_quality']

X_test = test.drop(['quality', 'high_quality', 'timestamp'], axis=1)
y_test = test['high_quality']

# Start an MLflow run
mlflow.set_experiment("/Workspace/Shared/purgo_poc/winequality-experiement")
with mlflow.start_run():
    # Train a Random Forest model
    rf = RandomForestClassifier(random_state=42)
    rf.fit(X_train, y_train)
    
    # Log the model
    mlflow.sklearn.log_model(rf, "random_forest_model")
    
    # Validate the model
    validate_score = rf.score(X_validate, y_validate)
    mlflow.log_metric("validation_score", validate_score)
    
    # Test the model
    test_score = rf.score(X_test, y_test)
    mlflow.log_metric("test_score", test_score)
