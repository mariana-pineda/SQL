# ------------------------------------------------------------------------------------------------
# PySpark Implementation: Masking Last 4 Digits of invoice_number in d_product_revenue_clone
# ------------------------------------------------------------------------------------------------
# - Drops and recreates purgo_databricks.purgo_playground.d_product_revenue_clone table
# - Clones schema from purgo_databricks.purgo_playground.d_product_revenue
# - Applies strict masking logic to invoice_number (per gherkin rules)
# - Overwrites invoice_number with masked string value in clone table
# - Only modifies the clone table; does not touch other tables
# - Includes error handling for permissions and data type overflows
# ------------------------------------------------------------------------------------------------

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, udf
from pyspark.sql.types import StringType, LongType

# ------------------------------------------------------------------------------------------------
# -- Config: Unity Catalog and Table References
# ------------------------------------------------------------------------------------------------
CATALOG = "purgo_databricks"
SCHEMA = "purgo_playground"
SOURCE_TABLE = f"{CATALOG}.{SCHEMA}.d_product_revenue"
CLONE_TABLE = f"{CATALOG}.{SCHEMA}.d_product_revenue_clone"

# ------------------------------------------------------------------------------------------------
# -- Step 1: Drop the clone table if it exists, handling permissions errors
# ------------------------------------------------------------------------------------------------
try:
    spark.sql(f"DROP TABLE IF EXISTS {CLONE_TABLE}")
except Exception as drop_exc:
    if "PERMISSION" in str(drop_exc).upper():
        raise RuntimeError("Insufficient permissions to drop d_product_revenue_clone")
    else:
        raise

# ------------------------------------------------------------------------------------------------
# -- Step 2: Replicate the source table's schema to create the clone table (empty)
# ------------------------------------------------------------------------------------------------
source_df = spark.table(SOURCE_TABLE)
clone_schema = source_df.schema
empty_clone_df = spark.createDataFrame([], schema=clone_schema)
empty_clone_df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(CLONE_TABLE)

# ------------------------------------------------------------------------------------------------
# -- Step 3: Define masking logic for invoice_number, fully covering documented edge cases
# ------------------------------------------------------------------------------------------------
def mask_invoice_number(val):
    """
    Masks invoice_number as a string according to business & compliance requirements:
    - If null, returns null.
    - For >=4 digits (ignoring sign), replace last 4 digits with '*' (retain prefix/sign).
    - For <4 digits (ignoring sign), replace all digits with '*' (one per digit, retain sign if negative).
    - Always return as string, sign retained if negative.
    - Raises error if value is outside bigint range.
    """
    if val is None:
        return None
    try:
        int_val = int(val)
    except Exception:
        raise ValueError("invoice_number value exceeds valid bigint range")
    if int_val > 9223372036854775807 or int_val < -9223372036854775808:
        raise ValueError("invoice_number value exceeds valid bigint range")
    abs_val = abs(int_val)
    n_digits = len(str(abs_val))
    sign = "-" if int_val < 0 else ""
    if n_digits >= 4:
        prefix = str(abs_val)[:-4]
        masked = prefix + ("*" * 4)
    else:
        masked = "*" * n_digits
    return sign + masked

mask_invoice_number_udf = udf(mask_invoice_number, StringType())

# ------------------------------------------------------------------------------------------------
# -- Step 4: Read from source, apply masking, and write to clone table with full overwrite
# ------------------------------------------------------------------------------------------------
# -- All columns except invoice_number are preserved unmodified.
masked_df = (
    source_df
    .withColumn(
        "invoice_number",
        when(col("invoice_number").isNull(), None)
        .otherwise(mask_invoice_number_udf(col("invoice_number").cast(LongType())))
        .cast(StringType())
    )
)

# -- Ensure masked_df schema aligns to the clone table, prevent column count/type drift
assert masked_df.columns == [f.name for f in clone_schema], "Column mismatch after masking transformation"

masked_df.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable(CLONE_TABLE)

# ------------------------------------------------------------------------------------------------
# -- END: d_product_revenue_clone is fully masked & ready for downstream use
# ------------------------------------------------------------------------------------------------