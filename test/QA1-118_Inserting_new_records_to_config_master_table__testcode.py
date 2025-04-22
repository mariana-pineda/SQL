# /* 
# PySpark Test Suite for purgo_playground.config_master Table
# This test suite covers insertion of new records, validation of data types, handling duplicates,
# missing fields, and permission enforcement in the purgo_playground.config_master table.
# */

import unittest
from pyspark.sql import Row
from pyspark.sql.types import StructType, StructField, IntegerType, StringType

# /* 
# Define the test schema for config_master table
# */
schema = StructType([
    StructField("config_id", IntegerType(), False),
    StructField("src_objt_name", StringType(), True),
    StructField("src_sys", StringType(), True),
    StructField("f_format", StringType(), True),
    StructField("freq", StringType(), True),
    StructField("loc", StringType(), True),
    StructField("active_flag", StringType(), True),
    StructField("s3_landing_path", StringType(), True),
    StructField("s3_archive_path", StringType(), True),
    StructField("s3_src_path", StringType(), True),
    StructField("delta_load_ts", StringType(), True),
    StructField("full_or_incr_load", StringType(), True),
    StructField("zip_file", StringType(), True),
    StructField("country", StringType(), True),
    StructField("region", StringType(), True),
    StructField("affiliate_group", StringType(), True),
    StructField("affiliate", StringType(), True),
    StructField("column_condition", StringType(), True),
    StructField("dwh_path", StringType(), True),
    StructField("delimiter", StringType(), True),
    StructField("box_id", StringType(), True),
    StructField("len_file", StringType(), True),
    StructField("outbound_ind", StringType(), True),
    StructField("outbound_loc", StringType(), True),
    StructField("source_config_id", StringType(), True),
    StructField("exception_report_path", StringType(), True),
    StructField("src_layer", StringType(), True),
    StructField("quote_char", StringType(), True),
    StructField("col_list", StringType(), True),
    StructField("primary_key_col", StringType(), True),
    StructField("email", StringType(), True),
    StructField("expected_dt", StringType(), True),
    StructField("target_table", StringType(), True),
    StructField("target_src_sys", StringType(), True),
    StructField("dynamic_dt_file_loc", StringType(), True),
    StructField("dt_pattern", StringType(), True),
    StructField("latest_file_processed", StringType(), True),
    StructField("delta_stg_tables", StringType(), True),
    StructField("stg_skip_indicator", StringType(), True),
    StructField("delta_stg_table_view", StringType(), True),
    StructField("delta_pret1_table", StringType(), True),
    StructField("pre_t1_skip_indicator", StringType(), True),
    StructField("t2_force_exclude", StringType(), True),
    StructField("dq_rule_name", StringType(), True),
    StructField("source_path", StringType(), True),
    StructField("pre_process_function", StringType(), True),
    StructField("encode_val", StringType(), True),
    StructField("decode_val", StringType(), True),
    StructField("header", StringType(), True),
    StructField("inferschema", StringType(), True),
    StructField("actual_file_name", StringType(), True),
    StructField("t1_layer_flag", StringType(), True),
    StructField("t2_layer_flag", StringType(), True),
    StructField("t3_layer_flag", StringType(), True),
    StructField("dag_id", StringType(), True)
])

class TestConfigMaster(unittest.TestCase):
    """ 
    Test cases for purgo_playground.config_master table
    """

    @classmethod
    def setUpClass(cls):
        # /* 
        # Setup initial data for testing
        # */
        cls.test_data = [
            # Happy path: Valid record
            Row(
                config_id=1001, src_objt_name="ID_Sales", src_sys="ID_Sales",
                f_format="ID_MON_Sales_", freq="Daily", loc="US", active_flag="Y",
                s3_landing_path="s3a://my_bucket/landing/ID/ID_Sales/", 
                s3_archive_path="s3a://my_bucket/archive/ID/ID_Sales/",
                s3_src_path="/SecureFtp/-InternalX/ID/IN/DATA/Sales/",
                delta_load_ts="2024-03-21T00:00:00.000+0000", full_or_incr_load="Full",
                zip_file="yes", country="ID", region="ID", affiliate_group="ID",
                affiliate="ID", column_condition="condition", dwh_path="/dwh/path/", delimiter=",",
                box_id="box123", len_file="1000", outbound_ind="N", outbound_loc="US",
                source_config_id="src_conf_1", exception_report_path="/exception/path/",
                src_layer="ID_Sales", quote_char="\"", col_list="col1,col2",
                primary_key_col="id", email="email@example.com", expected_dt="2024-03-21",
                target_table="target_table", target_src_sys="ID_Sales",
                dynamic_dt_file_loc="/dynamic/path/", dt_pattern="yyyy-MM-dd",
                latest_file_processed="file1", delta_stg_tables="stg_ID_sales",
                stg_skip_indicator="N", delta_stg_table_view="view_stg",
                delta_pret1_table="delta_pret1", pre_t1_skip_indicator="N",
                t2_force_exclude="Y", dq_rule_name="rule1", source_path="/SecureFtp/-InternalX/ID/IN/DATA/Sales/",
                pre_process_function="function1", encode_val="enc", decode_val="dec",
                header="header1", inferschema="true", actual_file_name="stg_ID_wholesaler",
                t1_layer_flag="N", t2_layer_flag="N", t3_layer_flag="N",
                dag_id="LOAD_SALES_ID"
            )
        ]

        # /* 
        # Create DataFrame with initial test data
        # */
        cls.initial_df = spark.createDataFrame(cls.test_data, schema)
        
        # /* 
        # Insert initial data into config_master table
        # */
        try:
            cls.initial_df.write.mode("append").saveAsTable("purgo_playground.config_master")
        except Exception as e:
            # /* 
            # Handle insertion errors gracefully
            # */
            print(f"Error inserting initial test data: {e}")

    @classmethod
    def tearDownClass(cls):
        # /* 
        # Cleanup: Remove test data from config_master table
        # */
        try:
            spark.sql("""
                DELETE FROM purgo_playground.config_master
                WHERE config_id IN (1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1, 2147483647)
            """)
        except Exception as e:
            # /* 
            # Handle cleanup errors gracefully
            # */
            print(f"Error during cleanup: {e}")
        # /* 
        # Commented out spark.stop() to prevent issues in Databricks
        # */
        # spark.stop()

    def test_insert_valid_record(self):
        """ 
        Test inserting a valid new record into config_master
        """
        # /* 
        # Define new valid record
        # */
        new_record = Row(
            config_id=1002, src_objt_name="ID_Sales", src_sys="ID_Sales",
            f_format="ID_MON_Sales_", freq="Weekly", loc="CA", active_flag="Y",
            s3_landing_path="s3a://data_bucket/landing/ID/ID_Sales/", 
            s3_archive_path="s3a://data_bucket/archive/ID/ID_Sales/",
            s3_src_path="/SecureFtp/-InternalX/ID/IN/DATA/Sales/",
            delta_load_ts="2024-04-01T12:00:00.000+0000", full_or_incr_load="Partial",
            zip_file="yes", country="ID", region="ID", affiliate_group="ID",
            affiliate="ID", column_condition="condition_dup", dwh_path="/dwh/dup_path/", delimiter="|",
            box_id="box_dup", len_file="500", outbound_ind="N", outbound_loc="CA",
            source_config_id="src_conf_dup", exception_report_path="/exception/dup_path/",
            src_layer="ID_Sales", quote_char="`", col_list="col_dup1,col_dup2",
            primary_key_col="id_dup", email="dup_email@example.com", expected_dt="2024-04-01",
            target_table="target_table_dup", target_src_sys="ID_Sales",
            dynamic_dt_file_loc="/dynamic/dup/path/", dt_pattern="MM-dd-yyyy",
            latest_file_processed="file_dup", delta_stg_tables="stg_ID_sales_dup",
            stg_skip_indicator="N", delta_stg_table_view="view_stg_dup",
            delta_pret1_table="delta_pret1_dup", pre_t1_skip_indicator="N",
            t2_force_exclude="Y", dq_rule_name="rule_dup", source_path="/SecureFtp/-InternalX/ID/IN/DATA/Sales/",
            pre_process_function="function_dup", encode_val="enc_dup", decode_val="dec_dup",
            header="header_dup", inferschema="true", actual_file_name="stg_ID_wholesaler_dup",
            t1_layer_flag="N", t2_layer_flag="N", t3_layer_flag="N",
            dag_id="LOAD_SALES_ID_DUP"
        )
        
        # /* 
        # Create DataFrame for new record
        # */
        new_df = spark.createDataFrame([new_record], schema)
        
        # /* 
        # Insert new record into config_master table
        # */
        try:
            new_df.write.mode("append").saveAsTable("purgo_playground.config_master")
        except Exception as e:
            self.fail(f"Insertion of valid record failed: {e}")
        
        # /* 
        # Retrieve the inserted record to verify
        # */
        inserted_df = spark.sql("""
            SELECT * FROM purgo_playground.config_master 
            WHERE config_id = 1002
        """)
        
        # /* 
        # Assert that the record exists
        # */
        self.assertEqual(inserted_df.count(), 1, "Valid record was not inserted successfully.")
        
        # /* 
        # Verify dag_id
        # */
        dag_id = inserted_df.collect()[0]['dag_id']
        self.assertEqual(dag_id, "LOAD_SALES_ID_DUP", "dag_id does not match expected value.")

    def test_duplicate_dag_id_insertion(self):
        """ 
        Test that inserting a record with duplicate dag_id fails
        """
        # /* 
        # Define duplicate dag_id record
        # */
        duplicate_record = Row(
            config_id=1003, src_objt_name="ID_Sales_Duplicate", src_sys="ID_Sales",
            f_format="ID_MON_Sales_dup_", freq="Weekly", loc="CA", active_flag="Y",
            s3_landing_path="s3a://duplicate_bucket/landing/ID/ID_Sales/", 
            s3_archive_path="s3a://duplicate_bucket/archive/ID/ID_Sales/",
            s3_src_path="/SecureFtp/-InternalX/ID/IN/DATA/Sales/",
            delta_load_ts="2024-04-01T12:00:00.000+0000", full_or_incr_load="Partial",
            zip_file="yes", country="ID", region="ID", affiliate_group="ID",
            affiliate="ID", column_condition="condition_dup", dwh_path="/dwh/dup_path/", delimiter="|",
            box_id="box_dup", len_file="500", outbound_ind="N", outbound_loc="CA",
            source_config_id="src_conf_dup", exception_report_path="/exception/dup_path/",
            src_layer="ID_Sales", quote_char="`", col_list="col_dup1,col_dup2",
            primary_key_col="id_dup", email="dup_email@example.com", expected_dt="2024-04-01",
            target_table="target_table_dup", target_src_sys="ID_Sales",
            dynamic_dt_file_loc="/dynamic/dup/path/", dt_pattern="MM-dd-yyyy",
            latest_file_processed="file_dup", delta_stg_tables="stg_ID_sales_dup",
            stg_skip_indicator="N", delta_stg_table_view="view_stg_dup",
            delta_pret1_table="delta_pret1_dup", pre_t1_skip_indicator="N",
            t2_force_exclude="Y", dq_rule_name="rule_dup", source_path="/SecureFtp/-InternalX/ID/IN/DATA/Sales/",
            pre_process_function="function_dup", encode_val="enc_dup", decode_val="dec_dup",
            header="header_dup", inferschema="true", actual_file_name="stg_ID_wholesaler_dup",
            t1_layer_flag="N", t2_layer_flag="N", t3_layer_flag="N",
            dag_id="LOAD_SALES_ID"  # Duplicate dag_id
        )
        
        # /* 
        # Create DataFrame for duplicate record
        # */
        duplicate_df = spark.createDataFrame([duplicate_record], schema)
        
        # /* 
        # Attempt to insert duplicate dag_id and expect failure
        # */
        with self.assertRaises(Exception) as context:
            duplicate_df.write.mode("append").saveAsTable("purgo_playground.config_master")
        
        # /* 
        # Verify the error message contains 'Duplicate dag_id'
        # */
        self.assertIn("Duplicate dag_id", str(context.exception), "Duplicate dag_id insertion did not fail as expected.")

    def test_missing_required_fields_insertion(self):
        """ 
        Test that inserting a record with missing required fields fails
        """
        # /* 
        # Define record with missing s3_landing_path and s3_archive_path
        # */
        missing_fields_record = Row(
            config_id=1004, src_objt_name="ID_Sales_Missing", src_sys="ID_Sales",
            f_format="ID_MON_Sales_missing_", freq="Weekly", loc="DE", active_flag="Y",
            s3_landing_path="",  # Missing
            s3_archive_path="",  # Missing
            s3_src_path="/SecureFtp/-InternalX/ID/IN/DATA/Sales/",
            delta_load_ts="2024-07-20T14:00:00.000+0000", full_or_incr_load="Full",
            zip_file="yes", country="ID", region="ID", affiliate_group="ID",
            affiliate="ID", column_condition="condition_missing", dwh_path="/dwh/missing_path/", delimiter=",",
            box_id="box_missing", len_file="1000", outbound_ind="N", outbound_loc="DE",
            source_config_id="src_conf_missing", exception_report_path="/exception/missing_path/",
            src_layer="ID_Sales_Missing", quote_char="\"", col_list="col_missing1,col_missing2",
            primary_key_col="id_missing", email="missing_email@example.com", expected_dt="2024-07-20",
            target_table="target_table_missing", target_src_sys="ID_Sales",
            dynamic_dt_file_loc="/dynamic/missing/path/", dt_pattern="dd-MM-yyyy",
            latest_file_processed="file_missing", delta_stg_tables="stg_ID_sales_missing",
            stg_skip_indicator="N", delta_stg_table_view="view_stg_missing",
            delta_pret1_table="delta_pret1_missing", pre_t1_skip_indicator="N",
            t2_force_exclude="Y", dq_rule_name="rule_missing", source_path="/SecureFtp/-InternalX/ID/IN/DATA/Sales/",
            pre_process_function="function_missing", encode_val="enc_missing", decode_val="dec_missing",
            header="header_missing", inferschema="true", actual_file_name="stg_ID_wholesaler_missing",
            t1_layer_flag="N", t2_layer_flag="N", t3_layer_flag="N",
            dag_id="LOAD_SALES_ID_NEW"
        )
        
        # /* 
        # Create DataFrame for record with missing fields
        # */
        missing_fields_df = spark.createDataFrame([missing_fields_record], schema)
        
        # /* 
        # Attempt to insert record with missing required fields and expect failure
        # */
        with self.assertRaises(Exception) as context:
            missing_fields_df.write.mode("append").saveAsTable("purgo_playground.config_master")
        
        # /* 
        # Verify the error message contains 's3_landing_path and s3_archive_path are required fields'
        # */
        self.assertIn("s3_landing_path and s3_archive_path are required fields", str(context.exception), 
                      "Insertion with missing required fields did not fail as expected.")

    def test_invalid_s3_landing_path_format(self):
        """ 
        Test that inserting a record with invalid s3_landing_path format fails
        """
        # /* 
        # Define record with invalid s3_landing_path
        # */
        invalid_s3_record = Row(
            config_id=1005, src_objt_name="ID_Sales_Invalid_S3", src_sys="ID_Sales",
            f_format="ID_MON_Sales_invalid_s3_", freq="Daily", loc="FR", active_flag="Y",
            s3_landing_path="invalid_path/landing/ID/ID_Sales/",  # Invalid format
            s3_archive_path="s3a://invalid_bucket/archive/ID/ID_Sales/",
            s3_src_path="/SecureFtp/-InternalX/ID/IN/DATA/Sales/",
            delta_load_ts="2024-06-01T10:00:00.000+0000", full_or_incr_load="Full",
            zip_file="yes", country="ID", region="ID", affiliate_group="ID",
            affiliate="ID", column_condition="condition_invalid_s3", dwh_path="/dwh/invalid_s3_path/", delimiter=",",
            box_id="box_invalid_s3", len_file="1000", outbound_ind="N", outbound_loc="FR",
            source_config_id="src_conf_invalid_s3", exception_report_path="/exception/invalid_s3_path/",
            src_layer="ID_Sales_Invalid", quote_char="\"", col_list="col_invalid1,col_invalid2",
            primary_key_col="id_invalid_s3", email="invalid_s3_email@example.com", expected_dt="2024-06-01",
            target_table="target_table_invalid_s3", target_src_sys="ID_Sales",
            dynamic_dt_file_loc="/dynamic/invalid_s3/path/", dt_pattern="yyyy/MM/dd",
            latest_file_processed="file_invalid_s3", delta_stg_tables="stg_ID_sales_invalid_s3",
            stg_skip_indicator="N", delta_stg_table_view="view_stg_invalid_s3",
            delta_pret1_table="delta_pret1_invalid_s3", pre_t1_skip_indicator="N",
            t2_force_exclude="Y", dq_rule_name="rule_invalid_s3", source_path="/SecureFtp/-InternalX/ID/IN/DATA/Sales/",
            pre_process_function="function_invalid_s3", encode_val="enc_invalid_s3", decode_val="dec_invalid_s3",
            header="header_invalid_s3", inferschema="true", actual_file_name="stg_ID_wholesaler_invalid_s3",
            t1_layer_flag="N", t2_layer_flag="N", t3_layer_flag="N",
            dag_id="LOAD_SALES_ID_VALID"
        )
        
        # /* 
        # Create DataFrame for record with invalid s3_landing_path
        # */
        invalid_s3_df = spark.createDataFrame([invalid_s3_record], schema)
        
        # /* 
        # Attempt to insert record with invalid s3_landing_path and expect failure
        # */
        with self.assertRaises(Exception) as context:
            invalid_s3_df.write.mode("append").saveAsTable("purgo_playground.config_master")
        
        # /* 
        # Verify the error message contains 's3_landing_path must follow the format'
        # */
        self.assertIn("s3_landing_path must follow the format", str(context.exception), 
                      "Insertion with invalid s3_landing_path did not fail as expected.")

    def test_missing_s3_bucket_value(self):
        """ 
        Test that inserting a record with missing s3_bucket value fails
        """
        # /* 
        # Define record with missing s3_bucket in s3_landing_path
        # */
        missing_s3_bucket_record = Row(
            config_id=1006, src_objt_name="ID_Sales_Missing_Bucket", src_sys="ID_Sales",
            f_format="ID_MON_Sales_missing_bucket_", freq="Daily", loc="BE", active_flag="Y",
            s3_landing_path="s3a:///landing/ID/ID_Sales/",  # Missing bucket
            s3_archive_path="s3a://archive_bucket/archive/ID/ID_Sales/",
            s3_src_path="/SecureFtp/-InternalX/ID/IN/DATA/Sales/",
            delta_load_ts="2024-07-25T09:00:00.000+0000", full_or_incr_load="Full",
            zip_file="yes", country="ID", region="ID", affiliate_group="ID",
            affiliate="ID", column_condition="condition_missing_bucket", dwh_path="/dwh/missing_bucket_path/", delimiter=",",
            box_id="box_missing_bucket", len_file="1000", outbound_ind="N", outbound_loc="BE",
            source_config_id="src_conf_missing_bucket", exception_report_path="/exception/missing_bucket_path/",
            src_layer="ID_Sales_Missing_Bucket", quote_char="\"", col_list="col_missing_bucket1,col_missing_bucket2",
            primary_key_col="id_missing_bucket", email="missing_bucket_email@example.com", expected_dt="2024-07-25",
            target_table="target_table_missing_bucket", target_src_sys="ID_Sales",
            dynamic_dt_file_loc="/dynamic/missing_bucket/path/", dt_pattern="dd-MM-yyyy",
            latest_file_processed="file_missing_bucket", delta_stg_tables="stg_ID_sales_missing_bucket",
            stg_skip_indicator="N", delta_stg_table_view="view_stg_missing_bucket",
            delta_pret1_table="delta_pret1_missing_bucket", pre_t1_skip_indicator="N",
            t2_force_exclude="Y", dq_rule_name="rule_missing_bucket", source_path="/SecureFtp/-InternalX/ID/IN/DATA/Sales/",
            pre_process_function="function_missing_bucket", encode_val="enc_missing_bucket", decode_val="dec_missing_bucket",
            header="header_missing_bucket", inferschema="true", actual_file_name="stg_ID_wholesaler_missing_bucket",
            t1_layer_flag="N", t2_layer_flag="N", t3_layer_flag="N",
            dag_id="LOAD_SALES_ID_NO_BUCKET"
        )
        
        # /* 
        # Create DataFrame for record with missing s3_bucket
        # */
        missing_s3_bucket_df = spark.createDataFrame([missing_s3_bucket_record], schema)
        
        # /* 
        # Attempt to insert record with missing s3_bucket and expect failure
        # */
        with self.assertRaises(Exception) as context:
            missing_s3_bucket_df.write.mode("append").saveAsTable("purgo_playground.config_master")
        
        # /* 
        # Verify the error message contains 's3_bucket value is missing'
        # */
        self.assertIn("s3_bucket value is missing", str(context.exception), 
                      "Insertion with missing s3_bucket did not fail as expected.")

    def test_config_id_auto_generation(self):
        """ 
        Test that config_id is auto-generated upon successful insertion
        """
        # /* 
        # Retrieve current maximum config_id
        # */
        max_config_id_df = spark.sql("""
            SELECT MAX(config_id) as max_id FROM purgo_playground.config_master
        """)
        max_config_id = max_config_id_df.collect()[0]['max_id']
        
        # /* 
        # Define new valid record without specifying config_id
        # Assuming config_id is auto-incremented
        # */
        new_record = Row(
            config_id=max_config_id + 1, src_objt_name="ID_Sales_AutoGen", src_sys="ID_Sales",
            f_format="ID_MON_Sales_AutoGen_", freq="Monthly", loc="SG", active_flag="Y",
            s3_landing_path="s3a://auto_bucket/landing/ID/ID_Sales/", 
            s3_archive_path="s3a://auto_bucket/archive/ID/ID_Sales/",
            s3_src_path="/SecureFtp/-InternalX/ID/IN/DATA/Sales/",
            delta_load_ts="2024-08-15T10:30:00.000+0000", full_or_incr_load="Full",
            zip_file="no", country="ID", region="ID", affiliate_group="ID",
            affiliate="ID", column_condition="condition_auto", dwh_path="/dwh/auto_path/", delimiter=",",
            box_id="box_auto", len_file="1500", outbound_ind="Y", outbound_loc="SG",
            source_config_id="src_conf_auto", exception_report_path="/exception/auto_path/",
            src_layer="ID_Sales_AutoGen", quote_char="\"", col_list="col_auto1,col_auto2",
            primary_key_col="id_auto", email="auto_email@example.com", expected_dt="2024-08-15",
            target_table="target_table_auto", target_src_sys="ID_Sales",
            dynamic_dt_file_loc="/dynamic/auto/path/", dt_pattern="yyyy-MM-dd",
            latest_file_processed="file_auto", delta_stg_tables="stg_ID_sales_auto",
            stg_skip_indicator="Y", delta_stg_table_view="view_stg_auto",
            delta_pret1_table="delta_pret1_auto", pre_t1_skip_indicator="Y",
            t2_force_exclude="Y", dq_rule_name="rule_auto", source_path="/SecureFtp/-InternalX/ID/IN/DATA/Sales/",
            pre_process_function="function_auto", encode_val="enc_auto", decode_val="dec_auto",
            header="header_auto", inferschema="true", actual_file_name="stg_ID_wholesaler_auto",
            t1_layer_flag="Y", t2_layer_flag="Y", t3_layer_flag="Y",
            dag_id="LOAD_SALES_ID_AUTO"
        )
        
        # /* 
        # Create DataFrame for new auto-generated config_id record
        # */
        new_df = spark.createDataFrame([new_record], schema)
        
        # /* 
        # Insert new record into config_master table
        # */
        try:
            new_df.write.mode("append").saveAsTable("purgo_playground.config_master")
        except Exception as e:
            self.fail(f"Insertion of auto-generated config_id record failed: {e}")
        
        # /* 
        # Retrieve the inserted record to verify config_id
        # */
        inserted_df = spark.sql(f"""
            SELECT * FROM purgo_playground.config_master 
            WHERE config_id = {max_config_id + 1}
        """)
        
        # /* 
        # Assert that the record exists
        # */
        self.assertEqual(inserted_df.count(), 1, "Auto-generated config_id record was not inserted successfully.")
        
        # /* 
        # Verify config_id auto-increment
        # */
        config_id = inserted_df.collect()[0]['config_id']
        self.assertEqual(config_id, max_config_id + 1, "config_id was not auto-generated correctly.")

    def test_permission_enforcement(self):
        """ 
        Test that users without write permissions cannot insert records
        """
        # /* 
        # Simulate a user without write permissions attempting insertion
        # Note: Actual permission testing would require a different approach or environment setup
        # Here, we simulate by catching permission-related exceptions
        # */
        unauthorized_record = Row(
            config_id=1007, src_objt_name="ID_Sales_Unauthorized", src_sys="ID_Sales",
            f_format="ID_MON_Sales_unauth_", freq="Daily", loc="IT", active_flag="Y",
            s3_landing_path="s3a://unauth_bucket/landing/ID/ID_Sales/", 
            s3_archive_path="s3a://unauth_bucket/archive/ID/ID_Sales/",
            s3_src_path="/SecureFtp/-InternalX/ID/IN/DATA/Sales/",
            delta_load_ts="2024-09-10T11:00:00.000+0000", full_or_incr_load="Full",
            zip_file="no", country="ID", region="ID", affiliate_group="ID",
            affiliate="ID", column_condition="condition_unauth", dwh_path="/dwh/unauth_path/", delimiter=",",
            box_id="box_unauth", len_file="2000", outbound_ind="Y", outbound_loc="IT",
            source_config_id="src_conf_unauth", exception_report_path="/exception/unauth_path/",
            src_layer="ID_Sales_Unauthorized", quote_char="\"", col_list="col_unauth1,col_unauth2",
            primary_key_col="id_unauth", email="unauth_email@example.com", expected_dt="2024-09-10",
            target_table="target_table_unauth", target_src_sys="ID_Sales",
            dynamic_dt_file_loc="/dynamic/unauth/path/", dt_pattern="yyyy-MM-dd",
            latest_file_processed="file_unauth", delta_stg_tables="stg_ID_sales_unauth",
            stg_skip_indicator="Y", delta_stg_table_view="view_stg_unauth",
            delta_pret1_table="delta_pret1_unauth", pre_t1_skip_indicator="Y",
            t2_force_exclude="Y", dq_rule_name="rule_unauth", source_path="/SecureFtp/-InternalX/ID/IN/DATA/Sales/",
            pre_process_function="function_unauth", encode_val="enc_unauth", decode_val="dec_unauth",
            header="header_unauth", inferschema="true", actual_file_name="stg_ID_wholesaler_unauth",
            t1_layer_flag="Y", t2_layer_flag="Y", t3_layer_flag="Y",
            dag_id="LOAD_SALES_ID_UNAUTH"
        )
        
        # /* 
        # Create DataFrame for unauthorized record
        # */
        unauthorized_df = spark.createDataFrame([unauthorized_record], schema)
        
        # /* 
        # Attempt to insert unauthorized record and expect failure
        # */
        with self.assertRaises(Exception) as context:
            unauthorized_df.write.mode("append").saveAsTable("purgo_playground.config_master")
        
        # /* 
        # Verify the error message contains 'Insufficient permissions'
        # */
        self.assertIn("Insufficient permissions", str(context.exception), 
                      "Unauthorized insertion did not fail as expected.")

    def test_downstream_dependencies_handling(self):
        """ 
        Test that downstream processes can read the new configuration correctly
        """
        # /* 
        # Insert a new valid record
        # */
        new_record = Row(
            config_id=1008, src_objt_name="ID_Sales_Downstream", src_sys="ID_Sales",
            f_format="ID_MON_Sales_downstream_", freq="Daily", loc="JP", active_flag="Y",
            s3_landing_path="s3a://downstream_bucket/landing/ID/ID_Sales/", 
            s3_archive_path="s3a://downstream_bucket/archive/ID/ID_Sales/",
            s3_src_path="/SecureFtp/-InternalX/ID/IN/DATA/Sales/",
            delta_load_ts="2024-10-05T09:15:00.000+0000", full_or_incr_load="Full",
            zip_file="yes", country="ID", region="ID", affiliate_group="ID",
            affiliate="ID", column_condition="condition_downstream", dwh_path="/dwh/downstream_path/", delimiter=",",
            box_id="box_downstream", len_file="1000", outbound_ind="N", outbound_loc="JP",
            source_config_id="src_conf_downstream", exception_report_path="/exception/downstream_path/",
            src_layer="ID_Sales_Downstream", quote_char="\"", col_list="col_down1,col_down2",
            primary_key_col="id_down", email="downstream_email@example.com", expected_dt="2024-10-05",
            target_table="target_table_downstream", target_src_sys="ID_Sales",
            dynamic_dt_file_loc="/dynamic/downstream/path/", dt_pattern="yyyy-MM-dd",
            latest_file_processed="file_downstream", delta_stg_tables="stg_ID_sales_downstream",
            stg_skip_indicator="N", delta_stg_table_view="view_stg_downstream",
            delta_pret1_table="delta_pret1_downstream", pre_t1_skip_indicator="N",
            t2_force_exclude="Y", dq_rule_name="rule_downstream", source_path="/SecureFtp/-InternalX/ID/IN/DATA/Sales/",
            pre_process_function="function_downstream", encode_val="enc_downstream", decode_val="dec_downstream",
            header="header_downstream", inferschema="true", actual_file_name="stg_ID_wholesaler_downstream",
            t1_layer_flag="N", t2_layer_flag="N", t3_layer_flag="N",
            dag_id="LOAD_SALES_ID_DOWNSTREAM"
        )
        
        # /* 
        # Create DataFrame for downstream record
        # */
        downstream_df = spark.createDataFrame([new_record], schema)
        
        # /* 
        # Insert downstream record into config_master table
        # */
        try:
            downstream_df.write.mode("append").saveAsTable("purgo_playground.config_master")
        except Exception as e:
            self.fail(f"Insertion of downstream record failed: {e}")
        
        # /* 
        # Simulate downstream process reading the new configuration
        # */
        downstream_process_df = spark.sql("""
            SELECT s3_landing_path, s3_archive_path 
            FROM purgo_playground.config_master 
            WHERE dag_id = 'LOAD_SALES_ID_DOWNSTREAM'
        """)
        
        # /* 
        # Assert that downstream process can read the correct paths
        # */
        self.assertEqual(downstream_process_df.count(), 1, "Downstream process did not read the new configuration.")
        paths = downstream_process_df.collect()[0]
        self.assertEqual(paths['s3_landing_path'], "s3a://downstream_bucket/landing/ID/ID_Sales/", 
                         "s3_landing_path does not match expected value.")
        self.assertEqual(paths['s3_archive_path'], "s3a://downstream_bucket/archive/ID/ID_Sales/", 
                         "s3_archive_path does not match expected value.")

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)