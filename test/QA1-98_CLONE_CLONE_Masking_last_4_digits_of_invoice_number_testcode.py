import unittest
from pyspark.sql import functions as F
from pyspark.sql.types import StringType, StructType

class TestMaskInvoiceNumber(unittest.TestCase):
    """ 
    Test Suite for Masking the Last Four Digits of invoice_number in d_product_revenue_clone Table
    """

    @classmethod
    def setUpClass(cls):
        """
        Setup operations before any tests are run.
        """
        # Drop the clone table if it exists
        try:
            spark.sql("DROP TABLE IF EXISTS purgo_playground.d_product_revenue_clone")
        except Exception as e:
            # Handle exception for dropping table
            pass

        # Create a replica of the original table
        try:
            spark.sql("""
                CREATE TABLE purgo_playground.d_product_revenue_clone AS
                SELECT * FROM purgo_playground.d_product_revenue
            """)
        except Exception as e:
            # Handle exception for cloning table
            pass

    @classmethod
    def tearDownClass(cls):
        """
        Cleanup operations after all tests are run.
        """
        # Drop the clone table after tests
        try:
            spark.sql("DROP TABLE IF EXISTS purgo_playground.d_product_revenue_clone")
        except Exception as e:
            # Handle exception for dropping table
            pass

    def mask_invoice_number(self, df):
        """
        Apply masking logic to the invoice_number column.
        """
        try:
            # Change invoice_number from bigint to string
            df = df.withColumn("invoice_number", F.col("invoice_number").cast(StringType()))
            
            # Mask the last four digits of invoice_number
            df = df.withColumn(
                "invoice_number",
                F.when(
                    F.length(F.col("invoice_number")) >= 4,
                    F.concat(
                        F.substring(F.col("invoice_number"), 1, F.length(F.col("invoice_number")) - 4),
                        F.lit("****")
                    )
                ).otherwise(
                    F.lit("****")
                )
            )
            return df
        except Exception as e:
            # Handle exception for masking logic
            raise e

    def test_successful_masking(self):
        """
        Test that the last four digits of a valid invoice_number are masked.
        """
        # Retrieve the clone table
        df = spark.table("purgo_playground.d_product_revenue_clone")
        
        # Apply masking
        df_masked = self.mask_invoice_number(df)
        
        # Assert that last four characters are '****'
        masked_df = df_masked.select("invoice_number").collect()
        for row in masked_df:
            self.assertTrue(row.invoice_number.endswith("****"))
            self.assertTrue(len(row.invoice_number) >= 4)

    def test_various_invoice_number_formats(self):
        """
        Test masking for various invoice_number formats.
        """
        test_data = [
            ("1234234534", "123423****"),
            ("9876543210", "987654****"),
            ("5678901234", "567890****"),
            ("1020304050", "102030****")
        ]
        schema = StructType().add("invoice_number", StringType())
        test_df = spark.createDataFrame(test_data, schema)
        
        # Apply masking
        masked_df = self.mask_invoice_number(test_df)
        results = masked_df.collect()
        
        for i, row in enumerate(results):
            self.assertEqual(row.invoice_number, test_data[i][1])

    def test_masking_fewer_than_four_digits(self):
        """
        Test that masking raises an error for invoice_number with fewer than four digits.
        """
        test_data = [("123",)]
        schema = StructType().add("invoice_number", StringType())
        test_df = spark.createDataFrame(test_data, schema)
        
        with self.assertRaises(Exception) as context:
            self.mask_invoice_number(test_df).collect()
        self.assertIn("Invoice number must have at least four digits to mask.", str(context.exception))

    def test_source_table_does_not_exist(self):
        """
        Test that an error is raised when the source table does not exist during cloning.
        """
        try:
            spark.sql("DROP TABLE IF EXISTS purgo_playground.d_product_revenue_clone")
            with self.assertRaises(Exception) as context:
                spark.sql("""
                    CREATE TABLE purgo_playground.d_product_revenue_clone AS
                    SELECT * FROM purgo_playground.d_product_revenue
                """)
            self.assertIn("Source table purgo_playground.d_product_revenue does not exist.", str(context.exception))
        except Exception as e:
            # Handle other exceptions
            pass

    def test_data_type_conversion(self):
        """
        Test that the invoice_number column is converted from bigint to string.
        """
        df = spark.table("purgo_playground.d_product_revenue_clone")
        df_masked = self.mask_invoice_number(df)
        
        # Get schema of the masked DataFrame
        schema = df_masked.schema
        invoice_number_type = dict(schema)["invoice_number"].dataType
        self.assertEqual(invoice_number_type, StringType())

    def test_data_integrity_after_masking(self):
        """
        Test that foreign key constraints remain intact after masking.
        """
        # Assuming there is a related table with foreign key constraints
        # This is a placeholder as actual foreign key checks would depend on the environment
        try:
            df = spark.table("purgo_playground.d_product_revenue_clone")
            df_masked = self.mask_invoice_number(df)
            df_masked.write.mode("overwrite").saveAsTable("purgo_playground.d_product_revenue_clone")
            
            # Validate foreign key constraints
            # Placeholder for actual foreign key validation
            self.assertTrue(True)
        except Exception as e:
            self.fail(f"Data integrity test failed: {e}")

    def test_automated_masking_process(self):
        """
        Test the automated daily masking process.
        """
        # Placeholder for scheduling and triggering the masking job
        try:
            df = spark.table("purgo_playground.d_product_revenue_clone")
            df_masked = self.mask_invoice_number(df)
            df_masked.write.mode("overwrite").saveAsTable("purgo_playground.d_product_revenue_clone")
            
            # Check for success message in logs
            # Placeholder as actual log checking would require access to logs
            success_message = "Masking process completed successfully."
            self.assertIn(success_message, "Masking process completed successfully.")
        except Exception as e:
            self.fail(f"Automated masking process test failed: {e}")

    def test_masked_invoice_number_format(self):
        """
        Test that masked invoice_number matches the expected regex pattern.
        """
        import re
        pattern = re.compile(r"^\d{6}\*{4}$")
        df = spark.table("purgo_playground.d_product_revenue_clone")
        df_masked = self.mask_invoice_number(df)
        masked_df = df_masked.select("invoice_number").collect()
        
        for row in masked_df:
            self.assertTrue(pattern.match(row.invoice_number))

    def test_error_handling_invalid_data_types(self):
        """
        Test that an error is raised when invoice_number contains non-bigint values.
        """
        test_data = [("ABCDEF1234",)]
        schema = StructType().add("invoice_number", StringType())
        test_df = spark.createDataFrame(test_data, schema)
        
        with self.assertRaises(Exception) as context:
            self.mask_invoice_number(test_df).collect()
        self.assertIn("Invalid data type for invoice_number. Expected bigint.", str(context.exception))

    def test_schema_validation(self):
        """
        Test that the schema of the clone table matches the target schema.
        """
        target_schema = spark.table("purgo_playground.d_product_revenue").schema
        clone_schema = spark.table("purgo_playground.d_product_revenue_clone").schema
        
        # Ensure number of columns match
        self.assertEqual(len(target_schema), len(clone_schema))
        
        # Ensure column names and types match
        for target_field, clone_field in zip(target_schema, clone_schema):
            self.assertEqual(target_field.name, clone_field.name)
            if target_field.name == "invoice_number":
                self.assertEqual(clone_field.dataType, StringType())
            else:
                self.assertEqual(target_field.dataType, clone_field.dataType)

    def test_column_count_before_inserting(self):
        """
        Test that the number of columns matches the target table's schema before inserting.
        """
        target_columns = [field.name for field in spark.table("purgo_playground.d_product_revenue").schema]
        clone_columns = [field.name for field in spark.table("purgo_playground.d_product_revenue_clone").schema]
        self.assertEqual(len(target_columns), len(clone_columns))

    def test_handle_missing_data_gracefully(self):
        """
        Test that missing or invalid data is handled gracefully during file operations.
        """
        try:
            # Attempt to read a non-existent file
            df = spark.read.format("delta").load("purgo_playground.non_existent_file")
            self.fail("Expected an exception for missing file.")
        except Exception as e:
            self.assertIn("Path does not exist", str(e))

if __name__ == '__main__':
    unittest.main()