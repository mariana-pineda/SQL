# Import necessary PySpark libraries
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType
from pyspark.sql.functions import col, regexp_extract, when, current_timestamp
from pyspark.sql import DataFrame

# Define the PySpark schema for "product_desc" table
schema = StructType([
    StructField("product_id", StringType(), True),
    StructField("product_description", StringType(), True),
    StructField("dimension_1", DoubleType(), True),
    StructField("dimension_2", DoubleType(), True),
    StructField("dimension_3", DoubleType(), True)
])

# Assume df is the dataframe read from "purgo_playground.product_desc"
def extract_and_update_product_size(df: DataFrame) -> DataFrame:
    """
    Extracts product_size from product_description or falls back on product_id
    and adds 'timestemp' column to the DataFrame.
    
    Parameters:
    df (DataFrame): The input DataFrame with product_id and product_description.
    
    Returns:
    DataFrame: Updated DataFrame with 'product_size' and 'timestemp' columns.
    """
    # Pattern for extracting size in 'x.x-x.x-x.x' or 'x.x' formats
    size_pattern = r'(\d+\.\d+-\d+\.\d+-\d+\.\d+|\d+\.\d+)'
    
    # Extract product size using regex pattern
    df = df.withColumn(
        "product_size",
        when(
            regexp_extract(col("product_description"), size_pattern, 0) != "",
            regexp_extract(col("product_description"), size_pattern, 0)
        ).otherwise(
            regexp_extract(col("product_id"), size_pattern, 0)
        )
    )
    
    # Add current timestamp as 'timestemp'
    df = df.withColumn("timestemp", current_timestamp())
    
    return df

# Invoke the function to process the data
updated_df = extract_and_update_product_size(df)

# Write back the processed DataFrame to the Delta table
updated_df.write.format("delta").mode("overwrite").saveAsTable("purgo_playground.product_desc")

# Apply table optimization strategies:
# Optimize the table by Z-ordering on 'product_size' for better performance on queries filtering by product size
spark.sql("""
    OPTIMIZE purgo_playground.product_desc
    ZORDER BY (product_size)
""")

# Vacuum to remove old files and maintain the performance and storage efficiency
spark.sql("""
    VACUUM purgo_playground.product_desc RETAIN 168 HOURS
""")

# Ensure the Delta Lake table properties are set for data versioning and schema evolution
spark.sql("""
    ALTER TABLE purgo_playground.product_desc SET TBLPROPERTIES (
        'delta.autoOptimize.optimizeWrite' = 'true',
        'delta.autoOptimize.autoCompact' = 'true'
    )
""")

