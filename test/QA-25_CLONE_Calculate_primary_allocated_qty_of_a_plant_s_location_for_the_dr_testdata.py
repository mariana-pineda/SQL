from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType

# Initialize Spark session
spark = SparkSession.builder.appName("Test Data Generation").getOrCreate()

# Define schema for f_inv_movmnt
f_inv_movmnt_schema = StructType([
    StructField("txn_id", StringType(), True),
    StructField("inv_loc", StringType(), True),
    StructField("financial_qty", DoubleType(), True),
    StructField("net_qty", DoubleType(), True),
    StructField("expired_dt", StringType(), True),  # YYYYMMDD format
    StructField("item_nbr", StringType(), True),
    StructField("unit_cost", DoubleType(), True),
    StructField("um_rate", DoubleType(), True),
    StructField("plant_loc_cd", StringType(), True),
    StructField("inv_stock_reference", StringType(), True),
    StructField("stock_type", StringType(), True),
    StructField("qty_on_hand", DoubleType(), True),
    StructField("qty_shipped", DoubleType(), True),
    StructField("cancel_dt", StringType(), True),  # YYYYMMDD format
    StructField("flag_active", StringType(), True),
    StructField("crt_dt", TimestampType(), True),
    StructField("updt_dt", TimestampType(), True)
])

# Create test data for f_inv_movmnt
f_inv_movmnt_data = [
    ("001", "loc1", 100.0, 80.0, "20231231", "item001", 20.50, 0.76, "PL1", "REF001", "RAW", 60.0, 20.0, "20231101", "yes", "2024-03-21T00:00:00.000+0000", "2024-03-22T00:00:00.000+0000"),
    ("002", "loc2", 200.0, 180.0, "20231231", "item002", 25.75, 0.76, "PL2", "REF002", "FG", 150.0, 30.0, "20231102", "no", "2024-03-21T00:00:00.000+0000", "2024-03-22T00:00:00.000+0000"),
    # Edge case with zero quantities
    ("003", "loc3", 0.0, 0.0, "20231231", "item003", 30.00, 0.76, "PL3", "REF003", "WIP", 0.0, 0.0, "20231103", "yes", "2024-03-21T00:00:00.000+0000", "2024-03-22T00:00:00.000+0000"),
    # NULL handling scenario
    ("004", None, None, 160.0, "20231231", "item004", None, 0.76, "PL4", "REF004", "OT", None, None, "20231104", "no", "2024-03-21T00:00:00.000+0000", "2024-03-22T00:00:00.000+0000"),
    # Special characters and multi-byte characters
    ("005", "特殊字符位置", 250.0, 230.0, "20231231", "項目005", 40.75, 0.76, "PL5", "REF005", "OT", 210.0, 40.0, "20231105", "yes", "2024-03-21T00:00:00.000+0000", "2024-03-22T00:00:00.000+0000"),
    # Negative quantity scenario
    ("006", "loc6", -50.0, -20.0, "20231231", "item006", 50.00, 0.76, "PL6", "REF006", "FG", -30.0, -20.0, "20231106", "no", "2024-03-21T00:00:00.000+0000", "2024-03-22T00:00:00.000+0000")
]

# Create DataFrame from test data
f_inv_movmnt_df = spark.createDataFrame(f_inv_movmnt_data, schema=f_inv_movmnt_schema)

# Show DataFrame for verification
f_inv_movmnt_df.show(truncate=False)

# Define schema for f_order
f_order_schema = StructType([
    StructField("order_nbr", StringType(), True),
    StructField("order_line_nbr", StringType(), True),
    StructField("primary_qty", DoubleType(), True),
    StructField("open_qty", DoubleType(), True),
    StructField("shipped_qty", DoubleType(), True),
    StructField("cancel_qty", DoubleType(), True),
    StructField("allocated_qty", DoubleType(), True)  # For calculated result
])

# Create test data for f_order
f_order_data = [
    ("001", "0011", 10.0, 5.0, 2.0, 1.0, 18.0),
    ("002", "0012", 20.0, 0.0, 3.0, 2.0, 25.0),
    ("003", "0013", 15.0, 10.0, 5.0, 5.0, 35.0),
    # Edge case with large numbers
    ("004", "0014", 1000000.0, 500000.0, 200000.0, 100000.0, 1800000.0),
    # NULL handling scenario
    ("005", "0015", None, None, None, None, 0.0),
    # Special characters in order numbers
    ("006", "特0016", 12.0, 6.0, 3.0, 2.0, 23.0),
    # Negative quantities for error checking
    ("007", "0017", -10.0, -5.0, -2.0, -1.0, -18.0)
]

# Create DataFrame from test data
f_order_df = spark.createDataFrame(f_order_data, schema=f_order_schema)

# Show DataFrame for verification
f_order_df.show(truncate=False)
