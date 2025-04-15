from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_replace

# Mask the last 4 digits of the invoice_number
def mask_invoice_number(df):
    try:
        # Use regexp_replace to replace last 4 digits with '****'
        return df.withColumn("invoice_number", regexp_replace(col("invoice_number"), r"(\d{4})$", "****"))
    except Exception as e:
        # Log if an exception occurs during masking
        print(f"Error while masking invoice_number: {e}")
        return None

# Drop the table if it exists
def drop_table_if_exists(table_name):
    try:
        # Drop table using SQL command
        spark.sql(f"DROP TABLE IF EXISTS {table_name}")
    except Exception as e:
        # Log if an exception occurs during table drop
        print(f"Error while dropping table {table_name}: {e}")

# Create clone table and perform masking
def clone_and_mask_table(src_table, clone_table):
    # Drop clone table if it exists
    drop_table_if_exists(clone_table)
    
    try:
        # Load data from the source table
        df = spark.table(src_table)
    except Exception as e:
        print(f"Error loading source data from {src_table}: {e}")
        return
    
    # Apply masking to the DataFrame
    masked_df = mask_invoice_number(df)
    if masked_df is not None:
        try:
            # Save the masked DataFrame as the clone table
            masked_df.write.mode("overwrite").saveAsTable(clone_table)
            print(f"Clone table {clone_table} created successfully with masked data.")
        except Exception as e:
            print(f"Error creating clone table {clone_table}: {e}")

# Main execution function
def main():
    # Define source and clone tables
    src_table = "purgo_playground.d_product_revenue"
    clone_table = "purgo_playground.d_product_revenue_clone"
    
    # Clone and mask data
    clone_and_mask_table(src_table, clone_table)

# Execute the main processing function
main()