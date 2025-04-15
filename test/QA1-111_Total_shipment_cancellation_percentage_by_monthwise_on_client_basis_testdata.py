from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month, sum, count, lit, when
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType, DoubleType

spark = SparkSession.builder.appName("Databricks Test Data Generation").getOrCreate()

# Define schema for test data
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

# Generate test data for shipments
shipments_data = [
    (1, '2024-01-15T00:00:00.000+0000', 101, 201, 'completed', 'Yes', 1000), # Valid completed shipment
    (2, '2024-01-18T00:00:00.000+0000', 102, 202, 'completed', 'No', 2000),  # Valid not cancelled shipment
    (3, '2024-02-20T00:00:00.000+0000', 103, 203, 'completed', 'yes', 1500), # Valid with lowercase cancellation flag
    (4, '2024-02-22T00:00:00.000+0000', 104, None,   'completed', 'Yes', 1800), # Invalid with null client_id
    (5, '2024-03-25T00:00:00.000+0000', 105, 205, 'partial', 'No', 1700),  # Partial shipment
    (6, '2023-03-25T00:00:00.000+0000', 105, 205, 'completed', 'YES', 2100), # Valid with uppercase cancellation flag
    (7, None, 106, 206, 'completed', 'No', 1800), # Null shipment_date
    (8, 'invalid_date', 107, 207, 'completed', 'Yes', 1600), # Incorrect date format
    (9, '2024-04-15T00:00:00.000+0000', 108, 208, 'completed', 'No', 1900), # Valid record
    (10, '2024-04-18T00:00:00.000+0000', 109, 209, 'completed', 'Yes', 1200) # Valid record
]

# Generate test data for clients
clients_data = [
    (201, 'Client A'),
    (202, 'Client B'),
    (203, 'Client C'),
    (205, 'Client D'),
    (206, 'Client E'),
    (208, 'Client F')
]

# Create DataFrames
shipments_df = spark.createDataFrame(shipments_data, schema=shipments_schema)
clients_df = spark.createDataFrame(clients_data, schema=clients_schema)

# Process dataframe
processed_shipments_df = shipments_df.filter(col("status") == "completed") \
    .filter((col("shipment_date").isNotNull()) & (col("client_id").isNotNull())) \
    .filter(~col("shipment_date").isin("None", "invalid_date"))

# Extract year and month from shipment_date, ignoring invalid and null dates
processed_shipments_df = processed_shipments_df.withColumn("year", year("shipment_date")) \
    .withColumn("month", month("shipment_date"))

# Calculate total shipments, cancelled shipments, and join with clients
aggregated_shipments_df = processed_shipments_df.groupBy("client_id", "year", "month") \
    .agg(count("*").alias("total_shipments"),
         sum(when(col("cancellation_flag").isin("Yes", "yes", "YES"), 1).otherwise(0)).alias("cancelled_shipments"))

result_df = aggregated_shipments_df.join(clients_df, "client_id", "inner") \
    .select(
        col("client_name"),
        col("year"),
        col("month"),
        col("total_shipments"),
        col("cancelled_shipments"),
        (col("cancelled_shipments") / col("total_shipments") * 100).alias("cancellation_percentage")
    )

result_df.show(20)


This code uses PySpark to generate test records, ensuring a variety of scenarios including valid, edge, and error cases. The data processing includes filtering for completed shipments, handling null and invalid dates, managing various cancellation flag formats, and joining with client data. Comments and considerations ensure that each scenario is appropriately addressed while maintaining consistency with Databricks data types and conventions.