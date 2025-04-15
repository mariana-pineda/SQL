from pyspark.sql import functions as F

# Load data from Unity Catalog tables
shipments_df = spark.table("purgo_playground.shipments")
clients_df = spark.table("purgo_playground.clients")

# Begin data processing
try:
    # Extract year and month from shipment_date
    shipment_analysis_df = shipments_df \
        .select("client_id", "shipment_date", "cancellation_flag") \
        .filter(F.col("shipment_date").isNotNull()) \
        .filter(F.col("client_id").isNotNull()) \
        .withColumn("year", F.year("shipment_date")) \
        .withColumn("month", F.month("shipment_date")) \
        .groupBy("client_id", "year", "month") \
        .agg(
            F.count("client_id").alias("total_shipments"),
            F.sum(F.when(F.col("cancellation_flag") == "Yes", 1).otherwise(0)).alias("cancelled_shipments")
        ) \
        .withColumn("cancellation_percentage", 
                    F.round((F.col("cancelled_shipments") / F.col("total_shipments")) * 100, 2))

    # Join with clients table to get client_name
    shipment_analysis_df = shipment_analysis_df \
        .join(clients_df, "client_id") \
        .select("client_name", "year", "month", "total_shipments", "cancelled_shipments", "cancellation_percentage")

    # Display result
    shipment_analysis_df.show()
except Exception as e:
    # Handle errors gracefully, log errors if necessary
    print(f"Error in processing: {e}")

