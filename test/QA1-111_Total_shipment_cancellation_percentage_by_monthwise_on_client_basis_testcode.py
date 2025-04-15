from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month, when, count, sum, round

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Shipment Statistics Analysis") \
    .getOrCreate()

# Define schemas for testing
shipments_schema = "shipment_id BIGINT, shipment_date TIMESTAMP, product_id BIGINT, client_id BIGINT, status STRING, cancellation_flag STRING, revenue BIGINT"
clients_schema = "client_id BIGINT, client_name STRING"

# Generate test data for shipments table
shipments_data = [
    (1, '2024-03-21T00:00:00.000+0000', 101, 1, 'Shipped', 'No', 5000),
    (2, '2024-04-15T00:00:00.000+0000', 102, 2, 'Cancelled', 'Yes', 7000),
    (3, '2024-04-20T00:00:00.000+0000', 103, 3, 'Shipped', 'No', 3000),
    (4, '2024-05-05T00:00:00.000+0000', 104, 4, 'Cancelled', 'Yes', 8000),
    (5, 'invalid-date-format', 105, 5, 'Shipped', 'No', 9000),
]

# Generate test data for clients table
clients_data = [
    (1, 'Client A'),
    (2, 'Client B'),
    (3, 'Client C'),
    (4, 'Client D'),
    (5, 'Client E')
]

# Create DataFrames based on the schema and test data
shipments_df = spark.createDataFrame(shipments_data, schema=shipments_schema)
clients_df = spark.createDataFrame(clients_data, schema=clients_schema)

# Begin data type validation
try:
    # Validate and convert data types, handling invalid data gracefully
    shipments_df = shipments_df.withColumn("shipment_date", 
                                           when(col("shipment_date").cast("TIMESTAMP").isNotNull(), col("shipment_date"))
                                           .otherwise(None))
    shipments_df = shipments_df.withColumn("cancellation_flag",
                                           when(col("cancellation_flag").isin("Yes", "No"), col("cancellation_flag"))
                                           .otherwise(None))
except Exception as e:
    print(f"Error in data type validation: {e}")

# Extract year and month based on shipment_date
shipment_analysis_df = shipments_df \
    .filter(col("client_id").isNotNull()) \
    .filter(col("shipment_date").isNotNull()) \
    .withColumn("year", year("shipment_date")) \
    .withColumn("month", month("shipment_date")) \
    .groupBy("client_id", "year", "month") \
    .agg(
        count(col("shipment_id")).alias("total_shipments"),
        sum(when(col("cancellation_flag") == "Yes", 1).otherwise(0)).alias("cancelled_shipments")
    ) \
    .withColumn("cancellation_percentage",
                round((col("cancelled_shipments") / col("total_shipments")) * 100, 2))

# Join with clients table to get client_name
shipment_analysis_df = shipment_analysis_df.join(clients_df, "client_id") \
    .select("client_name", "year", "month", "total_shipments", "cancelled_shipments", "cancellation_percentage")

# Display final DataFrame
shipment_analysis_df.show()

# Performance tests (Optional)
# Add any Spark performance testing code if necessary, such as caching data or monitoring execution times

# Cleanup operations
spark.stop()


