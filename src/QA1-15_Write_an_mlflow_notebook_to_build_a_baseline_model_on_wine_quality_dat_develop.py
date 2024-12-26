# Databricks notebook source
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import mlflow
import mlflow.sklearn

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

# Prepare features and labels
features = df.columns.drop(['quality', 'high_quality', 'timestamp'])
X_train = train_df[features]
y_train = train_df['high_quality']
X_val = validation_df[features]
y_val = validation_df['high_quality']
X_test = test_df[features]
y_test = test_df['high_quality']

# Train a Random Forest model
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train, y_train)

# Validate the model
val_predictions = rf_model.predict(X_val)
val_accuracy = accuracy_score(y_val, val_predictions)

# Test the model
test_predictions = rf_model.predict(X_test)
test_accuracy = accuracy_score(y_test, test_predictions)

# Log the experiment in MLflow
mlflow.set_experiment("/Workspace/Shared/purgo_poc/winequality-experiement")
with mlflow.start_run():
    mlflow.log_param("model_type", "RandomForest")
    mlflow.log_metric("validation_accuracy", val_accuracy)
    mlflow.log_metric("test_accuracy", test_accuracy)
    mlflow.sklearn.log_model(rf_model, "model")
