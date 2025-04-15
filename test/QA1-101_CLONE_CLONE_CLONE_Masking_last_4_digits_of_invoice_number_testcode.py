from pyspark.sql.functions import col, regexp_replace

# Load data from the source table in Unity Catalog
def load_data():
    try:
        # Load data from the d_product_revenue table in purgo_playground catalog
        df = spark.table("purgo_playground.d_product_revenue")
        return df
    except Exception as e:
        # Log an error message if data loading fails
        print(f"Error loading data: {e}")
        return None

# Mask the last 4 digits of the invoice_number column
def mask_invoice_number(df):
    try:
        # Use regexp_replace to replace the last 4 digits with '****'
        masked_df = df.withColumn("invoice_number", regexp_replace(col("invoice_number"), r"(\d{4})$", "****"))
        return masked_df
    except Exception as e:
        # Log an error message if masking fails
        print(f"Error masking invoice_number: {e}")
        return None

# Create or replace the clone table with masked data
def create_clone_table(df):
    try:
        # Save the masked DataFrame as a new table named d_product_revenue_clone
        df.write.mode("overwrite").saveAsTable("purgo_playground.d_product_revenue_clone")
        print("Table d_product_revenue_clone created successfully.")
    except Exception as e:
        # Log an error message if table creation fails
        print(f"Error creating clone table: {e}")

# Main processing logic
def process_data():
    # Load the original data from the source table
    original_df = load_data()
    if original_df is not None:
        # Apply masking transformation
        masked_df = mask_invoice_number(original_df)
        if masked_df is not None:
            # Create or replace the target clone table with masked data
            create_clone_table(masked_df)

# Execute the data processing
process_data()