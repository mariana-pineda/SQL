# /*
# Implementation for masking the last four digits of invoice_number in purgo_playground.d_product_revenue_clone
# This script drops the clone table if it exists, creates a replica of the original table, masks the invoice_number,
# and updates the clone table with masked values. Proper error handling and logging are implemented.
# */

from pyspark.sql.functions import col, when, regexp_replace, length
from pyspark.sql.types import StringType
import logging

# Set up logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# /* 
# Drop the clone table if it exists
# */
try:
    spark.sql("DROP TABLE IF EXISTS purgo_playground.d_product_revenue_clone")
except Exception as e:
    logger.error(f"Failed to drop table purgo_playground.d_product_revenue_clone: {e}")

# /* 
# Create a replica of the original table
# */
try:
    spark.sql("""
        CREATE TABLE purgo_playground.d_product_revenue_clone AS
        SELECT * FROM purgo_playground.d_product_revenue
    """)
except Exception as e:
    logger.error(f"Failed to create clone table purgo_playground.d_product_revenue_clone: {e}")

# /* 
# Define masking function for invoice_number
# */
def mask_invoice_number(df):
    try:
        # Convert invoice_number to string
        df = df.withColumn("invoice_number", col("invoice_number").cast(StringType()))
        
        # Apply masking logic
        df = df.withColumn(
            "invoice_number",
            when(col("invoice_number").isNull(), 
                 logger.error("Invoice number cannot be null")).otherwise(col("invoice_number"))
        )
        df = df.withColumn(
            "invoice_number",
            when(length(col("invoice_number")) < 4, 
                 logger.error("Invoice number must have at least 4 digits to mask")).otherwise(col("invoice_number"))
        )
        df = df.withColumn(
            "invoice_number",
            when(~col("invoice_number").rlike("^[0-9]+$"), 
                 logger.error("Invoice number must be numeric")).otherwise(col("invoice_number"))
        )
        df = df.withColumn(
            "invoice_number",
            when(
                (col("invoice_number").isNotNull()) & 
                (length(col("invoice_number")) >= 4) & 
                (col("invoice_number").rlike("^[0-9]+$")),
                regexp_replace(col("invoice_number"), r"\d{4}$", "****")
            ).otherwise(col("invoice_number"))
        )
        return df
    except Exception as e:
        logger.error(f"Error during masking invoice_number: {e}")
        return df

# /* 
# Read the clone table
# */
try:
    df_clone = spark.table("purgo_playground.d_product_revenue_clone")
except Exception as e:
    logger.error(f"Failed to read purgo_playground.d_product_revenue_clone: {e}")
    df_clone = None

if df_clone:
    # /* 
    # Apply masking to the invoice_number column
    # */
    df_masked = mask_invoice_number(df_clone)
    
    # /* 
    # Validate the number of columns matches the target schema
    # */
    original_count = len(df_clone.columns)
    masked_count = len(df_masked.columns)
    if original_count != masked_count:
        logger.error("Column count mismatch after masking invoice_number")
    else:
        # /* 
        # Validate data type of invoice_number is string
        # */
        if dict(df_masked.dtypes).get("invoice_number") != "string":
            logger.error("Data type of invoice_number is not string after masking")
        else:
            # /* 
            # Update the clone table with masked invoice_number
            # */
            try:
                df_masked.write.mode("overwrite").saveAsTable("purgo_playground.d_product_revenue_clone")
            except Exception as e:
                logger.error(f"Failed to write masked data to purgo_playground.d_product_revenue_clone: {e}")