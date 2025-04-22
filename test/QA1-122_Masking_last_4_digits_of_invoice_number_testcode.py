"""
Setup and Configuration
"""

# Import necessary libraries
import unittest
from pyspark.sql.functions import col, regexp_replace, length
from pyspark.sql.types import StringType, StructType, StructField, LongType, DateType, DoubleType

"""
Test Class for Masking Invoice Numbers
"""
class TestInvoiceNumberMasking(unittest.TestCase):
    
    """
    Setup method to initialize the test environment
    """
    def setUp(self):
        # Drop the clone table if it exists
        try:
            spark.sql("""
                DROP TABLE IF EXISTS purgo_databricks.purgo_playground.d_product_revenue_clone
            """)
        except Exception as e:
            # Handle any exceptions during table drop
            print(f"Error dropping table: {e}")
        
        # Create a replica of the original table
        try:
            spark.sql("""
                CREATE TABLE purgo_databricks.purgo_playground.d_product_revenue_clone
                AS SELECT * FROM purgo_databricks.purgo_playground.d_product_revenue
            """)
        except Exception as e:
            # Handle any exceptions during table creation
            print(f"Error creating clone table: {e}")
    
    """
    Test Schema Validation
    """
    def test_schema_validation(self):
        # Define expected schema
        expected_schema = StructType([
            StructField("product_id", LongType(), False),
            StructField("product_name", StringType(), True),
            StructField("product_type", StringType(), True),
            StructField("revenue", LongType(), True),
            StructField("country", StringType(), True),
            StructField("customer_id", StringType(), True),
            StructField("purchased_date", DateType(), True),
            StructField("invoice_date", DateType(), True),
            StructField("invoice_number", StringType(), True),
            StructField("is_returned", LongType(), True),
            StructField("customer_satisfaction_score", LongType(), True),
            StructField("product_details", StringType(), True),
            StructField("customer_first_purchased_date", DateType(), True),
            StructField("customer_first_product", StringType(), True),
            StructField("customer_first_revenue", DoubleType(), True)
        ])
        
        # Read the clone table schema
        actual_schema = spark.table("purgo_databricks.purgo_playground.d_product_revenue_clone").schema
        
        # Assert schemas are equal
        self.assertEqual(expected_schema, actual_schema, "Schema does not match the expected schema.")
    
    """
    Test Column Count Validation
    """
    def test_column_count(self):
        # Define expected number of columns
        expected_column_count = 15
        
        # Get actual number of columns
        actual_column_count = len(spark.table("purgo_databricks.purgo_playground.d_product_revenue_clone").columns)
        
        # Assert column counts match
        self.assertEqual(expected_column_count, actual_column_count, "Number of columns does not match the target schema.")
    
    """
    Test Data Type Conversion for invoice_number
    """
    def test_invoice_number_data_type(self):
        # Read the clone table
        df = spark.table("purgo_databricks.purgo_playground.d_product_revenue_clone")
        
        # Get the data type of invoice_number
        invoice_number_type = dict(df.dtypes)['invoice_number']
        
        # Assert the data type is string
        self.assertEqual(invoice_number_type, 'string', "invoice_number column is not of type string.")
    
    """
    Test Masking of Valid Invoice Numbers
    """
    def test_masking_valid_invoice_numbers(self):
        # Apply masking logic
        df = spark.table("purgo_databricks.purgo_playground.d_product_revenue_clone")
        df_masked = df.withColumn(
            "invoice_number",
            regexp_replace(col("invoice_number").cast(StringType()), r"(\d{4})$", "****")
        )
        
        # Write masked DataFrame back to the clone table
        df_masked.write.mode("overwrite").saveAsTable("purgo_databricks.purgo_playground.d_product_revenue_clone")
        
        # Read the masked data
        masked_df = spark.table("purgo_databricks.purgo_playground.d_product_revenue_clone")
        
        # Collect sample data for assertions
        samples = masked_df.select("invoice_number").take(3)
        
        # Define expected masked patterns
        for sample in samples:
            invoice = sample['invoice_number']
            self.assertTrue(
                len(invoice) >= 4 and invoice[-4:] == "****",
                f"Masked invoice_number {invoice} does not end with '****'."
            )
    
    """
    Test Handling of Invoice Numbers with Fewer Than Four Digits
    """
    def test_invoice_number_fewer_than_four_digits(self):
        # Create test DataFrame with invoice_number fewer than four digits
        test_data = [("123",)]
        schema = StructType([StructField("invoice_number", StringType(), True)])
        test_df = spark.createDataFrame(test_data, schema)
        
        # Attempt masking and expect an error
        with self.assertRaises(Exception) as context:
            masked_df = test_df.withColumn(
                "invoice_number",
                regexp_replace(col("invoice_number"), r"(\d{4})$", "****")
            )
            masked_df.collect()
        
        # Assert the error message
        self.assertIn("substring", str(context.exception))
    
    """
    Test Handling of Null Invoice Numbers
    """
    def test_null_invoice_number(self):
        # Create test DataFrame with null invoice_number
        test_data = [(None,)]
        schema = StructType([StructField("invoice_number", StringType(), True)])
        test_df = spark.createDataFrame(test_data, schema)
        
        # Attempt masking
        df_masked = test_df.withColumn(
            "invoice_number",
            regexp_replace(col("invoice_number"), r"(\d{4})$", "****")
        )
        
        # Collect results
        results = df_masked.collect()
        
        # Assert that invoice_number is still null
        self.assertIsNone(results[0]['invoice_number'], "Null invoice_number should remain null after masking.")
    
    """
    Test Handling of Non-Numeric Invoice Numbers
    """
    def test_non_numeric_invoice_number(self):
        # Create test DataFrame with non-numeric invoice_number
        test_data = [("INV12345AB",)]
        schema = StructType([StructField("invoice_number", StringType(), True)])
        test_df = spark.createDataFrame(test_data, schema)
        
        # Apply masking
        df_masked = test_df.withColumn(
            "invoice_number",
            regexp_replace(col("invoice_number"), r"(\d{4})$", "****")
        )
        
        # Collect results
        results = df_masked.collect()
        
        # Assert that masking was applied correctly
        expected_invoice = "INV12345****"
        self.assertEqual(results[0]['invoice_number'], "INV12345****", "Non-numeric invoice_number masking failed.")
    
    """
    Cleanup method to remove the clone table after tests
    """
    def tearDown(self):
        try:
            spark.sql("""
                DROP TABLE IF EXISTS purgo_databricks.purgo_playground.d_product_revenue_clone
            """)
        except Exception as e:
            # Handle any exceptions during table drop
            print(f"Error during cleanup: {e}")

"""
Execute the tests
"""

if __name__ == '__main__':
    unittest.main()