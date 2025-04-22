# /* 
# Setup and Configuration
# Assume spark is already available in the environment
# Import necessary modules for testing
# */
import unittest
from pyspark.sql.types import StructType, StructField, StringType, LongType, DoubleType, DateType
from pyspark.sql.functions import when, col, length, concat, lit
from pyspark.sql import Row

class TestInvoiceNumberMasking(unittest.TestCase):
    # /* 
    # Define the schema for d_product_revenue_clone
    # */
    schema = StructType([
        StructField("product_id", LongType(), True),
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

    # /* 
    # Create test data covering various scenarios
    # */
    test_data = [
        # Happy path
        Row(1, "Product A", "Type 1", 1000, "USA", "C001", "2024-01-10", "2024-01-15", "1234567890", 0, 5, "Detail A", "2023-12-01", "Product X", 500.0),
        Row(2, "Product B", "Type 2", 2000, "Canada", "C002", "2024-02-20", "2024-02-25", "9876543210", 1, 4, "Detail B", "2023-11-05", "Product Y", 1500.0),
        
        # Edge cases: invoice_number with exactly four digits
        Row(3, "Product C", "Type 1", 1500, "UK", "C003", "2024-03-15", "2024-03-20", "1234", 0, 3, "Detail C", "2023-10-10", "Product Z", 750.0),
        
        # Edge cases: invoice_number with more than four digits
        Row(4, "Product D", "Type 3", 2500, "Germany", "C004", "2024-04-10", "2024-04-15", "555566667777", 0, 5, "Detail D", "2023-09-12", "Product W", 2000.0),
        
        # Error cases: invoice_number with non-numeric characters
        Row(5, "Product E", "Type 2", 3000, "France", "C005", "2024-05-05", "2024-05-10", "ABCDEF1234", 1, 2, "Detail E", "2023-08-08", "Product V", 2500.0),
        
        # NULL handling: invoice_number is null
        Row(6, "Product F", "Type 1", 1800, "Spain", "C006", "2024-06-18", "2024-06-22", None, 0, 4, "Detail F", "2023-07-07", "Product U", 900.0),
        
        # Special characters in product_name
        Row(7, "Prøduct G", "Type 4", 2200, "Italy", "C007", "2024-07-20", "2024-07-25", "1122334455", 0, 5, "Detail G", "2023-06-06", "Product T", 1200.0),
        
        # Multi-byte characters in customer_id
        Row(8, "Product H", "Type 2", 1600, "Japan", "C008Ω", "2024-08-15", "2024-08-20", "9988776655", 1, 3, "Detail H", "2023-05-05", "Product S", 800.0),
        
        # Invoice_number with fewer than four digits
        Row(9, "Product I", "Type 3", 1400, "Australia", "C009", "2024-09-10", "2024-09-14", "123", 0, 4, "Detail I", "2023-04-04", "Product R", 600.0),
        
        # Invoice_number with exactly four asterisks after masking
        Row(10, "Product J", "Type 1", 1700, "Brazil", "C010", "2024-10-05", "2024-10-10", "5678", 1, 2, "Detail J", "2023-03-03", "Product Q", 1100.0),
        
        # Special characters in product_details
        Row(11, "Product K", "Type 4", 1900, "Mexico", "C011", "2024-11-12", "2024-11-18", "3344556677", 0, 5, "Detail & K!", "2023-02-02", "Product P", 1300.0),
        
        # Null values in other fields
        Row(12, None, "Type 2", 2100, "Netherlands", "C012", "2024-12-20", "2024-12-25", "7766554433", 1, None, "Detail L", None, "Product O", 0.0),
    
        # Additional records to make up 20-30 diverse test cases
        Row(13, "Product L", "Type 3", 2300, "Sweden", "C013", "2024-01-05", "2024-01-10", "4455667788", 0, 4, "Detail M", "2023-01-01", "Product N", 1400.0),
        Row(14, "Product M", "Type 1", 1200, "Norway", "C014", "2024-02-14", "2024-02-19", "6677889900", 1, 3, "Detail N", "2022-12-12", "Product M", 700.0),
        Row(15, "Product N", "Type 4", 2600, "Switzerland", "C015", "2024-03-25", "2024-03-30", "8899001122", 0, 5, "Detail O", "2022-11-11", "Product L", 1600.0),
        Row(16, "Prodúct O", "Type 2", 2400, "Denmark", "C016", "2024-04-08", "2024-04-13", "9900112233", 1, 2, "Detail P", "2022-10-10", "Product K", 900.0),
        Row(17, "Product P", "Type 3", 2500, "Finland", "C017", "2024-05-19", "2024-05-24", "1020304050", 0, 4, "Detail Q", "2022-09-09", "Product J", 1000.0),
        Row(18, "Product Q", "Type 1", 2800, "Ireland", "C018", "2024-06-30", "2024-07-05", "5566778899", 1, 1, "Detail R", "2022-08-08", "Product I", 1100.0),
        Row(19, "Product R", "Type 4", 2700, "Belgium", "C019", "2024-07-11", "2024-07-16", "2233445566", 0, 5, "Detail S", "2022-07-07", "Product H", 1200.0),
        Row(20, "Product S", "Type 2", 2900, "Austria", "C020", "2024-08-22", "2024-08-27", "3344556677", 1, 3, "Detail T", "2022-06-06", "Product G", 1300.0)
    ]

    def setUp(self):
        # /* 
        # Setup before each test
        # Drop the clone table if it exists and recreate it with test data
        # */
        try:
            spark.sql("DROP TABLE IF EXISTS purgo_databricks.purgo_playground.d_product_revenue_clone")
        except Exception as e:
            # /* Handle potential errors during table drop */
            print(f"Error dropping table: {e}")
        
        try:
            # /* 
            # Create DataFrame with test data
            # Mask the last four digits of invoice_number
            # Write the masked data to d_product_revenue_clone table
            # */
            df = spark.createDataFrame(self.test_data, self.schema)
            masked_df = df.withColumn(
                "invoice_number",
                when(
                    col("invoice_number").isNull(),
                    None
                ).when(
                    length(col("invoice_number")) < 4,
                    lit("****")
                ).otherwise(
                    concat(substring(col("invoice_number"), 1, length(col("invoice_number")) - 4), lit("****"))
                )
            )
            masked_df.write.mode("overwrite").format("delta").saveAsTable("purgo_databricks.purgo_playground.d_product_revenue_clone")
        except Exception as e:
            # /* Handle potential errors during table creation and data masking */
            print(f"Error during setup: {e}")

    def test_mask_last_four_digits(self):
        # /* 
        # Unit test for masking the last four digits of a valid invoice_number
        # */
        try:
            df = spark.table("purgo_databricks.purgo_playground.d_product_revenue_clone")
            result = df.filter(col("invoice_number") == "123456****").count()
            self.assertEqual(result, 1, "Failed to mask the last four digits correctly")
        except Exception as e:
            self.fail(f"test_mask_last_four_digits failed: {e}")

    def test_mask_various_invoice_numbers(self):
        # /* 
        # Parameterized test for masking various invoice_number formats
        # */
        test_cases = [
            ("9876543210", "987654****"),
            ("111122223333", "11112222****"),
            ("555566667777", "55556666****"),
            ("1234", "****")
        ]
        for original, expected in test_cases:
            with self.subTest(original=original, expected=expected):
                try:
                    df = spark.table("purgo_databricks.purgo_playground.d_product_revenue_clone")
                    result = df.filter(col("invoice_number") == expected).count()
                    self.assertEqual(result, 1, f"Invoice_number {original} was not masked to {expected}")
                except Exception as e:
                    self.fail(f"test_mask_various_invoice_numbers failed for {original}: {e}")

    def test_invoice_number_fewer_than_four_digits(self):
        # /* 
        # Test handling of invoice_number with fewer than four digits
        # Expect the invoice_number to be '****'
        # */
        try:
            df = spark.table("purgo_databricks.purgo_playground.d_product_revenue_clone")
            result = df.filter((col("invoice_number") == "****") & (col("product_id") == 9)).count()
            self.assertEqual(result, 1, "Failed to handle invoice_number with fewer than four digits")
        except Exception as e:
            self.fail(f"test_invoice_number_fewer_than_four_digits failed: {e}")

    def test_null_invoice_number(self):
        # /* 
        # Test handling of null invoice_number
        # Expect the invoice_number to remain null
        # */
        try:
            df = spark.table("purgo_databricks.purgo_playground.d_product_revenue_clone")
            result = df.filter(col("invoice_number").isNull() & (col("product_id") == 6)).count()
            self.assertEqual(result, 1, "Failed to handle null invoice_number properly")
        except Exception as e:
            self.fail(f"test_null_invoice_number failed: {e}")

    def test_data_type_consistency(self):
        # /* 
        # Verify that the data type of invoice_number remains consistent after masking
        # */
        try:
            df = spark.table("purgo_databricks.purgo_playground.d_product_revenue_clone")
            invoice_type = df.schema["invoice_number"].dataType
            self.assertEqual(invoice_type, StringType(), "Data type of invoice_number does not remain consistent")
        except Exception as e:
            self.fail(f"test_data_type_consistency failed: {e}")

    def test_schema_validation(self):
        # /* 
        # Validate the schema of the clone table matches the target schema
        # */
        target_schema = StructType([
            StructField("product_id", LongType(), True),
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
        try:
            df = spark.table("purgo_databricks.purgo_playground.d_product_revenue_clone")
            self.assertEqual(df.schema, target_schema, "Schema validation failed for d_product_revenue_clone")
        except Exception as e:
            self.fail(f"test_schema_validation failed: {e}")

    def test_column_count(self):
        # /* 
        # Ensure the number of columns matches the target table's schema
        # */
        try:
            df = spark.table("purgo_databricks.purgo_playground.d_product_revenue_clone")
            target_column_count = len(self.schema.fields)
            self.assertEqual(len(df.columns), target_column_count, "Column count mismatch in d_product_revenue_clone")
        except Exception as e:
            self.fail(f"test_column_count failed: {e}")

    def test_masked_data_loaded_correctly(self):
        # /* 
        # Verify that all invoice_number entries have the last four digits masked
        # */
        try:
            df = spark.table("purgo_databricks.purgo_playground.d_product_revenue_clone")
            masked = df.filter(~col("invoice_number").rlike("^\d+$"))
            self.assertEqual(masked.count(), 5, "Not all invoice_number entries are masked correctly")
        except Exception as e:
            self.fail(f"test_masked_data_loaded_correctly failed: {e}")

    def test_invoice_number_format_after_masking(self):
        # /* 
        # Validate the format of invoice_number after masking matches the regex ^\d{6}\*{4}$
        # */
        try:
            df = spark.table("purgo_databricks.purgo_playground.d_product_revenue_clone")
            regex_match = df.filter(col("invoice_number").rlike("^\d{6}\*{4}$")).count()
            self.assertGreaterEqual(regex_match, 1, "invoice_number does not match the expected regex after masking")
        except Exception as e:
            self.fail(f"test_invoice_number_format_after_masking failed: {e}")

    def test_only_invoice_number_modified(self):
        # /* 
        # Ensure that only the invoice_number column is modified during masking
        # */
        try:
            df = spark.table("purgo_databricks.purgo_playground.d_product_revenue_clone")
            original_df = spark.table("purgo_databricks.purgo_playground.d_product_revenue")
            joined_df = df.join(original_df, "product_id")
            modified_columns = [col("d_product_revenue_clone." + field.name) for field in self.schema.fields if field.name != "invoice_number"]
            unchanged = joined_df.filter(
                (df["product_name"] == original_df["product_name"]) &
                (df["product_type"] == original_df["product_type"]) &
                (df["revenue"] == original_df["revenue"]) &
                (df["country"] == original_df["country"]) &
                (df["customer_id"] == original_df["customer_id"]) &
                (df["purchased_date"] == original_df["purchased_date"]) &
                (df["invoice_date"] == original_df["invoice_date"]) &
                (df["is_returned"] == original_df["is_returned"]) &
                (df["customer_satisfaction_score"] == original_df["customer_satisfaction_score"]) &
                (df["product_details"] == original_df["product_details"]) &
                (df["customer_first_purchased_date"] == original_df["customer_first_purchased_date"]) &
                (df["customer_first_product"] == original_df["customer_first_product"]) &
                (df["customer_first_revenue"] == original_df["customer_first_revenue"])
            ).count()
            self.assertEqual(unchanged, df.count(), "Other columns were altered during masking")
        except Exception as e:
            self.fail(f"test_only_invoice_number_modified failed: {e}")

    def test_cleanup_operations(self):
        # /* 
        # Ensure proper cleanup after tests
        # Drop the clone table
        # */
        try:
            spark.sql("DROP TABLE IF EXISTS purgo_databricks.purgo_playground.d_product_revenue_clone")
            table_exists = spark.catalog.tableExists("purgo_databricks.purgo_playground.d_product_revenue_clone")
            self.assertFalse(table_exists, "Cleanup failed: d_product_revenue_clone table still exists")
        except Exception as e:
            self.fail(f"test_cleanup_operations failed: {e}")

    def tearDown(self):
        # /* 
        # Cleanup after each test
        # Ensure the clone table is dropped
        # */
        try:
            spark.sql("DROP TABLE IF EXISTS purgo_databricks.purgo_playground.d_product_revenue_clone")
        except Exception as e:
            print(f"Error during teardown: {e}")

# /* 
# Execute the tests
# */
if __name__ == '__main__':
    unittest.main()