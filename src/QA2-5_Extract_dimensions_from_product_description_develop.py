from pyspark.sql.functions import col, regexp_extract, when, current_timestamp
from pyspark.sql.types import StringType
from delta.tables import DeltaTable

# Assuming input data is in Delta format and stored in 'purgo_playground.product_desc'
input_table = "purgo_playground.product_desc"

# Output table in Delta format
output_table = "purgo_playground.product_desc"

# Load the existing data from the Delta table
df = spark.read.table(input_table)

# Function to extract product size from product_description or product_id
def extract_product_size(df):
    # Define regular expression patterns for extracting product size
    pattern_desc = r"(\d+\.\d+-\d+\.\d+-\d+\.\d+)"
    pattern_id = r"(\d+\.\d+-\d+\.\d+-\d+\.\d+|\d+\.\d+)"

    # Extract product size from description or fallback to product_id
    df = df.withColumn(
        "product_size",
        when(
            col("product_description").isNotNull() & 
            (regexp_extract(col("product_description"), pattern_desc, 0) != ""),
            regexp_extract(col("product_description"), pattern_desc, 0)
        ).otherwise(
            regexp_extract(col("product_id"), pattern_id, 0)
        )
    ).withColumn("timestemp", current_timestamp())

    return df

# Apply the extraction logic
processed_df = extract_product_size(df)

# Write the processed data back to Delta, ensuring schema compatibility and history
processed_df.write.format("delta").mode("append").option("mergeSchema", "true").saveAsTable(output_table)

# Optimize the table for faster retrievals
spark.sql(f"OPTIMIZE {output_table} ZORDER BY (product_size)")

# Vacuum the table for space reduction
spark.sql(f"VACUUM {output_table} RETAIN 0 HOURS")

# Display status message
print("Product size extraction and table update complete.")

