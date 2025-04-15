from pyspark.sql.functions import col, year, month, count, sum, when

# Assuming the 'spark' session is available

# Create DataFrames for shipments and clients
shipments_df = spark.table("purgo_playground.shipments")
clients_df = spark.table("purgo_playground.clients")

# Process shipments data: filter completed shipments and valid dates
processed_shipments_df = shipments_df.filter(col("status") == "completed") \
    .filter((col("shipment_date").isNotNull()) & (col("client_id").isNotNull())) \
    .filter(~col("shipment_date").isin("None", "invalid_date"))

# Extract year and month from shipment_date
processed_shipments_df = processed_shipments_df.withColumn("year", year("shipment_date")) \
    .withColumn("month", month("shipment_date"))

# Aggregate: calculate total and cancelled shipments
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

# Test assertions
assert result_df.agg(sum("total_shipments")).first()[0] == 5, "Total shipments count does not match"
assert result_df.filter(col("client_name") == 'Client A').select("cancellation_percentage").first()[0] == 100.0, "Client A's cancellation percentage mismatch"
assert result_df.filter(col("month") == 3).count() == 1, "Month 3 data should exist and be complete"