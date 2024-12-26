# Databricks notebook source
import unittest
import pandas as pd
from datetime import datetime

class TestWineQualityModel(unittest.TestCase):
    
    def setUp(self):
        # Load the dataset
        self.data_path = "/dbfs/databricks-datasets/wine-quality/winequality-white.csv"
        self.df = pd.read_csv(self.data_path, sep=';')
        
        # Transform the "quality" column to "high_quality"
        self.df['high_quality'] = self.df['quality'] > 6
        
        # Add a new column to save the timestamp
        self.df['timestamp'] = datetime.now()
        
        # Generate test data
        self.test_data = [
            {'fixed_acidity': 7.0, 'volatile_acidity': 0.27, 'citric_acid': 0.36, 'residual_sugar': 20.7, 'chlorides': 0.045, 
             'free_sulfur_dioxide': 45.0, 'total_sulfur_dioxide': 170.0, 'density': 1.001, 'pH': 3.0, 'sulphates': 0.45, 
             'alcohol': 8.8, 'quality': 6, 'high_quality': False, 'timestamp': datetime.now()},
            {'fixed_acidity': 6.3, 'volatile_acidity': 0.3, 'citric_acid': 0.34, 'residual_sugar': 1.6, 'chlorides': 0.049, 
             'free_sulfur_dioxide': 14.0, 'total_sulfur_dioxide': 132.0, 'density': 0.994, 'pH': 3.3, 'sulphates': 0.49, 
             'alcohol': 9.5, 'quality': 6, 'high_quality': False, 'timestamp': datetime.now()},
            # Add more test cases as needed
        ]
        self.test_df = pd.DataFrame(self.test_data)
    
    def test_quality_transformation(self):
        # Test if the quality transformation is correct
        for index, row in self.test_df.iterrows():
            expected = row['quality'] > 6
            actual = row['high_quality']
            self.assertEqual(expected, actual, f"Failed at index {index}: expected {expected}, got {actual}")
    
    def test_timestamp_column(self):
        # Test if the timestamp column is added
        for index, row in self.test_df.iterrows():
            self.assertIsInstance(row['timestamp'], datetime, f"Timestamp is not a datetime object at index {index}")
    
    def test_data_split(self):
        # Test if the data is split correctly
        train_size = int(0.6 * len(self.df))
        validate_size = int(0.2 * len(self.df))
        test_size = len(self.df) - train_size - validate_size
        
        self.assertEqual(train_size + validate_size + test_size, len(self.df), "Data split sizes do not add up")
        self.assertEqual(train_size, int(0.6 * len(self.df)), "Training set size is incorrect")
        self.assertEqual(validate_size, int(0.2 * len(self.df)), "Validation set size is incorrect")
        self.assertEqual(test_size, int(0.2 * len(self.df)), "Test set size is incorrect")

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)
