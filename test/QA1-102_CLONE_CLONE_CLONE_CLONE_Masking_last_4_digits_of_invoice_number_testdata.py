from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr, lit

# Initialize Spark session
spark = SparkSession.builder \
    .appName('MaskInvoiceData') \
    .config('spark.sql.catalogImplementation', 'hive') \
    .getOrCreate()

# Drop the clone table if it exists
spark.sql("DROP TABLE IF EXISTS purgo_playground.d_product_revenue_clone")

# Create a clone of the original table
spark.sql("""
    CREATE TABLE purgo_playground.d_product_revenue_clone AS
    SELECT * FROM purgo_playground.d_product_revenue
""")

# Load data into DataFrame
clone_df = spark.table("purgo_playground.d_product_revenue_clone")

# Define masking function
def mask_invoice_number(invoice_number):
    if invoice_number is not None:
        return str(invoice_number)[:-4] + '****'
    return None  # Handle NULL gracefully

# Apply masking to the invoice_number column
masked_clone_df = clone_df.withColumn(
    'invoice_number',
    expr("IF(invoice_number IS NOT NULL, CONCAT(CAST(invoice_number AS STRING)[0:LEN(CAST(invoice_number AS STRING))-4], '****'), NULL) AS invoice_number")
)

# Write back masked data to clone table
masked_clone_df.write.mode("overwrite").saveAsTable("purgo_playground.d_product_revenue_clone")

# Additional Test Scenarios
# Happy Path - valid invoice numbers
test_data_valid = [(1234567890,), (9876543210,), (1111222233334444,)]
valid_df = spark.createDataFrame(test_data_valid, ['invoice_number'])
valid_df.withColumn("masked_invoice_number", expr("CONCAT(CAST(invoice_number AS STRING)[0:LEN(CAST(invoice_number AS STRING))-4], '****')")).show()

# Edge Case - null and edge numbers
test_data_edge = [(None,), (0,), (-123456,), (9999999999999999,)]
edge_df = spark.createDataFrame(test_data_edge, ['invoice_number'])
edge_df.withColumn("masked_invoice_number", expr("IF(invoice_number IS NOT NULL, CONCAT(CAST(invoice_number AS STRING)[0:LEN(CAST(invoice_number AS STRING))-4], '****'), NULL)")).show()

# Error Case: negative numbers and non-integer handling
test_data_error = [(None,), (12345,), ('invalid',), (-1234567890,)]
error_df = spark.createDataFrame(test_data_error, ['invoice_number'])
error_df = error_df.withColumn("masked_invoice_number", 
                               expr("CASE WHEN CAST(invoice_number AS STRING) RLIKE '^[0-9]+$' AND invoice_number >= 0 THEN CONCAT(CAST(invoice_number AS STRING)[0:LEN(CAST(invoice_number AS STRING))-4], '****') ELSE NULL END"))
error_df.show()

