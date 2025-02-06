import unittest
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

class TestDataQualityChecks(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Initialize Spark session
        cls.spark = SparkSession.builder \
            .appName("Data Quality Checks Test") \
            .getOrCreate()
        
        # Load the drug_inventory_management table
        cls.drug_inventory_df = cls.spark.table("agilisium_playground.purgo_playground.drug_inventory_management")

    @classmethod
    def tearDownClass(cls):
        # Stop the Spark session
        cls.spark.stop()

    def test_non_null_drug_id(self):
        # Test for non-null drug_id
        total_rows = self.drug_inventory_df.count()
        passing_rows = self.drug_inventory_df.filter(col("drug_id").isNotNull()).count()
        pass_percentage = (passing_rows / total_rows) * 100
        result = "pass" if pass_percentage == 100 else "fail"
        
        # Assert the result
        self.assertEqual(result, "pass", "Non-null drug_id check failed")
        self.assertEqual(pass_percentage, 100, "Pass percentage for non-null drug_id is not 100%")

    def test_positive_quantity(self):
        # Test for positive quantity
        total_rows = self.drug_inventory_df.count()
        passing_rows = self.drug_inventory_df.filter(col("quantity") > 0).count()
        pass_percentage = (passing_rows / total_rows) * 100
        result = "pass" if pass_percentage == 100 else "fail"
        
        # Assert the result
        self.assertEqual(result, "pass", "Positive quantity check failed")
        self.assertEqual(pass_percentage, 100, "Pass percentage for positive quantity is not 100%")

    def test_valid_expiration_date_format(self):
        # Test for valid expiration_date format
        total_rows = self.drug_inventory_df.count()
        passing_rows = self.drug_inventory_df.filter(col("expiration_date").rlike(r"^\d{4}-\d{2}-\d{2}$")).count()
        pass_percentage = (passing_rows / total_rows) * 100
        result = "pass" if pass_percentage == 100 else "fail"
        
        # Assert the result
        self.assertEqual(result, "pass", "Valid expiration_date format check failed")
        self.assertEqual(pass_percentage, 100, "Pass percentage for valid expiration_date format is not 100%")

    def test_error_handling_for_invalid_column(self):
        # Test error handling for invalid column
        with self.assertRaises(Exception):
            self.drug_inventory_df.filter(col("invalid_column").isNotNull()).count()

if __name__ == '__main__':
    unittest.main()
