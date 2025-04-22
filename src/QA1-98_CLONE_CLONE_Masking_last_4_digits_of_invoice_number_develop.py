"""
/*
Header: 
This script clones the purgo_playground.d_product_revenue table to purgo_playground.d_product_revenue_clone
and masks the last four digits of the invoice_number column by replacing them with '****'.
The invoice_number column is converted from bigint to string to accommodate the masking.
*/
"""

from pyspark.sql import functions as F
from pyspark.sql.types import StringType

# Drop the clone table if it exists
try:
    spark.sql("""
        DROP TABLE IF EXISTS purgo_playground.d_product_revenue_clone
    """)
except Exception as e:
    # Log the exception if dropping the table fails
    # e.g., logger.error(f"Failed to drop table: {e}")
    pass

# Create a replica of the original table
try:
    spark.sql("""
        CREATE TABLE purgo_playground.d_product_revenue_clone AS
        SELECT * FROM purgo_playground.d_product_revenue
    """)
except Exception as e:
    # Log the exception if cloning the table fails
    # e.g., logger.error(f"Failed to clone table: {e}")
    raise Exception("Source table purgo_playground.d_product_revenue does not exist.")

# Function to mask the last four digits of invoice_number
def mask_invoice_number(df):
    """
    Masks the last four digits of the invoice_number column by replacing them with '****'.
    Converts the invoice_number from bigint to string.
    Raises an error if invoice_number has fewer than four digits.
    """
    try:
        # Convert invoice_number to string
        df = df.withColumn("invoice_number", F.col("invoice_number").cast(StringType()))
        
        # Check for invoice_number length
        df = df.withColumn("invoice_number", 
                           F.when(F.length(F.col("invoice_number")) >= 4,
                                  F.concat(
                                      F.substring(F.col("invoice_number"), 1, F.length(F.col("invoice_number")) - 4),
                                      F.lit("****")
                                  )
                                 ).otherwise(
                                     F.expr("null")
                                 )
                          )
        
        # Raise exception for invoice_number with fewer than four digits
        if df.filter(F.col("invoice_number").isNull()).count() > 0:
            raise ValueError("Invoice number must have at least four digits to mask.")
        
        return df
    except Exception as e:
        # Log the exception if masking fails
        # e.g., logger.error(f"Failed to mask invoice_number: {e}")
        raise e

# Read the clone table
try:
    df_clone = spark.table("purgo_playground.d_product_revenue_clone")
except Exception as e:
    # Log the exception if reading the table fails
    # e.g., logger.error(f"Failed to read clone table: {e}")
    raise e

# Apply masking to the invoice_number column
try:
    df_masked = mask_invoice_number(df_clone)
except Exception as e:
    # Log the exception if masking fails
    # e.g., logger.error(f"Masking process failed: {e}")
    raise e

# Write the masked DataFrame back to the clone table
try:
    df_masked.write.mode("overwrite").saveAsTable("purgo_playground.d_product_revenue_clone")
except Exception as e:
    # Log the exception if writing to the table fails
    # e.g., logger.error(f"Failed to write masked data: {e}")
    raise e

# Masking process completed successfully
# e.g., logger.info("Masking process completed successfully.")