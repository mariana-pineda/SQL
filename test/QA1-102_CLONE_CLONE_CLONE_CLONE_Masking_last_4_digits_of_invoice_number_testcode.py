from pyspark.sql import SparkSession
from pyspark.sql.functions import expr

# Initialize Spark session
spark = SparkSession.builder \
    .appName('MaskInvoiceData') \
    .config('spark.sql.catalogImplementation', 'hive') \
    .getOrCreate()

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
    'invoice_number',
    expr("IF(invoice_number IS NOT NULL, CONCAT(CAST(invoice_number AS STRING)[0:LEN(CAST(invoice_number AS STRING))-4], '****'), NULL) AS invoice_number")
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
    expr("CONCAT(CAST(invoice_number AS STRING)[0:LEN(CAST(invoice_number AS STRING))-4], '****')")
).show()

# Edge Case - null and zero handling
test_data_edge = [(None,), (0,), (-123456,), (9999999999999999,)]
edge_df = spark.createDataFrame(test_data_edge, ['invoice_number'])
edge_df.withColumn(
    "masked_invoice_number", 
    expr("IF(invoice_number IS NOT NULL, CONCAT(CAST(invoice_number AS STRING)[0:LEN(CAST(invoice_number AS STRING))-4], '****'), NULL)")
).show()

# Error Case: Negative numbers and non-numeric input
test_data_error = [(None,), (12345,), ('invalid',), (-1234567890,)]
error_df = spark.createDataFrame(test_data_error, ['invoice_number'])
error_df.withColumn(
    "masked_invoice_number", 
    expr("CASE WHEN CAST(invoice_number AS STRING) RLIKE '^[0-9]+$' AND invoice_number >= 0 THEN CONCAT(CAST(invoice_number AS STRING)[0:LEN(CAST(invoice_number AS STRING))-4], '****') ELSE NULL END")
).show()

# ===================================
# Integration Test: End-to-End Flow
# ===================================

# Validate that no invoice_number in clone table retains original form
integrity_check_df = spark.table("purgo_playground.d_product_revenue_clone")
assert integrity_check_df.filter(expr("invoice_number RLIKE '^.*\\d{4}$'")).count() == 0, "Unmasked invoice_number found"

# Perform validation on mask integrity
integrity_check_df.filter(expr("invoice_number IS NOT NULL")).show()

# ===================================
# Cleanup Operations
# ===================================

# Ensure cleanup after the tests
spark.sql("DROP TABLE IF EXISTS testing_temp_table")