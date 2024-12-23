# Databricks notebook source
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import mlflow
import mlflow.sklearn

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

# Separate features and target
X_train = train_df.drop('high_quality', axis=1)
y_train = train_df['high_quality']
X_validation = validation_df.drop('high_quality', axis=1)
y_validation = validation_df['high_quality']
X_test = test_df.drop('high_quality', axis=1)
y_test = test_df['high_quality']

# Train the Random Forest model
rf_model = RandomForestClassifier(random_state=42)
rf_model.fit(X_train, y_train)

# Validate the model
y_val_pred = rf_model.predict(X_validation)
validation_accuracy = accuracy_score(y_validation, y_val_pred)

# Test the model
y_test_pred = rf_model.predict(X_test)
test_accuracy = accuracy_score(y_test, y_test_pred)

# Log the experiment
mlflow.set_experiment("/Workspace/Shared/purgo_poc/winequality-experiement")
with mlflow.start_run():
    mlflow.log_param("random_state", 42)
    mlflow.log_metric("validation_accuracy", validation_accuracy)
    mlflow.log_metric("test_accuracy", test_accuracy)
    mlflow.sklearn.log_model(rf_model, "random_forest_model")
