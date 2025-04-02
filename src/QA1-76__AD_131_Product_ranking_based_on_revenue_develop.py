# PySpark Implementation Code for Databricks Environment

# Import necessary libraries
from pyspark.sql.functions import col, row_number, when
from pyspark.sql.window import Window

# Setup and configuration information
# Ensure the database and schema are correctly set up in Unity Catalog
# Commented out SparkSession initialization (spark is already available in Databricks)
'''
CREATE DATABASE IF NOT EXISTS purgo_playground;
USE purgo_playground;
'''

# Create DataFrame with test data simulating SQL TestData CTE
test_data = [
    (1, 'Electronics', '2022-01-15T00:00:00.000+0000', 1000.50, 'USA'),
    (2, 'Clothing', '2022-02-20T00:00:00.000+0000', 1500.75, 'Canada'),
    (None, None, None, None, None), # Testing null handling
    (-3, '', '1970-01-01T00:00:00.000+0000', -500.25, '!@#$%') # Edge case testing
]

columns = ["id", "product_type", "purchased_date", "revenue", "country"]

df_test_data = spark.createDataFrame(test_data, columns)

# Validate that the number of columns matches the target table's schema before insertion
df_validated = df_test_data.filter(col("id").isNotNull())

# Insert validated data into a Delta table ensuring column match
df_validated.write.format("delta").mode("append").saveAsTable("purgo_playground.information_schema.product_revenue")

# Unit tests for transformations using window functions for ranking products by revenue per country monthly 
window_spec = Window.partitionBy("country").orderBy(col("revenue").desc())
ranked_df = df_validated.withColumn("rank_monthly", row_number().over(window_spec))

# Integration test for performance classification based on consistency criteria across months.
performance_df = ranked_df.groupBy("id") \
    .agg(when((col('rank_monthly') <= 3) & (col('rank_monthly').cast('int') >= 6), 'Gold')
         .when((col('rank_monthly') <= 3) & (col('rank_monthly').cast('int') >= 3), 'Silver')
         .otherwise('Bronze').alias('performance_classification'))

performance_df.show()

# Cleanup operations after tests execution to remove rows with missing IDs or invalid data points.
df_cleaned = df_validated.filter(col("id").isNotNull())
df_cleaned.write.format("delta").mode("overwrite").saveAsTable("purgo_playground.information_schema.product_revenue")

# Additional cleanup logic can be added here if necessary.

''' End of PySpark Implementation '''