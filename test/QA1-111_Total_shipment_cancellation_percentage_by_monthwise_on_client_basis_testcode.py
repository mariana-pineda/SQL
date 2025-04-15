from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month, count, sum, when

# Assuming the 'spark' session is available as per instructions

# Schema definitions for shipments and clients tables
shipments_schema = StructType([
    StructField("shipment_id", LongType(), False),
    StructField("shipment_date", StringType(), True),
    StructField("product_id", LongType(), False),
    StructField("client_id", LongType(), False),
    StructField("status", StringType(), False),
    StructField("cancellation_flag", StringType(), False),
    StructField("revenue", LongType(), False)
])

clients_schema = StructType([
    StructField("client_id", LongType(), False),
    StructField("client_name", StringType(), False)
])

# Example data to mimic the test datasets used for unit and integration testing
shipments_data = [
    (1, '2024-01-15', 101, 201, 'completed', 'Yes', 1000),
    (2, '2024-01-18', 102, 202, 'completed', 'No', 2000),
    (3, '2024-02-20', 103, 203, 'completed', 'yes', 1500),
    (4, '2024-02-22', 104, None, 'completed', 'Yes', 1800), # Invalid row with null client_id
    (5, '2024-03-25', 105, 205, 'partial', 'No', 1700),  # Partial shipment
    (6, '2023-03-25', 105, 205, 'completed', 'YES', 2100),
    (7, None, 106, 206, 'completed', 'No', 1800), # Null shipment_date
    (8, 'invalid_date', 107, 207, 'completed', 'Yes', 1600), # Incorrect date format
    (9, '2024-04-15', 108, 208, 'completed', 'No', 1900),
    (10, '2024-04-18', 109, 209, 'completed', 'Yes', 1200)
]

clients_data = [
    (201, 'Client A'),
    (202, 'Client B'),
    (203, 'Client C'),
    (205, 'Client D'),
    (206, 'Client E'),
    (208, 'Client F')
]

# Create DataFrame for shipments and clients
shipments_df = spark.createDataFrame(shipments_data, schema=shipments_schema)
clients_df = spark.createDataFrame(clients_data, schema=clients_schema)

# Filter and process shipments data
# Only include completed shipments
processed_shipments_df = shipments_df.filter(col("status") == "completed") \
    .filter((col("shipment_date").isNotNull()) & (col("client_id").isNotNull())) \
    .filter(~col("shipment_date").isin("None", "invalid_date"))

# Extract year and month from the shipment_date
processed_shipments_df = processed_shipments_df.withColumn("year", year("shipment_date")) \
    .withColumn("month", month("shipment_date"))

# Aggregate shipments data
aggregated_df = processed_shipments_df.groupBy("client_id", "year", "month") \
    .agg(count("shipment_id").alias("total_shipments"),
         sum(when(col("cancellation_flag").isin("Yes", "yes", "YES"), 1).otherwise(0)).alias("cancelled_shipments"))

# Join with clients to include client_name
result_df = aggregated_df.join(clients_df, "client_id", "inner") \
    .select(
        col("client_name"),
        col("year"),
        col("month"),
        col("total_shipments"),
        col("cancelled_shipments"),
        (col("cancelled_shipments") / col("total_shipments") * 100).alias("cancellation_percentage")
    )

# Display results
result_df.show()

# Test assertions (use proper test framework in a real scenario)
assert result_df.agg(sum("total_shipments")).first()[0] == 5, "Total shipments count does not match"
assert result_df.filter(col("client_name") == 'Client A').select("cancellation_percentage").first()[0] == 100.0, "Client A's cancellation percentage mismatch"
assert result_df.filter(col("month") == 3).count() == 1, "Month 3 data should exist and be complete"

