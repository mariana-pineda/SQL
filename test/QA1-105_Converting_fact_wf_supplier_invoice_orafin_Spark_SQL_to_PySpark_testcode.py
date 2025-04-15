from pyspark.sql import SparkSession, functions as F
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType, LongType

# Initialize Spark session
spark = SparkSession.builder.appName("DatabricksTestCode").getOrCreate()

# Define schema for supplier_invoice DataFrame
supplier_invoice_schema = StructType([
    StructField("invc_entry_period", TimestampType(), True),
    StructField("suplr_invc_nbr", StringType(), True),
    StructField("vchr_nbr", StringType(), True),
    StructField("vchr_line_nbr", StringType(), True),
    StructField("fscl_yr_nbr", LongType(), True),
    StructField("vchr_type_cd", StringType(), True),
    StructField("vchr_status", StringType(), True),
    StructField("supplier_cd", StringType(), True),
    StructField("supplier_name", StringType(), True),
    StructField("supplier_type_cd", StringType(), True),
    StructField("suplr_invc_dt", TimestampType(), True),
    StructField("ap_payment_term_cd", StringType(), True),
    StructField("ap_payment_term_desc", StringType(), True),
    StructField("cost_centre_cd", StringType(), True),
    StructField("cost_centre_nm", StringType(), True),
    StructField("gl_acct_id", StringType(), True),
    StructField("gl_acct_nm", StringType(), True),
    StructField("inv_line_desc", StringType(), True),
    StructField("remit_to_addr_line_1", StringType(), True),
    StructField("column1", StringType(), True),
    StructField("column2", StringType(), True),
    StructField("column3", StringType(), True)
])

# Create DataFrame adhering to defined schema
data = [
    # Add sample data conforming to schema constraints
    ('2023-01-01 00:00:00', 'INV123', 'VCHR123', 'LINE123', 2023, 'TYPE1', 'STATUS1', 'SUP123', 'Supplier Name', 'Type1', '2023-01-01 00:00:00', 'TERM1', 'Term Description', 'CC123', 'Cost Centre Name', 'GL123', 'GL Name', 'Line Description', 'Address Line 1', 'Column1', 'Column2', 'Column3'),
    # Additional rows for testing edge cases and normal scenarios...
]

df = spark.createDataFrame(data, schema=supplier_invoice_schema)

# Handling missing or invalid data
try:
    # Perform operations like transformation, filtering, calculations
    transformed_df = df.withColumn('fscl_yr_nbr', F.year('suplr_invc_dt'))
    
    # Validate schema consistency
    assert len(df.columns) == len(supplier_invoice_schema.fields), "Column count mismatch"
    
    # Test data type conversions and validate NULL handling
    df = df.withColumn("invc_entry_period", F.date_format(df.invc_entry_period, "yyyyMM"))
    df = df.fillna({'suplr_invc_nbr': 'Unknown'})
except Exception as e:
    print(f"Error occurred: {e}")

# Write DataFrame to Delta lake after processing
try: 
    df.write.format("delta").mode("append").save(f"{unity_catalog}.purgo_playground.supplier_invoice")
except Exception as e:
    print(f"Error writing to Delta Lake: {e}")

# Validate Delta Lake operations
updated_df = spark.read.format("delta").load(f"{unity_catalog}.purgo_playground.supplier_invoice")
assert updated_df.count() > 0, "Delta Lake update failed"

# Clean up operation after tests
spark.sql(f"DELETE FROM purgo_playground.supplier_invoice WHERE vchr_status = 'Incomplete'")

# Stop Spark session
spark.stop()