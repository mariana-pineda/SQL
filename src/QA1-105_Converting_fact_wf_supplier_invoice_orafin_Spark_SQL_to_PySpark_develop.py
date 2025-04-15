from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, LongType, TimestampType
from pyspark.sql.functions import col, when, lit, expr, row_number, sum as spark_sum, window, concat_ws, coalesce, date_format
from pyspark.sql.window import Window

# Initialize Spark session
spark = SparkSession.builder \
    .appName("PySparkConversion") \
    .getOrCreate()

# Initialize variables from widgets
target_table_path = dbutils.widgets.get("target_table_path")
partition_key = dbutils.widgets.get("partition")
table_format = dbutils.widgets.get("table_format")
compression = dbutils.widgets.get("compression")
table_name = dbutils.widgets.get("table_name")
unity_catalog = dbutils.widgets.get("unity_catalog")
raw_unity_catalog = dbutils.widgets.get("raw_unity_catalog")
raw_unity_catalog_hist = dbutils.widgets.get("raw_unity_catalog_hist")

# Define the schema for supplier_invoice_bkp table
schema_supplier_invoice_bkp = StructType([
    # Define all schema fields here
])

# Function to read control table (Stub for conversion)
def read_control_table(project, table_name, load_type, control_table):
    # Implement reading logic
    return None

# Setup partitioning configuration
spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")

# Try-Except for securing method call
try:
    job_id = dbutils.notebook.entry_point.getDbutils().notebook().getContext().jobId().get()
except Exception as e:
    job_id = -123

# Construct job URL
base_url, jobs_api_secret = get_basejob_url(environment)
job_url = f"{base_url}/#job/{job_id}/run/1"

# Control table configuration
control_table = f"{config_unity_catalog}.{cl_control_table}"
ctrl_tbl_entry = read_control_table(project, table_name, load_type, control_table)

# Query supplier_invoice data
df_supplier_invoice = spark.sql(f"""
    SELECT cost_center_segment,gl_balancing_segment,gl_segment1,gl_code_combination_id,invoiced_on_date,invoice_id,
           invoice_type_code,transaction_currency_code,ledger_currency_code,invoice_schedule_due_date,payables_bu_id,
           natural_account_segment,invoice_accounting_date,invoice_number,supplier_party_id,supplier_site_id,
           invoice_source_code,ROW_NUMBER() OVER (PARTITION BY invoice_id ORDER BY snapshot_captured_date DESC) AS RowNum
    FROM {raw_unity_catalog}.dw_ap_sla_aging_invoice_ca
    WHERE RowNum=1
""")

# Example transformation using PySpark
df_transformed = df_supplier_invoice.withColumn("source_country", lit("NA")) \
                                    .withColumn("supplier_segment", when(col("invoice_type_code") == "CREDIT", "TYPE1").otherwise("TYPE2")) \
                                    .withColumn("updated_invc_txn_amt", expr("transaction_amount * 1.1"))

# Window function example
window_spec = Window.partitionBy("invoice_id").orderBy("snapshot_captured_date")
df_windowed = df_supplier_invoice.withColumn("window_func_result", spark_sum("transaction_amount").over(window_spec))

# Delta Lake Merge Example (error handling)
try:
    spark.sql("""
        MERGE INTO purgo_playground.supplier_invoice_bkp USING purgo_playground.supplier_invoice
        ON supplier_invoice_bkp.po_nbr = supplier_invoice.po_nbr
        WHEN MATCHED THEN UPDATE SET supplier_invoice_bkp.unit_prc = supplier_invoice.unit_prc
    """)
except Exception as e:
    assert "AnalysisException" in str(e), "Delta Lake operation failed unexpectedly"

# Show transformed DataFrame
df_transformed.show()

# Stubbing function for base job URL retrieval
def get_basejob_url(environment):
    # Replace with logic to retrieve base job URL
    return "http://baseurl.com", "secret"

# Cleanup processes
df_transformed.unpersist()

