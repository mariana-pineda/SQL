from pyspark.sql import SparkSession
from pyspark.sql.functions import when, col
from pyspark.sql.types import StructType, StructField, StringType, DecimalType

# Initialize Spark session
spark = SparkSession.builder \
    .appName("APL_QTY_Test") \
    .getOrCreate()

# Define the schema for f_inv_movmnt_apl_qty_result
schema = StructType([
    StructField("txn_id", StringType(), True),
    StructField("ref_txn_qty", DecimalType(3, 1), True),
    StructField("cumulative_txn_qty", DecimalType(4, 1), True),
    StructField("cumulative_ref_ord_sched_qty", DecimalType(4, 1), True),
    StructField("ref_ord_sched_qty", DecimalType(3, 1), True),
    StructField("prior_cumulative_txn_qty", DecimalType(3, 1), True),
    StructField("prior_cumulative_ref_ord_sched_qty", DecimalType(3, 1), True),
    StructField("apl_qty", DecimalType(5, 1), True),
])

# Generate test data based on the logic
data = [
    ("1", 50.0, 100.0, 90.0, 50.0, 40.0, 30.0, None),
    ("2", -10.0, 80.0, 70.0, 40.0, 50.0, 45.0, None),
    ("3", 20.0, 60.0, 100.0, 30.0, 30.0, 25.0, None),
]

# Create DataFrame from data
df = spark.createDataFrame(data, schema)

# Implement logic for apl_qty calculation
df = df.withColumn("apl_qty", when(
    (col("ref_txn_qty") > 0) & (col("cumulative_txn_qty") >= col("cumulative_ref_ord_sched_qty")),
    when(col("prior_cumulative_ref_ord_sched_qty") < col("prior_cumulative_txn_qty"),
         col("ref_ord_sched_qty") - (col("prior_cumulative_txn_qty") - col("prior_cumulative_ref_ord_sched_qty"))).otherwise(col("ref_ord_sched_qty"))
).otherwise(when(
    (col("ref_txn_qty") > 0) & (col("cumulative_ref_ord_sched_qty") >= col("cumulative_txn_qty")),
    when(col("prior_cumulative_ref_ord_sched_qty") > col("prior_cumulative_txn_qty"),
         col("ref_txn_qty") - (col("prior_cumulative_ref_ord_sched_qty") - col("prior_cumulative_txn_qty"))).otherwise(col("ref_txn_qty"))
).otherwise(when(
    (col("ref_txn_qty") < 0) & (col("cumulative_txn_qty") != 0) & (col("cumulative_ref_ord_sched_qty") > 0),
    col("ref_txn_qty")
).otherwise(None))))

# Show the DataFrame with calculated apl_qty
df.show(truncate=False)

# Validate schema
assert df.schema == schema, "Schema mismatch detected!"

# Check number of columns matches target table
assert len(df.columns) == len(schema.fieldNames()), "Column count mismatch detected!"

# Check data quality
assert df.select("apl_qty").where(df.apl_qty.isNull()).count() < df.count(), "Data quality issue detected!"

# Perform integration test
df.write.format("delta").mode("overwrite").saveAsTable("purgo_playground.purgo_playground.f_inv_movmnt_apl_qty_result")

# Verify Delta Lake operations
result_df = spark.sql("""SELECT * FROM purgo_playground.purgo_playground.f_inv_movmnt_apl_qty_result""")
assert result_df.count() == df.count(), "Data insertion error!"

# Clean up any temporary data
spark.sql("""DROP TABLE IF EXISTS purgo_playground.purgo_playground.f_inv_movmnt_apl_qty_result""")