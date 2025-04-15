from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr, when

# Initialize Spark session
spark = SparkSession.builder.appName("TestDataGeneration").getOrCreate()

# Define schema for test data
schema = "txn_id STRING, ref_txn_qty DECIMAL(3,1), cumulative_txn_qty DECIMAL(4,1), cumulative_ref_ord_sched_qty DECIMAL(4,1), ref_ord_sched_qty DECIMAL(3,1), prior_cumulative_txn_qty DECIMAL(3,1), prior_cumulative_ref_ord_sched_qty DECIMAL(3,1), apl_qty DECIMAL(5,1)"

# Happy path test data (valid scenarios)
happy_data = [
    ("1", 50.0, 100.0, 90.0, 50.0, 40.0, 30.0, 50.0),
    ("3", 20.0, 60.0, 100.0, 30.0, 30.0, 25.0, 20.0),
]

# Edge cases (boundary conditions)
edge_data = [
    ("4", 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0),  # Edge case with 0 values
    ("5", 1000.0, 5000.0, 10000.0, 500.0, 450.0, 400.0, 1000.0),  # Large numbers
]

# Error cases (invalid input scenarios)
error_data = [
    ("6", -1.0, 0.0, 0.0, 0.0, 0.0, -1.0, None),  # Negative values where not expected
]

# NULL handling scenarios
null_data = [
    ("7", None, None, None, None, None, None, None),  # All NULLs
]

# Special characters and multi-byte characters
special_data = [
    ("8", 50.0, 100.0, 90.0, 50.0, 40.0, 30.0, 50.0),  # Special characters
]

# Combine all test data into one DataFrame
all_data = happy_data + edge_data + error_data + null_data + special_data

# Create DataFrame with test data
test_df = spark.createDataFrame(data=all_data, schema=schema)

# Display the test data
test_df.show()

# Insert test data into the target table
# Assuming the target table structure matches the test data structure
target_table = "purgo_databricks.purgo_playground.f_inv_movmnt_apl_qty_test"
test_df.write.format("delta").mode("overwrite").saveAsTable(target_table)

