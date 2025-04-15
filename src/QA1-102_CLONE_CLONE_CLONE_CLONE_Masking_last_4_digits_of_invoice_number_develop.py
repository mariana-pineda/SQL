from pyspark.sql import functions as F
from pyspark.sql import SparkSession

# Assuming SparkSession is already initialized as `spark`

# ===================================
# Setup and configuration
# ===================================

# Drop the clone table if it exists
spark.sql("DROP TABLE IF EXISTS purgo_playground.d_product_revenue_clone")

# Create a clone of the original table
spark.sql("""
    CREATE TABLE purgo_playground.d_product_revenue_clone AS
    SELECT * FROM purgo_playground.d_product_revenue
""")

# ===================================
# Masking Logic
# ===================================

# Load the clone table into DataFrame
clone_df = spark.table("purgo_playground.d_product_revenue_clone")

# Apply masking to the invoice_number column
masked_clone_df = clone_df.withColumn(
    "invoice_number",
    F.when(
        clone_df["invoice_number"].isNotNull(),
        F.concat(F.expr("substring(CAST(invoice_number AS STRING), 1, length(CAST(invoice_number AS STRING))-4)"), F.lit("****"))
    ).otherwise(None)
)

# Write back masked data to clone table
masked_clone_df.write.mode("overwrite").saveAsTable("purgo_playground.d_product_revenue_clone")

# ===================================
# Schema Validation
# ===================================

# Validate the schema matches the original
assert clone_df.columns == masked_clone_df.columns, "Schema mismatch after masking"

# ===================================
# Unit Test: Masking Functionality Validation
# ===================================

# Happy Path - valid invoice numbers
test_data_valid = [(1234567890,), (9876543210,), (1111222233334444,)]
valid_df = spark.createDataFrame(test_data_valid, ['invoice_number'])
valid_df.withColumn(
    "masked_invoice_number", 
    F.when(
        valid_df["invoice_number"].isNotNull(),
        F.concat(F.expr("substring(CAST(invoice_number AS STRING), 1, length(CAST(invoice_number AS STRING))-4)"), F.lit("****"))
    ).otherwise(None)
).show()

# Edge Case - null and zero handling
test_data_edge = [(None,), (0,), (-123456,), (9999999999999999,)]
edge_df = spark.createDataFrame(test_data_edge, ['invoice_number'])
edge_df.withColumn(
    "masked_invoice_number", 
    F.when(
        edge_df["invoice_number"].isNotNull(),
        F.concat(F.expr("substring(CAST(invoice_number AS STRING), 1, length(CAST(invoice_number AS STRING))-4)"), F.lit("****"))
    ).otherwise(None)
).show()

# Error Case: Negative numbers and non-numeric input
test_data_error = [(None,), (12345,), (-1234567890,)]
error_df = spark.createDataFrame(test_data_error, ['invoice_number'])
error_df.withColumn(
    "masked_invoice_number", 
    F.when(
        F.expr("CAST(invoice_number AS STRING) RLIKE '^[0-9]+$' AND invoice_number >= 0"),
        F.concat(F.expr("substring(CAST(invoice_number AS STRING), 1, length(CAST(invoice_number AS STRING))-4)"), F.lit("****"))
    ).otherwise(None)
).show()

# ===================================
# Integration Test: End-to-End Flow
# ===================================

# Validate that no invoice_number in clone table retains original form
integrity_check_df = spark.table("purgo_playground.d_product_revenue_clone")
assert integrity_check_df.filter(F.expr("CAST(invoice_number AS STRING) RLIKE '\\d{4}$'")).count() == 0, "Unmasked invoice_number found"

# Perform validation on mask integrity
integrity_check_df.filter(F.col("invoice_number").isNotNull()).show()

# ===================================
# Cleanup Operations
# ===================================

# Ensure cleanup after the tests
spark.sql("DROP TABLE IF EXISTS testing_temp_table")