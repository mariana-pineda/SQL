# Databricks notebook source
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import mlflow
import mlflow.sklearn

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

# Start an MLflow run
mlflow.set_experiment("/Workspace/Shared/purgo_poc/winequality-experiement")
with mlflow.start_run():
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
    mlflow.log_metric("validation_accuracy", validate_accuracy)
    mlflow.log_metric("test_accuracy", test_accuracy)
    mlflow.sklearn.log_model(model, "random_forest_model")

    print(f"Validation Accuracy: {validate_accuracy}")
    print(f"Test Accuracy: {test_accuracy}")
