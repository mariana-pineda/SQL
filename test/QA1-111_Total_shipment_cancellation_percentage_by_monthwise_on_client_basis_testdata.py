from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month, when, count, sum, round

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Test Data Generation for Shipment Analysis") \
    .getOrCreate()

# Define schemas for testing
shipments_schema = "shipment_id BIGINT, shipment_date TIMESTAMP, product_id BIGINT, client_id BIGINT, status STRING, cancellation_flag STRING, revenue BIGINT"
clients_schema = "client_id BIGINT, client_name STRING"

# Generate test data for shipments table
shipments_data = [
    # Happy path test data
    (1, '2024-03-21T00:00:00.000+0000', 101, 1, 'Shipped', 'No', 5000),
    (2, '2024-04-15T00:00:00.000+0000', 102, 2, 'Cancelled', 'Yes', 7000),
    (3, '2024-04-20T00:00:00.000+0000', 103, 3, 'Shipped', 'No', 3000),
    (4, '2024-05-05T00:00:00.000+0000', 104, 4, 'Cancelled', 'Yes', 8000),
    
    # Edge cases
    (5, '2024-04-01T00:00:00.000+0000', 105, 5, 'Shipped', 'No', 9000),
    (6, '2024-04-30T00:00:00.000+0000', 106, 6, 'Cancelled', 'Yes', 2000),
    (7, '2024-02-29T00:00:00.000+0000', 107, 7, 'Shipped', 'No', 8500),

    # Error cases
    (8, '2024-04-10T00:00:00.000+0000', 108, None, 'Cancelled', 'Yes', 9500),  # NULL client_id
    (9, 'invalid-date-format', 109, 5, 'Shipped', 'No', 10000),               # Invalid date format
    (10, '2024-06-15T00:00:00.000+0000', 110, 9, 'Shipped', 'Maybe', 6000),   # Invalid cancellation_flag

    # Special characters and multi-byte characters
    (11, '2024-03-21T00:00:00.000+0000', 111, 10, 'Shipp€d', 'Nô', 4000),     # Special characters
    (12, '2024-03-21T00:00:00.000+0000', 112, 11, '送货', '否', 7500)         # Multi-byte characters
]

# Generate test data for clients table
clients_data = [
    (1, 'Client A'),
    (2, 'Client B'),
    (3, 'Client C'),
    (4, 'Client D'),
    (5, 'Client E'),
    (6, 'Client F'),
    (7, 'Client G'),
    (8, 'Client H'),
    (9, 'Client I'),
    (10, 'Client J'),
    (11, 'Client K')
]

# Create DataFrames based on the schema and test data
shipments_df = spark.createDataFrame(shipments_data, schema=shipments_schema)
clients_df = spark.createDataFrame(clients_data, schema=clients_schema)

# Validate and convert data types, handling invalid data gracefully
try:
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

shipment_analysis_df.show()

