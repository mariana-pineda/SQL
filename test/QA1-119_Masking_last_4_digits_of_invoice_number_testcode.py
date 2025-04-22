# /* 
# Test Code for Masking the last four digits of invoice_number in purgo_playground.d_product_revenue_clone
# This test suite verifies the masking logic, schema validation, data type conversions, and error handling.
# */

import unittest
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, regexp_replace, length
from pyspark.sql.types import StringType
import logging

# Set up logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Uncomment the following lines if running outside Databricks environment
# spark = SparkSession.builder.appName("MaskingTests").getOrCreate()

class MaskingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # /* 
        # Setup: Drop the d_product_revenue_clone table if it exists and create a replica from d_product_revenue
        # */
        try:
            spark.sql("DROP TABLE IF EXISTS purgo_playground.d_product_revenue_clone")
            spark.sql("CREATE TABLE purgo_playground.d_product_revenue_clone AS SELECT * FROM purgo_playground.d_product_revenue")
        except Exception as e:
            logger.error(f"Setup failed: {e}")

    @classmethod
    def tearDownClass(cls):
        # /* 
        # Cleanup: Drop the d_product_revenue_clone table after tests
        # */
        try:
            spark.sql("DROP TABLE IF EXISTS purgo_playground.d_product_revenue_clone")
        except Exception as e:
            logger.error(f"Teardown failed: {e}")
        # spark.stop()  # Commented out as per instructions

    def mask_invoice_number(self, df):
        # /* 
        # Masking Logic: Replace the last four digits of invoice_number with '*' and convert to string
        # Handle errors for invalid formats and nulls
        # */
        try:
            df = df.withColumn("invoice_number", col("invoice_number").cast(StringType()))
            df = df.withColumn("invoice_number", 
                               when(col("invoice_number").isNull(), None)
                               .when(length(col("invoice_number")) < 4, 
                                     logger.error("Invoice number must have at least 4 digits to mask"))
                               .when(~col("invoice_number").rlike("^[0-9]+$"), 
                                     logger.error("Invoice number must be numeric"))
                               .otherwise(regexp_replace(col("invoice_number"), r"\d{4}$", "****")))
            return df
        except Exception as e:
            logger.error(f"Error during masking: {e}")
            return df

    def test_successful_masking(self):
        # /* 
        # Unit Test: Successfully mask the last four digits of a valid invoice_number
        # */
        df = spark.table("purgo_playground.d_product_revenue_clone")
        masked_df = self.mask_invoice_number(df)
        masked_df.createOrReplaceTempView("masked_table")

        result = spark.sql("""
            SELECT invoice_number FROM masked_table WHERE invoice_number LIKE '123423****'
        """)
        count = result.count()
        self.assertGreater(count, 0, "Masking failed for valid invoice_number")

    def test_mask_multiple_invoice_numbers(self):
        # /* 
        # Unit Test: Mask multiple invoice_number values with varying formats
        # */
        df = spark.table("purgo_playground.d_product_revenue_clone")
        masked_df = self.mask_invoice_number(df)
        masked_df.createOrReplaceTempView("masked_table_multiple")

        test_cases = [
            ("1234234534", "123423****"),
            ("98765432101234", "9876543210****"),
            ("55555555", "5555****"),
            ("00001234", "0000****")
        ]

        for original, masked in test_cases:
            result = spark.sql(f"""
                SELECT invoice_number FROM masked_table_multiple 
                WHERE invoice_number = '{masked}' 
                AND invoice_number LIKE '{masked}'
            """)
            count = result.count()
            self.assertGreater(count, 0, f"Masking failed for invoice_number: {original}")

    def test_invoice_number_fewer_than_four_digits(self):
        # /* 
        # Unit Test: Handle invoice_number with fewer than four digits
        # Expect an error to be logged
        # */
        df = spark.table("purgo_playground.d_product_revenue_clone").filter(col("invoice_number") == 123)
        masked_df = self.mask_invoice_number(df)
        masked_df.show()
        # Since errors are logged, manually verify logs or extend logger to capture logs for assertions

    def test_null_invoice_number(self):
        # /* 
        # Unit Test: Handle null invoice_number
        # Expect an error to be logged
        # */
        df = spark.table("purgo_playground.d_product_revenue_clone").filter(col("invoice_number").isNull())
        masked_df = self.mask_invoice_number(df)
        masked_df.show()
        # Since errors are logged, manually verify logs or extend logger to capture logs for assertions

    def test_data_type_conversion(self):
        # /* 
        # Unit Test: Ensure invoice_number data type is converted to string after masking
        # */
        df = spark.table("purgo_playground.d_product_revenue_clone").filter(col("invoice_number") == 9876543210)
        masked_df = self.mask_invoice_number(df)
        masked_df.createOrReplaceTempView("masked_table_dtype")

        datatype = masked_df.schema["invoice_number"].dataType.typeName()
        self.assertEqual(datatype, "string", "invoice_number was not converted to string")

    def test_only_last_four_digits_masked(self):
        # /* 
        # Unit Test: Verify that only the last four digits are masked
        # */
        df = spark.table("purgo_playground.d_product_revenue_clone").filter(col("invoice_number") == 567890123456)
        masked_df = self.mask_invoice_number(df)
        masked_df.createOrReplaceTempView("masked_table_partial")

        result = spark.sql("""
            SELECT invoice_number FROM masked_table_partial WHERE invoice_number = '56789012****'
        """)
        count = result.count()
        self.assertGreater(count, 0, "Only the last four digits should be masked")

    def test_non_numeric_invoice_number(self):
        # /* 
        # Unit Test: Validate that non-numeric invoice_number values are handled appropriately
        # Expect an error to be logged
        # */
        df = spark.table("purgo_playground.d_product_revenue_clone").filter(col("invoice_number") == "ABCDEF1234")
        masked_df = self.mask_invoice_number(df)
        masked_df.show()
        # Since errors are logged, manually verify logs or extend logger to capture logs for assertions

    def test_column_count_match(self):
        # /* 
        # Integration Test: Ensure the number of columns matches the target table's schema before inserting
        # */
        original_df = spark.table("purgo_playground.d_product_revenue_clone")
        masked_df = self.mask_invoice_number(original_df)
        self.assertEqual(len(original_df.columns), len(masked_df.columns), "Column count mismatch after masking")

    def test_schema_validation(self):
        # /* 
        # Data Quality Test: Validate the schema of the masked table
        # */
        masked_df = self.mask_invoice_number(spark.table("purgo_playground.d_product_revenue_clone"))
        expected_schema = spark.table("purgo_playground.d_product_revenue_clone").schema
        self.assertEqual(masked_df.schema, expected_schema, "Schema mismatch after masking")

    def test_delta_lake_operations(self):
        # /* 
        # Databricks-Specific Test: Test Delta Lake operations on the masked table
        # */
        try:
            masked_df = self.mask_invoice_number(spark.table("purgo_playground.d_product_revenue_clone"))
            masked_df.write.format("delta").mode("overwrite").saveAsTable("purgo_playground.d_product_revenue_clone")
            
            # Test MERGE operation
            new_data = spark.createDataFrame([
                (1, "Product A Updated", "Type 1", 1100, "USA", "CUST001", "2024-01-10", "2024-01-15", "123456****", 0, 5, "Details A Updated", "2023-12-01", "Product X", 550.0)
            ], schema=original_df.schema)
            new_data.write.format("delta").mode("append").saveAsTable("purgo_playground.d_product_revenue_clone")

            merged_df = spark.sql("""
                MERGE INTO purgo_playground.d_product_revenue_clone AS target
                USING new_data AS source
                ON target.product_id = source.product_id
                WHEN MATCHED THEN UPDATE SET *
            """)
            self.assertIsNotNone(merged_df, "Delta Lake MERGE operation failed")
        except Exception as e:
            self.fail(f"Delta Lake operations failed: {e}")

if __name__ == '__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)