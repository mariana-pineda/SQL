from pyspark.sql import SparkSession
from pyspark.sql.functions import expr, col

# Assume 'spark' session is already initialized in Databricks environment

# Drop the clone table if it already exists
spark.sql("DROP TABLE IF EXISTS purgo_playground.d_product_revenue_clone")

# Create a replica of the original table
spark.sql("CREATE TABLE purgo_playground.d_product_revenue_clone AS SELECT * FROM purgo_playground.d_product_revenue")

# Read the cloned table into a DataFrame
df_clone = spark.table("purgo_playground.d_product_revenue_clone")

# Apply masking to the invoice_number column
masked_df = df_clone.withColumn("invoice_number", expr("concat(substring(invoice_number, 1, length(invoice_number)-4), '****')"))

# Validate the invoice number format to ensure there are no invalid entries
def validate_invoice_number_format(df):
    return df.withColumn('valid_format', expr("length(invoice_number) = 10"))

masked_df = validate_invoice_number_format(masked_df)

# Separate valid and invalid records
valid_invoice_df = masked_df.filter(col('valid_format') == True).drop('valid_format')
invalid_invoice_df = masked_df.filter(col('valid_format') == False)

# Show any invalid records (expected to be zero)
invalid_invoice_df.select("invoice_number").show(truncate=False)

# Overwrite the cloned table with valid masked data
valid_invoice_df.write.mode("overwrite").saveAsTable("purgo_playground.d_product_revenue_clone")

# Display valid masked records to verify the process
valid_invoice_df.show(truncate=False)

# Assertions to ensure all operations were successful and data integrity is maintained
assert invalid_invoice_df.count() == 0, "Error: There are invoice numbers with invalid format"
assert valid_invoice_df.filter(col("invoice_number").endsWith("****")).count() == valid_invoice_df.count(), "Error: Not all invoice numbers were masked correctly"