from pyspark.sql import functions as F

# Drop the d_product_revenue_clone table if it exists
try:
    spark.sql("DROP TABLE IF EXISTS purgo_playground.d_product_revenue_clone")
except Exception as e:
    print(f"Error dropping table: {e}")

# Create a replica of the d_product_revenue table
try:
    spark.sql("""
        CREATE TABLE purgo_playground.d_product_revenue_clone AS
        SELECT * FROM purgo_playground.d_product_revenue
    """)
except Exception as e:
    print(f"Error creating table: {e}")

# Load the d_product_revenue_clone table into a DataFrame
try:
    df_clone = spark.table("purgo_playground.d_product_revenue_clone")

    # Apply masking operation on the last four digits of invoice_number
    df_masked = df_clone.withColumn("invoice_number", 
                                    F.concat(F.col("invoice_number").cast("string").substr(1, 6), F.lit("****")))

    # Write the masked DataFrame back to the table
    df_masked.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable("purgo_playground.d_product_revenue_clone")
except Exception as e:
    print(f"Error during masking and data insertion: {e}")

# Unit test for data masking logic
example_data = [(1234234534,), (9876543210,), (1111222233,)]
columns = ['invoice_number']
schema = "invoice_number bigint"

# Create a DataFrame for test data
test_df = spark.createDataFrame(example_data, schema=schema)

# Expected DataFrame after masking
expected_df = test_df.withColumn("invoice_number", 
                                 F.concat(F.col("invoice_number").cast("string").substr(1, 6), F.lit("****")))

# Filter and select masked invoice numbers from the result DataFrame
result_df = df_masked.select("invoice_number").filter(F.col("invoice_number").isNotNull()).limit(3)

# Assertion for correct mask
assert expected_df.collect() == result_df.collect(), "Masking logic validation failed"

# Test scenarios for invalid data types
invalid_example_data = [(None,), ('abc123xyz',), (1234.5678,)]
invalid_columns = ['invoice_number']

# Loop through invalid data examples, expect errors on invalid data
for invalid_data in invalid_example_data:
    try:
        # Attempt to apply masking logic on invalid data
        invalid_df = spark.createDataFrame([invalid_data], schema=schema)
        invalid_df.withColumn("invoice_number", 
                              F.concat(F.col("invoice_number").cast("string").substr(1, 6), F.lit("****"))).collect()
    except Exception:
        print(f"Successfully handled invalid data type for invoice_number: {invalid_data}")

# Test for handling NULL values in invoice_number
null_test_data = [(None,)]
null_df = spark.createDataFrame(null_test_data, schema=schema)

try:
    # Attempt to apply masking logic on NULL value
    null_df.withColumn("invoice_number", 
                       F.concat(F.col("invoice_number").cast("string").substr(1, 6), F.lit("****"))).collect()
except Exception:
    print("Successfully handled NULL value for invoice_number")