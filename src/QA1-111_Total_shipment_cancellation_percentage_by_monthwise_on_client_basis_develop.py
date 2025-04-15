from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month, count, sum, when, lit

# Assuming the 'spark' session is available as per instructions

# Read data from Unity Catalog tables
shipments_df = spark.table("purgo_playground.shipments")
clients_df = spark.table("purgo_playground.clients")

# Filter and process shipments data
processed_shipments_df = shipments_df.filter(col("status") == lit("completed")) \
    .filter(col("shipment_date").isNotNull() & col("client_id").isNotNull()) \
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

# Validate results (use proper test framework in a real scenario)
assert result_df.agg(sum("total_shipments")).first()[0] > 0, "Total shipments count should be greater than 0"

