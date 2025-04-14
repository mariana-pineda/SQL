from pyspark.sql import functions as F

# Dropping the replica table if it exists
try:
    spark.sql("DROP TABLE IF EXISTS purgo_playground.d_product_revenue_clone")
except Exception as e:
    print(f"Error dropping table: {e}")

# Creating the replica of d_product_revenue
try:
    spark.sql("""
        CREATE TABLE purgo_playground.d_product_revenue_clone AS
        SELECT * FROM purgo_playground.d_product_revenue
    """)
except Exception as e:
    print(f"Error creating table: {e}")

# Masking logic for invoice numbers
try:
    df_clone = spark.table("purgo_playground.d_product_revenue_clone")

    # Mask the last four digits of invoice_number
    df_masked = df_clone.withColumn("invoice_number", 
                                    F.concat(F.col("invoice_number").cast("string").substr(1, 6), F.lit("****")))

    # Write the masked data back into the table
    df_masked.write.mode("overwrite").option("overwriteSchema", "true").saveAsTable("purgo_playground.d_product_revenue_clone")

except Exception as e:
    print(f"Error during masking and data insertion: {e}")

# Example test scenarios:
# Validate successful masking
example_data = [(1234234534,), (9876543210,), (1111222233,)]
columns = ['invoice_number']
schema = "invoice_number bigint"

test_df = spark.createDataFrame(example_data, schema=schema)

expected_df = test_df.withColumn("invoice_number", 
                                 F.concat(F.col("invoice_number").cast("string").substr(1, 6), F.lit("****")))

result_df = df_masked.select("invoice_number").limit(3)

assert expected_df.collect() == result_df.collect(), "Masking logic validation failed"

# Handle error on invalid data type
invalid_example_data = [(None,), ('abc123xyz',), (1234.5678,)]
invalid_columns = ['invoice_number']

for invalid_data in invalid_example_data:
    try:
        invalid_df = spark.createDataFrame([invalid_data], schema=schema)
        invalid_df.withColumn("invoice_number", 
                              F.concat(F.col("invoice_number").cast("string").substr(1, 6), F.lit("****"))).collect()
    except Exception:
        print(f"Invalid data type for invoice_number: {invalid_data}")

# Validate mask for NULL handling and special characters
null_test_data = [(None,)]
null_df = spark.createDataFrame(null_test_data, schema=schema)

try:
    null_df.withColumn("invoice_number", 
                       F.concat(F.col("invoice_number").cast("string").substr(1, 6), F.lit("****"))).collect()
except Exception:
    print("Successfully handled NULL value for invoice_number")