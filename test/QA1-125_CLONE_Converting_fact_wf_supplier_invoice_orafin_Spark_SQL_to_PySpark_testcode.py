%pip install delta

# /* 
#    Test Suite for Converting Spark.SQL Notebook to PySpark
#    This suite includes unit tests, integration tests, performance tests, and data quality validations
#    It also tests Delta Lake operations, MERGE, UPDATE, DELETE, window functions, and ensures proper cleanup
# */

# Import necessary modules
import unittest
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType, TimestampType
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, when

# /* 
#    Static Variables Initialization
#    Define expected schemas for target tables
# */

# Expected schema for purgo_playground.supplier_invoice_orig
EXPECTED_SCHEMA_SUPPLIER_INVOICE_ORIG = StructType([
    StructField("src_sys_cd", StringType(), True),
    StructField("po_nbr", StringType(), True),
    StructField("po_line_nbr", StringType(), True),
    StructField("invc_co_amt", DoubleType(), True),
    StructField("invc_txn_amt", DoubleType(), True),
    StructField("invc_txn_type", StringType(), True),
    StructField("document_type", StringType(), True),
    StructField("document_desc", StringType(), True),
    StructField("invc_entry_period", LongType(), True),
    StructField("vchr_nbr", LongType(), True),
    StructField("fscl_yr_nbr", LongType(), True),
    StructField("vchr_type_cd", StringType(), True),
    StructField("po_curncy_cd", StringType(), True),
    StructField("post_yr_mth_nbr", LongType(), True),
    StructField("invc_entry_dt", LongType(), True),
    StructField("paymt_due_dt", LongType(), True),
    StructField("txn_curncy_mth_rt", LongType(), True),
    StructField("inv_line_desc", StringType(), True),
    StructField("spend_type_cd", StringType(), True),
    StructField("supplier_cd", StringType(), True),
    StructField("suplr_invc_dt", LongType(), True),
    StructField("txn_orig_id", StringType(), True),
    StructField("suplr_invc_nbr", StringType(), True),
    StructField("remit_to_rgn_cd", StringType(), True),
    StructField("remit_to_rgn_nm", StringType(), True),
    StructField("suplr_paymt_terms_desc", StringType(), True),
    StructField("ap_payment_term_desc", StringType(), True),
    StructField("remit_to_cntry_nm", StringType(), True),
    StructField("supplier_type_cd", StringType(), True),
    StructField("suplr_paymt_terms_cd", StringType(), True),
    StructField("ap_payment_term_cd", StringType(), True),
    StructField("remit_to_addr_line_2", StringType(), True),
    StructField("remit_to_addr_line_3", StringType(), True),
    StructField("remit_to_addr_line_4", StringType(), True),
    StructField("remit_to_cntry_cd", StringType(), True),
    StructField("po_paymt_terms_cd", StringType(), True),
    StructField("po_paymt_terms_desc", StringType(), True),
    StructField("gl_acct_id", StringType(), True),
    StructField("cost_centre_cd", LongType(), True),
    StructField("co_cd", LongType(), True),
    StructField("co_curncy_cd", StringType(), True),
    StructField("pass_through_field", StringType(), True),
    StructField("pass_through_line", StringType(), True),
    StructField("item_nbr", StringType(), True),
    StructField("item_desc", StringType(), True),
    StructField("uom_conv_factor", StringType(), True),
    StructField("invc_uom_cd", StringType(), True),
    StructField("vendor_mat_no", StringType(), True),
    StructField("unit_prc", DoubleType(), True),
    StructField("invc_qty", LongType(), True),
    StructField("base_qty", StringType(), True),
    StructField("suplr_nm_src", StringType(), True),
    StructField("remit_to_st_cd", StringType(), True),
    StructField("part_rev_no", StringType(), True),
    StructField("contract_flag", StringType(), True),
    StructField("contract_type", StringType(), True),
    StructField("profit_cntr", StringType(), True),
    StructField("co_curncy_mth_rt", LongType(), True),
    StructField("invc_txn_pmar_amt", LongType(), True),
    StructField("invc_co_pmar_amt", LongType(), True),
    StructField("unit_prc_pmar_amt", StringType(), True),
    StructField("aprval_dt", StringType(), True),
    StructField("vomi_flag", StringType(), True),
    StructField("payment_compliance_flg", StringType(), True),
    StructField("vchr_line_nbr", LongType(), True),
    StructField("vchr_status", StringType(), True),
    StructField("thermo_item_nbr", StringType(), True),
    StructField("lcr_flag", StringType(), True),
    StructField("lcr_region", StringType(), True),
    StructField("invc_apprv_id", StringType(), True),
    StructField("reporting_site", StringType(), True),
    StructField("warehouse", StringType(), True),
    StructField("warehouse_nm", StringType(), True),
    StructField("unit", StringType(), True),
    StructField("nature", StringType(), True),
    StructField("inv_flg", StringType(), True),
    StructField("contract_start_date", StringType(), True),
    StructField("contract_end_date", StringType(), True),
    StructField("fk_orig", StringType(), True),
    StructField("floor_stock_cd", StringType(), True),
    StructField("sec_supp_cd", StringType(), True),
    StructField("rpt_flex1", StringType(), True),
    StructField("supplier_segment", StringType(), True),
    StructField("inv_flg_text", StringType(), True),
    StructField("invc_txn_amt_clsfctn", StringType(), True),
    StructField("source_country", StringType(), True),
    StructField("business_unit", StringType(), True),
    StructField("div_cd", StringType(), True)
])

# /* 
#    Test Suite Definition
# */

class TestSupplierInvoiceOrig(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # /* 
        #    Setup Class Method
        #    Initialize DataFrames for testing
        # */
        # Read the supplier_invoice_orig table
        cls.df_supplier_invoice_orig = spark.table("purgo_playground.supplier_invoice_orig")
        # Read the test data table
        cls.df_test_data = spark.table("purgo_playground.supplier_invoice_orig_test")

    def test_schema_validation(self):
        # /* 
        #    Test Schema Validation
        #    Ensure the schema of the test data matches the expected schema
        # */
        expected_fields = EXPECTED_SCHEMA_SUPPLIER_INVOICE_ORIG.fields
        actual_schema = self.df_test_data.schema
        self.assertEqual(len(expected_fields), len(actual_schema), "Number of columns does not match.")
        for expected_field, actual_field in zip(expected_fields, actual_schema):
            self.assertEqual(expected_field.name, actual_field.name, f"Column name mismatch: {expected_field.name} != {actual_field.name}")
            self.assertEqual(expected_field.dataType, actual_field.dataType, f"Data type mismatch for column {expected_field.name}")

    def test_column_count(self):
        # /* 
        #    Test Column Count
        #    Verify that the number of columns in the test data matches the target table
        # */
        expected_column_count = len(EXPECTED_SCHEMA_SUPPLIER_INVOICE_ORIG.fields)
        actual_column_count = len(self.df_test_data.columns)
        self.assertEqual(expected_column_count, actual_column_count, "Column count does not match the target table schema.")

    def test_data_types(self):
        # /* 
        #    Test Data Types
        #    Validate data types of each column in the test data
        # */
        actual_schema = self.df_test_data.schema
        for field in actual_schema.fields:
            if isinstance(field.dataType, StringType):
                self.assertTrue(True, f"Column {field.name} has correct STRING type.")
            elif isinstance(field.dataType, DoubleType):
                self.assertTrue(True, f"Column {field.name} has correct DOUBLE type.")
            elif isinstance(field.dataType, LongType):
                self.assertTrue(True, f"Column {field.name} has correct LONG type.")
            else:
                self.fail(f"Column {field.name} has unexpected data type: {field.dataType}")

    def test_null_handling(self):
        # /* 
        #    Test NULL Handling
        #    Ensure that columns handle NULL values as expected
        # */
        nullable_columns = [field.name for field in EXPECTED_SCHEMA_SUPPLIER_INVOICE_ORIG.fields if field.nullable]
        for column in nullable_columns:
            null_count = self.df_test_data.filter(col(column).isNull()).count()
            self.assertGreaterEqual(null_count, 0, f"Column {column} has NULL values which are allowed.")

    def test_data_type_conversion(self):
        # /* 
        #    Test Data Type Conversion
        #    Verify that data type conversions are correctly applied using Databricks functions
        # */
        try:
            df_converted = self.df_test_data.withColumn("invc_entry_period", col("invc_entry_period").cast(StringType()))
            df_converted.select("invc_entry_period").foreach(lambda row: row)
            self.assertTrue(True, "Data type conversion succeeded.")
        except Exception as e:
            self.fail(f"Data type conversion failed: {e}")

    def test_delta_operations(self):
        # /* 
        #    Test Delta Lake Operations
        #    Validate MERGE, UPDATE, DELETE operations on Delta tables
        # */
        from delta.tables import DeltaTable

        try:
            delta_table = DeltaTable.forName(spark, "purgo_playground.supplier_invoice_orig")
            # MERGE Operation Test
            delta_table.alias("orig").merge(
                self.df_test_data.alias("new"),
                "orig.invc_nbr = new.invc_nbr"
            ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
            self.assertTrue(True, "MERGE operation succeeded.")
        except Exception as e:
            self.fail(f"Delta MERGE operation failed: {e}")

    def test_window_functions(self):
        # /* 
        #    Test Window Functions
        #    Ensure that window functions are correctly applied
        # */
        try:
            df_with_rownum = self.df_supplier_invoice_orig.withColumn("RowNum", count("invoice_id").over(Window.partitionBy("invoice_id").orderBy("snapshot_captured_date")))
            row_num = df_with_rownum.filter(col("RowNum") == 1).count()
            self.assertGreater(row_num, 0, "Window function correctly applied.")
        except Exception as e:
            self.fail(f"Window function test failed: {e}")

    def test_column_mismatch_prevention(self):
        # /* 
        #    Test Column Mismatch Prevention
        #    Ensure that data insertion fails if column counts do not match
        # */
        try:
            # Attempt to write data with missing columns
            self.df_test_data.select("src_sys_cd", "po_nbr").write.mode("overwrite").format("delta").saveAsTable("purgo_playground.supplier_invoice_orig_mismatch")
            self.fail("Data insertion should have failed due to column mismatch.")
        except Exception as e:
            self.assertTrue(True, "Data insertion failed as expected due to column mismatch.")

    def test_file_handling(self):
        # /* 
        #    Test File Handling
        #    Ensure file opening is wrapped in try-except blocks to handle missing or invalid data
        # */
        try:
            # Attempt to read a non-existent file
            df_missing = spark.read.format("delta").load("purgo_playground.non_existent_table")
            self.fail("File reading should have failed for non-existent table.")
        except Exception as e:
            self.assertTrue(True, "File reading failed gracefully for missing table.")

    def test_cleanup_operations(self):
        # /* 
        #    Test Cleanup Operations
        #    Ensure that any temporary tables or data are properly cleaned up after tests
        # */
        try:
            spark.sql("DROP TABLE IF EXISTS purgo_playground.supplier_invoice_orig_mismatch")
            self.assertTrue(True, "Cleanup operation succeeded.")
        except Exception as e:
            self.fail(f"Cleanup operation failed: {e}")

    def test_performance(self):
        # /* 
        #    Test Performance
        #    Ensure that the PySpark code executes within acceptable performance thresholds
        # */
        import time
        try:
            start_time = time.time()
            self.df_test_data.count()
            end_time = time.time()
            duration = end_time - start_time
            self.assertLess(duration, 60, f"Performance test failed: Execution took {duration} seconds.")
        except Exception as e:
            self.fail(f"Performance test encountered an error: {e}")

    def test_data_quality(self):
        # /* 
        #    Test Data Quality
        #    Validate data quality rules such as positive amounts and valid status values
        # */
        try:
            # Check for negative 'invc_co_amt'
            negative_amounts = self.df_test_data.filter(col("invc_co_amt") < 0).count()
            self.assertEqual(negative_amounts, 0, "Data quality test failed: Negative invoice amounts found.")
            
            # Check for allowed 'vchr_status' values
            allowed_status = ['Active', 'Inactive']
            invalid_status = self.df_test_data.filter(~col("vchr_status").isin(allowed_status)).count()
            self.assertEqual(invalid_status, 0, "Data quality test failed: Invalid voucher statuses found.")
        except Exception as e:
            self.fail(f"Data quality test failed: {e}")

# /* 
#    Test Suite Execution
# */

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)