from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_replace

# Load data from purgo_playground.d_product_revenue
def load_data():
    try:
        df = spark.table("purgo_playground.d_product_revenue")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

# Mask the last 4 digits of invoice_number
def mask_invoice_number(df):
    try:
        masked_df = df.withColumn("invoice_number", regexp_replace(col("invoice_number"), r"(\d{4})$", "****"))
        return masked_df
    except Exception as e:
        print(f"Error masking invoice_number: {e}")
        return None

# Create or replace the d_product_revenue_clone table
def create_clone_table(df):
    try:
        df.write.mode("overwrite").saveAsTable("purgo_playground.d_product_revenue_clone")
        print("Table d_product_revenue_clone created successfully.")
    except Exception as e:
        print(f"Error creating clone table: {e}")

# Main processing logic
def process_data():
    # Load the original data
    original_df = load_data()
    if original_df is not None:
        # Mask invoice numbers
        masked_df = mask_invoice_number(original_df)
        if masked_df is not None:
            # Write masked data into a new table
            create_clone_table(masked_df)

# Execute the data processing
process_data()

