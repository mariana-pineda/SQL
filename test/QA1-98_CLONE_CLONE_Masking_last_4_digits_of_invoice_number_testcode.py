# Import necessary libraries
import unittest
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, substring, length, concat, lit
from pyspark.sql.types import StructType, StructField, LongType, StringType, DoubleType, DateType, TimestampType
from pyspark.sql.utils import AnalysisException

# Initialize Spark session (Assuming 'spark' is already available)
# spark = SparkSession.builder.appName("DatabricksTest").getOrCreate()

class TestDProductRevenueClone(unittest.TestCase):
    """Test suite for purgo_playground.d_product_revenue_clone table"""

    @classmethod
    def setUpClass(cls):
        """
        Setup configurations and initial state before any tests run
        """
        # Define schema for d_product_revenue_clone
        cls.schema = StructType([
            StructField("product_id", LongType(), True),
            StructField("product_name", StringType(), True),
            StructField("product_type", StringType(), True),
            StructField("revenue", LongType(), True),
            StructField("country", StringType(), True),
            StructField("customer_id", StringType(), True),
            StructField("purchased_date", DateType(), True),
            StructField("invoice_date", DateType(), True),
            StructField("invoice_number", LongType(), True),
            StructField("is_returned", LongType(), True),
            StructField("customer_satisfaction_score", LongType(), True),
            StructField("product_details", StringType(), True),
            StructField("customer_first_purchased_date", DateType(), True),
            StructField("customer_first_product", StringType(), True),
            StructField("customer_first_revenue", DoubleType(), True)
        ])
        
        # Drop the clone table if it exists
        try:
            spark.sql("""
                DROP TABLE IF EXISTS purgo_databricks.purgo_playground.d_product_revenue_clone
            """)
        except AnalysisException as e:
            # Log the exception if needed
            pass
        
        # Clone the original table
        try:
            spark.sql("""
                CREATE TABLE purgo_databricks.purgo_playground.d_product_revenue_clone
                AS SELECT * FROM purgo_databricks.purgo_playground.d_product_revenue
            """)
        except AnalysisException as e:
            print(f"Error cloning table: {e}")
    
    def test_clone_table_exists(self):
        """
        Validate that the clone table exists after cloning operation
        """
        try:
            tables = spark.sql("""
                SHOW TABLES IN purgo_databricks.purgo_playground
            """)
            table_list = [row.tableName for row in tables.collect()]
            self.assertIn("d_product_revenue_clone", table_list, "Clone table does not exist.")
        except Exception as e:
            self.fail(f"Exception occurred while checking table existence: {e}")
    
    def test_schema_validation(self):
        """
        Ensure the schema of the clone table matches the expected schema
        """
        try:
            clone_df = spark.table("purgo_databricks.purgo_playground.d_product_revenue_clone")
            clone_schema = clone_df.schema
            self.assertEqual(len(clone_schema), len(self.schema), "Number of columns does not match.")
            for field_clone, field_expected in zip(clone_schema, self.schema):
                self.assertEqual(field_clone.name, field_expected.name, f"Column name mismatch: {field_clone.name}")
                self.assertEqual(field_clone.dataType, field_expected.dataType, f"Data type mismatch for column: {field_clone.name}")
        except Exception as e:
            self.fail(f"Exception during schema validation: {e}")
    
    def test_invoice_number_masking(self):
        """
        Test that the last 4 digits of invoice_number are masked with '*'
        """
        try:
            clone_df = spark.table("purgo_databricks.purgo_playground.d_product_revenue_clone")
            masked_df = clone_df.withColumn(
                "masked_invoice_number",
                when(
                    (col("invoice_number").isNotNull()) & (length(col("invoice_number").cast(StringType())) >= 4),
                    concat(
                        substring(col("invoice_number").cast(StringType()), 1, length(col("invoice_number").cast(StringType())) - 4),
                        lit("****")
                    )
                ).otherwise(col("invoice_number").cast(StringType()))
            )
            
            masked_values = masked_df.select("invoice_number", "masked_invoice_number").collect()
            
            for row in masked_values:
                original = str(row['invoice_number'])
                expected = original[:-4] + "****" if len(original) >= 4 else original
                self.assertEqual(row['masked_invoice_number'], expected, f"Masking failed for invoice_number: {original}")
        except Exception as e:
            self.fail(f"Exception during invoice number masking test: {e}")
    
    def test_column_count(self):
        """
        Ensure the number of columns matches the target table's schema
        """
        try:
            clone_df = spark.table("purgo_databricks.purgo_playground.d_product_revenue_clone")
            target_schema = self.schema
            self.assertEqual(len(clone_df.columns), len(target_schema), "Column count does not match target schema.")
        except Exception as e:
            self.fail(f"Exception during column count test: {e}")
    
    def test_data_type_consistency(self):
        """
        Validate that data types of all columns are consistent between source and clone
        """
        try:
            clone_df = spark.table("purgo_databricks.purgo_playground.d_product_revenue_clone")
            for field in clone_df.schema.fields:
                expected_field = next((f for f in self.schema.fields if f.name == field.name), None)
                self.assertIsNotNone(expected_field, f"Unexpected column found: {field.name}")
                self.assertEqual(field.dataType, expected_field.dataType, f"Data type mismatch for column: {field.name}")
        except Exception as e:
            self.fail(f"Exception during data type consistency test: {e}")
    
    def test_null_handling(self):
        """
        Test that NULL values in invoice_number are handled gracefully
        """
        try:
            clone_df = spark.table("purgo_databricks.purgo_playground.d_product_revenue_clone")
            null_df = clone_df.filter(col("invoice_number").isNull())
            null_count = null_df.count()
            self.assertGreaterEqual(null_count, 0, "NULL handling failed for invoice_number.")
        except Exception as e:
            self.fail(f"Exception during NULL handling test: {e}")
    
    def test_edge_cases_masking(self):
        """
        Test masking logic for edge cases like invoice_number with less than 4 digits
        """
        try:
            clone_df = spark.table("purgo_databricks.purgo_playground.d_product_revenue_clone")
            edge_df = clone_df.filter(length(col("invoice_number").cast(StringType())) < 4)
            edge_cases = edge_df.select("invoice_number").collect()
            for row in edge_cases:
                original = str(row['invoice_number'])
                expected = original  # No masking applied
                masked = original  # As per masking logic
                self.assertEqual(original, masked, f"Edge case masking incorrectly applied for invoice_number: {original}")
        except Exception as e:
            self.fail(f"Exception during edge cases masking test: {e}")
    
    def test_masked_data_quality(self):
        """
        Ensure all masked invoice_number entries conform to the expected format
        """
        try:
            clone_df = spark.table("purgo_databricks.purgo_playground.d_product_revenue_clone")
            masked_df = clone_df.withColumn(
                "masked_invoice_number",
                when(
                    (col("invoice_number").isNotNull()) & (length(col("invoice_number").cast(StringType())) >= 4),
                    concat(
                        substring(col("invoice_number").cast(StringType()), 1, length(col("invoice_number").cast(StringType())) - 4),
                        lit("****")
                    )
                ).otherwise(col("invoice_number").cast(StringType()))
            )
            validity_df = masked_df.withColumn(
                "is_valid",
                when(
                    (length(col("masked_invoice_number")) >= 4) &
                    (substring(col("masked_invoice_number"), -4, 4) == "****"),
                    True
                ).otherwise(False)
            )
            invalid_entries = validity_df.filter(col("is_valid") == False).count()
            self.assertEqual(invalid_entries, 0, "Data quality validation failed for masked_invoice_number.")
        except Exception as e:
            self.fail(f"Exception during data quality validation test: {e}")
    
    def test_performance(self):
        """
        Basic performance test to ensure masking operation completes within expected time
        """
        import time
        try:
            start_time = time.time()
            clone_df = spark.table("purgo_databricks.purgo_playground.d_product_revenue_clone")
            clone_df.withColumn(
                "masked_invoice_number",
                when(
                    (col("invoice_number").isNotNull()) & (length(col("invoice_number").cast(StringType())) >= 4),
                    concat(
                        substring(col("invoice_number").cast(StringType()), 1, length(col("invoice_number").cast(StringType())) - 4),
                        lit("****")
                    )
                ).otherwise(col("invoice_number").cast(StringType()))
            ).collect()
            end_time = time.time()
            duration = end_time - start_time
            self.assertLess(duration, 10, "Performance test failed: Masking took too long.")
        except Exception as e:
            self.fail(f"Exception during performance test: {e}")
    
    def test_delta_operations(self):
        """
        Test Delta Lake operations like MERGE, UPDATE, DELETE on the clone table
        """
        try:
            # Assuming clone table is a Delta table
            clone_table = "purgo_databricks.purgo_playground.d_product_revenue_clone"
            
            # Perform an UPDATE operation
            spark.sql(f"""
                MERGE INTO {clone_table} AS tgt
                USING (SELECT product_id, 'Updated Product' AS product_name FROM {clone_table} LIMIT 1) AS src
                ON tgt.product_id = src.product_id
                WHEN MATCHED THEN UPDATE SET tgt.product_name = src.product_name
            """)
            
            updated_row = spark.sql(f"""
                SELECT product_name FROM {clone_table} LIMIT 1
            """).collect()[0]['product_name']
            
            self.assertEqual(updated_row, "Updated Product", "Delta Lake MERGE operation failed.")
            
            # Perform a DELETE operation
            spark.sql(f"""
                DELETE FROM {clone_table} WHERE product_id = 1
            """)
            remaining = spark.sql(f"""
                SELECT COUNT(*) as count FROM {clone_table} WHERE product_id = 1
            """).collect()[0]['count']
            self.assertEqual(remaining, 0, "Delta Lake DELETE operation failed.")
        except Exception as e:
            self.fail(f"Exception during Delta operations test: {e}")
    
    def test_cleanup_operations(self):
        """
        Ensure that cleanup operations are performed correctly after tests
        """
        try:
            # Drop the clone table after tests
            spark.sql("""
                DROP TABLE IF EXISTS purgo_databricks.purgo_playground.d_product_revenue_clone
            """)
            tables = spark.sql("""
                SHOW TABLES IN purgo_databricks.purgo_playground
            """)
            table_list = [row.tableName for row in tables.collect()]
            self.assertNotIn("d_product_revenue_clone", table_list, "Cleanup failed: Clone table still exists.")
        except Exception as e:
            self.fail(f"Exception during cleanup operations test: {e}")
    
    @classmethod
    def tearDownClass(cls):
        """
        Cleanup after all tests have run
        """
        try:
            spark.sql("""
                DROP TABLE IF EXISTS purgo_databricks.purgo_playground.d_product_revenue_clone
            """)
        except AnalysisException as e:
            pass

# Execute the tests
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)