# /* 
# Setup and Configuration
# Initialize the testing environment and necessary configurations.
# */

import unittest
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, length, substring, concat, lit, when
from pyspark.sql.types import StringType

class TestMaskInvoiceNumber(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize Spark session
        cls.spark = SparkSession.builder.appName("TestMaskInvoiceNumber").getOrCreate()
        try:
            # Drop the clone table if it exists
            cls.spark.sql("""
                DROP TABLE IF EXISTS purgo_databricks.purgo_playground.d_product_revenue_clone
            """)
        except Exception as e:
            # Handle any exceptions during table drop
            print(f"Error dropping table: {e}")
        
        try:
            # Clone the original table
            cls.spark.sql("""
                CREATE TABLE purgo_databricks.purgo_playground.d_product_revenue_clone
                AS SELECT * FROM purgo_databricks.purgo_playground.d_product_revenue
            """)
        except Exception as e:
            # Handle any exceptions during table cloning
            print(f"Error cloning table: {e}")
        
        # Read the cloned table
        cls.df_original = cls.spark.table("purgo_databricks.purgo_playground.d_product_revenue_clone")
    
    def mask_invoice_number(self, df):
        # /* 
        # PySpark logic to mask the last four digits of invoice_number
        # */
        try:
            df_masked = df.withColumn(
                "invoice_number",
                when(
                    length(col("invoice_number").cast(StringType())) >= 4,
                    concat(
                        substring(col("invoice_number").cast(StringType()), 1, length(col("invoice_number").cast(StringType())) - 4),
                        lit("****")
                    )
                ).otherwise(lit("****"))
            )
            return df_masked
        except Exception as e:
            # Handle any exceptions during masking
            raise Exception(f"Masking failed: {e}")
    
    def test_schema_validation(self):
        # /* 
        # Validate that the schema of the clone matches the original schema
        # */
        original_schema = self.df_original.schema
        cloned_table_schema = self.spark.table("purgo_databricks.purgo_playground.d_product_revenue_clone").schema
        self.assertEqual(original_schema, cloned_table_schema, "Schemas do not match")
    
    def test_column_count(self):
        # /* 
        # Ensure the number of columns matches the target table's schema
        # */
        original_columns = len(self.df_original.columns)
        cloned_columns = len(self.spark.table("purgo_databricks.purgo_playground.d_product_revenue_clone").columns)
        self.assertEqual(original_columns, cloned_columns, "Number of columns do not match")
    
    def test_masking_valid_invoice_number(self):
        # /* 
        # Test masking logic for a valid numeric invoice_number
        # */
        test_df = self.df_original.filter(col("invoice_number") == 1234234534)
        masked_df = self.mask_invoice_number(test_df)
        masked_value = masked_df.select("invoice_number").collect()[0][0]
        self.assertEqual(masked_value, "123423****", "Invoice number masking failed for valid input")
    
    def test_masking_various_invoice_numbers(self):
        # /* 
        # Test masking logic for various valid numeric invoice_numbers
        # */
        test_cases = {
            9876543210: "987654****",
            4567890123: "456789****"
        }
        for original, masked in test_cases.items():
            with self.subTest(original=original, masked=masked):
                test_df = self.df_original.filter(col("invoice_number") == original)
                masked_df = self.mask_invoice_number(test_df)
                masked_value = masked_df.select("invoice_number").collect()[0][0]
                self.assertEqual(masked_value, masked, f"Masking failed for invoice_number {original}")
    
    def test_masking_invoice_number_fewer_than_four_digits(self):
        # /* 
        # Test masking logic for invoice_number with fewer than four digits
        # */
        test_df = self.df_original.filter(col("invoice_number") == 123)
        masked_df = self.mask_invoice_number(test_df)
        masked_value = masked_df.select("invoice_number").collect()[0][0]
        self.assertEqual(masked_value, "****", "Masking failed for invoice_number with fewer than four digits")
    
    def test_masking_non_numeric_invoice_number(self):
        # /* 
        # Test masking logic for non-numeric invoice_number values
        # */
        try:
            test_df = self.spark.table("purgo_databricks.purgo_playground.d_product_revenue_clone")\
                .filter(col("invoice_number") == "ABC1234567")
            masked_df = self.mask_invoice_number(test_df)
            masked_df.collect()
            self.fail("Masking did not raise an error for non-numeric invoice_number")
        except Exception as e:
            self.assertIn("Masking failed", str(e), "Incorrect exception message for non-numeric invoice_number")
    
    def test_missing_clone_table(self):
        # /* 
        # Test masking logic when the clone table does not exist
        # */
        try:
            self.spark.sql("""
                DROP TABLE IF EXISTS purgo_databricks.purgo_playground.d_product_revenue_clone
            """)
            test_df = self.spark.table("purgo_databricks.purgo_playground.d_product_revenue_clone")
            masked_df = self.mask_invoice_number(test_df)
            masked_df.collect()
            self.fail("Masking did not raise an error when clone table is missing")
        except Exception as e:
            self.assertIn("cannot resolve", str(e), "Incorrect exception message for missing clone table")
    
    def test_insufficient_permissions(self):
        # /* 
        # Test masking logic failure due to insufficient permissions
        # */
        # Note: Simulating insufficient permissions is complex and typically requires environment setup.
        # Here, we assume an exception is raised when trying to drop or create the table without permissions.
        try:
            # Attempt to drop the table without permissions
            self.spark.sql("""
                DROP TABLE purgo_databricks.purgo_playground.d_product_revenue_clone
            """)
        except Exception as e:
            self.assertIn("Permission denied", str(e), "Incorrect exception message for insufficient permissions")
    
    def test_data_type_validation(self):
        # /* 
        # Validate that invoice_number is of the correct data type
        # */
        schema = self.spark.table("purgo_databricks.purgo_playground.d_product_revenue_clone").schema
        invoice_number_type = [field.dataType for field in schema.fields if field.name == "invoice_number"][0]
        self.assertEqual(str(invoice_number_type), "LongType", "invoice_number is not of type bigint")
    
    def tearDownClass(cls):
        # /* 
        # Cleanup operations after tests are done
        # */
        try:
            cls.spark.sql("""
                DROP TABLE IF EXISTS purgo_databricks.purgo_playground.d_product_revenue_clone
            """)
        except Exception as e:
            print(f"Error during cleanup: {e}")
        cls.spark.stop()

# /* 
# Execute the tests
# */

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)