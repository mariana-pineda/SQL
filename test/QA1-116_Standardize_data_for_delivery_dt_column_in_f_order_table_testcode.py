# /* 
# Test Suite for purgo_playground.f_order.delivery_dt Validation
# This suite includes schema validation, data type checks, format validation,
# NULL handling, and Delta Lake operations tests.
# */

import unittest
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, length, regexp_extract
from pyspark.sql.types import DecimalType

class TestFOrderDeliveryDt(unittest.TestCase):
    """Unit tests for validating the delivery_dt column in purgo_playground.f_order table."""

    @classmethod
    def setUpClass(cls):
        """Setup for the test suite. Initializes the Spark session and loads the f_order table."""
        # -- Initialize Spark session if not already available
        cls.spark = SparkSession.builder.getOrCreate()

        try:
            # -- Load the purgo_playground.f_order table
            cls.f_order_df = cls.spark.table("purgo_databricks.purgo_playground.f_order")
        except Exception as e:
            # -- Handle table loading issues gracefully
            print(f"Error loading table purgo_playground.f_order: {e}")
            cls.f_order_df = None

    @classmethod
    def tearDownClass(cls):
        """Cleanup after all tests are run."""
        # -- Drop any temporary views or data if created
        try:
            cls.spark.catalog.dropTempView("temp_f_order")
        except:
            pass

    def test_schema_validation(self):
        """Validate that the f_order table schema matches the expected schema."""
        # /* 
        # Schema Validation Test
        # Ensures that the f_order table has the correct columns with expected data types.
        # */

        expected_schema = {
            'order_nbr': 'string',
            'order_type': 'bigint',
            'delivery_dt': 'decimal(38,0)',
            'order_qty': 'double',
            'sched_dt': 'decimal(38,0)',
            'expected_shipped_dt': 'decimal(38,0)',
            'actual_shipped_dt': 'decimal(38,0)',
            'order_line_nbr': 'string',
            'loc_tracker_id': 'string',
            'shipping_add': 'string',
            'primary_qty': 'double',
            'open_qty': 'double',
            'shipped_qty': 'double',
            'order_desc': 'string',
            'flag_return': 'string',
            'flag_cancel': 'string',
            'cancel_dt': 'decimal(38,0)',
            'cancel_qty': 'double',
            'crt_dt': 'timestamp',
            'updt_dt': 'timestamp'
        }

        for column, dtype in expected_schema.items():
            with self.subTest(column=column):
                actual_dtype = dict(self.f_order_df.dtypes)[column]
                self.assertEqual(actual_dtype.lower(), dtype, 
                                 f"Column {column} expected type {dtype} but got {actual_dtype}")

    def test_column_count(self):
        """Ensure that the number of columns in f_order matches the expected count."""
        # /* 
        # Column Count Test
        # Verifies that the f_order table has exactly 20 columns as defined.
        # */

        expected_column_count = 20
        actual_column_count = len(self.f_order_df.columns)
        self.assertEqual(actual_column_count, expected_column_count,
                         f"Expected {expected_column_count} columns, found {actual_column_count}")

    def test_delivery_dt_data_type(self):
        """Validate that delivery_dt is of type Decimal(38,0)."""
        # /* 
        # Data Type Validation Test
        # Checks that all delivery_dt entries are of Decimal(38,0) type.
        # */

        decimal_type = DecimalType(38, 0)
        # -- Check if delivery_dt column has the correct data type
        schema_dt = dict(self.f_order_df.dtypes)['delivery_dt']
        self.assertEqual(schema_dt.lower(), "decimal(38,0)", 
                         f"delivery_dt expected type Decimal(38,0) but got {schema_dt}")

    def test_delivery_dt_format(self):
        """Check that delivery_dt values are in yyyymmdd format."""
        # /* 
        # Format Validation Test
        # Ensures that all delivery_dt values conform to the yyyymmdd format.
        # */

        # -- Convert delivery_dt to string to apply regex
        df_formatted = self.f_order_df.withColumn("delivery_dt_str", col("delivery_dt").cast("string"))

        # -- Extract year, month, day using regex
        df_extracted = df_formatted.withColumn("year", regexp_extract(col("delivery_dt_str"), r'^(\d{4})', 1)) \
                                    .withColumn("month", regexp_extract(col("delivery_dt_str"), r'^\d{4}(\d{2})', 1)) \
                                    .withColumn("day", regexp_extract(col("delivery_dt_str"), r'^\d{6}(\d{2})$', 1))

        # -- Check if month is between 01 and 12 and day is between 01 and 31
        df_valid = df_extracted.filter(
            (col("month").between("01", "12")) &
            (col("day").between("01", "31"))
        )

        total_records = self.f_order_df.count()
        valid_records = df_valid.count()

        self.assertEqual(valid_records, total_records, 
                         "Not all delivery_dt values are in the yyyymmdd format or have valid month/day")

    def test_delivery_dt_not_null(self):
        """Ensure that there are no NULL values in delivery_dt."""
        # /* 
        # NULL Handling Test
        # Verifies that the delivery_dt column does not contain any NULL values.
        # */

        null_count = self.f_order_df.filter(col("delivery_dt").isNull()).count()
        self.assertEqual(null_count, 0, "delivery_dt column contains NULL values")

    def test_column_mismatch_prevention(self):
        """Ensure that the number of columns matches the target table schema before insertion."""
        # /* 
        # Column Mismatch Prevention Test
        # Validates that the DataFrame has the exact number of columns as the target table.
        # */

        target_columns = set(['order_nbr', 'order_type', 'delivery_dt', 'order_qty', 'sched_dt',
                              'expected_shipped_dt', 'actual_shipped_dt', 'order_line_nbr',
                              'loc_tracker_id', 'shipping_add', 'primary_qty', 'open_qty',
                              'shipped_qty', 'order_desc', 'flag_return', 'flag_cancel',
                              'cancel_dt', 'cancel_qty', 'crt_dt', 'updt_dt'])
        source_columns = set(self.f_order_df.columns)
        self.assertEqual(source_columns, target_columns, 
                         "Source DataFrame columns do not match target table schema")

    def test_merge_operation(self):
        """Test Delta Lake MERGE operation on f_order table."""
        # /* 
        # Delta Lake MERGE Operation Test
        # Validates that MERGE operations function correctly on the f_order table.
        # */

        try:
            # -- Create a temporary DataFrame for merging
            merge_df = self.spark.createDataFrame([
                ("ORDER001", 1, 20240911),
                ("ORDER021", 21, 20250101)
            ], ["order_nbr", "order_type", "delivery_dt"])

            # -- Perform MERGE operation
            (self.f_order_df.alias("target")
             .merge(
                 merge_df.alias("source"),
                 "target.order_nbr = source.order_nbr"
             )
             .whenMatchedUpdate(set={"delivery_dt": col("source.delivery_dt")})
             .whenNotMatchedInsert(values={
                 "order_nbr": "source.order_nbr",
                 "order_type": "source.order_type",
                 "delivery_dt": "source.delivery_dt",
                 # Add other required fields with default or source values
                 "order_qty": 0.0,
                 "sched_dt": 0,
                 "expected_shipped_dt": 0,
                 "actual_shipped_dt": 0,
                 "order_line_nbr": "",
                 "loc_tracker_id": "",
                 "shipping_add": "",
                 "primary_qty": 0.0,
                 "open_qty": 0.0,
                 "shipped_qty": 0.0,
                 "order_desc": "",
                 "flag_return": "N",
                 "flag_cancel": "N",
                 "cancel_dt": 0,
                 "cancel_qty": 0.0,
                 "crt_dt": "current_timestamp()",
                 "updt_dt": "current_timestamp()"
             })
             .execute()
            )

            # -- Validate MERGE results
            updated_record = self.spark.table("purgo_databricks.purgo_playground.f_order") \
                                       .filter(col("order_nbr") == "ORDER001") \
                                       .select("delivery_dt") \
                                       .collect()[0]['delivery_dt']
            self.assertEqual(updated_record, 20240911, "MERGE operation did not update delivery_dt correctly")

            new_record = self.spark.table("purgo_databricks.purgo_playground.f_order") \
                                     .filter(col("order_nbr") == "ORDER021") \
                                     .count()
            self.assertEqual(new_record, 1, "MERGE operation did not insert new record correctly")

        except Exception as e:
            self.fail(f"MERGE operation test failed: {e}")

    def test_update_operation(self):
        """Test Delta Lake UPDATE operation on f_order table."""
        # /* 
        # Delta Lake UPDATE Operation Test
        # Validates that UPDATE operations function correctly on the f_order table.
        # */

        try:
            # -- Perform UPDATE operation
            (self.f_order_df.alias("target")
             .update(
                 set={"delivery_dt": 20241231},
                 condition=col("order_nbr") == "ORDER002"
             )
            )

            # -- Validate UPDATE results
            updated_record = self.spark.table("purgo_databricks.purgo_playground.f_order") \
                                       .filter(col("order_nbr") == "ORDER002") \
                                       .select("delivery_dt") \
                                       .collect()[0]['delivery_dt']
            self.assertEqual(updated_record, 20241231, "UPDATE operation did not set delivery_dt correctly")

        except Exception as e:
            self.fail(f"UPDATE operation test failed: {e}")

    def test_delete_operation(self):
        """Test Delta Lake DELETE operation on f_order table."""
        # /* 
        # Delta Lake DELETE Operation Test
        # Validates that DELETE operations function correctly on the f_order table.
        # */

        try:
            # -- Perform DELETE operation
            (self.f_order_df.alias("target")
             .delete(
                 condition=col("order_nbr") == "ORDER003"
             )
            )

            # -- Validate DELETE results
            deleted_record = self.spark.table("purgo_databricks.purgo_playground.f_order") \
                                      .filter(col("order_nbr") == "ORDER003") \
                                      .count()
            self.assertEqual(deleted_record, 0, "DELETE operation did not remove the record correctly")

        except Exception as e:
            self.fail(f"DELETE operation test failed: {e}")

    def test_cleanup_operations(self):
        """Ensure that cleanup operations are performed correctly."""
        # /* 
        # Cleanup Operations Test
        # Validates that any temporary data or views are cleaned up after tests.
        # */

        try:
            self.spark.catalog.dropTempView("temp_f_order")
        except Exception:
            pass  # If the view does not exist, no action is needed

        # -- Verify cleanup
        self.assertFalse(self.spark.catalog.tableExists("temp_f_order"), 
                         "Temporary views were not cleaned up properly")

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)