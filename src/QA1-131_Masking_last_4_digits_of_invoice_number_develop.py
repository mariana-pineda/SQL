from pyspark.sql.functions import col, expr, when, lit

# Assuming Spark session 'spark' is already available in the Databricks environment

# Try block for loading table
try:
    df = spark.table("purgo_playground.d_product_revenue_clone")
except Exception as e:
    print(f"Error loading table purgo_playground.d_product_revenue_clone: {e}")
    df = None

# Proceed if DataFrame is successfully loaded
if df:
    # Mask last 4 digits of invoice numbers that are 10 digits long
    df_masked = df.withColumn(
        "invoice_number",
        when(
            col("invoice_number").rlike(r'^\d{10}$'),
            expr("concat(substr(invoice_number, 1, 6), '****')")
        ).otherwise(col("invoice_number"))
    )

    # Handling null or empty invoice_number cases
    df_processed = df_masked.withColumn(
        "invoice_number",
        when((col("invoice_number").isNull()) | (col("invoice_number") == ""), lit(None)).otherwise(col("invoice_number"))
    )

    # Write processed DataFrame back to the replica table
    try:
        df_processed.write.format("delta").mode("overwrite").saveAsTable("purgo_playground.d_product_revenue_clone")
    except Exception as e:
        print(f"Error writing masked data to clone table: {e}")