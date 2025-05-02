from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import (
    col, 
    when, 
    lit, 
    length, 
    expr,
    udf
)
import sys

spark = SparkSession.builder.getOrCreate()

# --- Drop the target table if exists (with error handling for permissions) ---
try:
    spark.sql("""
        DROP TABLE IF EXISTS purgo_databricks.purgo_playground.d_product_revenue_clone
    """)
except Exception as e:
    if "PERMISSION" in str(e).upper():
        raise RuntimeError("Insufficient permissions to drop d_product_revenue_clone")
    else:
        raise

# --- Create replica using source table's schema (with overwrite semantics) ---
source_table = "purgo_databricks.purgo_playground.d_product_revenue"
target_table = "purgo_databricks.purgo_playground.d_product_revenue_clone"

# Get the schema from source table
source_df = spark.table(source_table)

# --- Generate Test Data ---
# Databricks native types enforced per schema, with diverse test records

test_data = [
    # Happy path: invoice_number > 4 digits
    (1001, "Aspicare", "OTC", 12345678, "USA", "cust_001", "2023-10-21", "2024-03-20", 1234234534, 0, 8, "Vitamin C supplement", "2020-08-15", "Aspirin", 220.55),
    (1002, "Zentrol", "Rx", 8572000, "IND", "cust_002", "2024-02-02", "2024-02-14", 9876543210, 1, 10, "Hypertension pills", "2018-05-01", "Centrol", 550.00),
    (1003, "Plexira", "Medical", 30510, "GBR", "cust_003", "2024-01-01", "2024-01-02", 1234567890123, 0, 9, "Implant device", "2022-04-18", "Plexira", 17235.88),
    (1004, "GammaX", "OTC", 5050, "DEU", "cust_004", "2023-10-10", "2024-01-01", 3456789, 1, 6, "Multivitamin drink", "2021-07-07", "Aspirin", 333.75),
    # Edge: invoice_number = 4 digits
    (1005, "BetaFlu", "Rx", 100000, "FRA", "cust_005", "2023-09-09", "2024-03-30", 1234, 0, 7, "Cold & flu remedy", "2018-09-09", "BetaFlu", 42.0),
    # Edge: invoice_number = 3 digits
    (1006, "Penta", "OTC", 3000, "ITA", "cust_006", "2023-01-12", "2024-03-12", 199, 1, 5, "Pain relief gel", "2020-10-05", "Penta", 5.01),
    # Edge: invoice_number = 1 digit
    (1007, "Luna", "Cosmetics", 5100, "ESP", "cust_007", "2022-12-30", "2024-03-11", 8, 0, 4, "Night cream", "2019-08-08", "GammaX", 19.8),
    (1008, "BioGen", "Rx", 15100, "MEX", "cust_008", "2023-08-30", "2024-02-01", 0, 1, 10, "DNA test kit", "2017-06-01", "Luna", 1458.08),
    # Edge: invoice_number NULL
    (1009, "TestNull", "Rx", 50, "BRA", "cust_009", "2023-02-27", "2024-03-02", None, 0, 6, "Test NULL invoice_number", "2015-06-09", "GammaX", 29.99),
    # Edge: negative invoice_number (various lengths)
    (1010, "Neg1", "OTC", 600, "USA", "cust_010", "2022-01-01", "2024-01-01", -5321, 1, 7, "Negative 4 digits", "2022-02-02", "BetaFlu", 99.23),
    (1011, "Neg2", "Rx", 7999, "DEU", "cust_011", "2023-09-09", "2024-03-01", -75, 0, 3, "Negative 2 digits", "2021-03-04", "Zentrol", 0.01),
    (1012, "Neg3", "Med", 1234, "SWE", "cust_012", "2024-01-24", "2024-03-22", -9999, 0, 1, "Negative 4 digits", "2024-01-08", "Aspirin", 3120.20),
    (1013, "Neg4", "OTC", 150, "AUS", "cust_013", "2021-12-11", "2024-02-04", -10001, 1, 8, "Negative 5 digits", "2019-12-07", "BetaFlu", 80.80),
    (1014, "Neg5", "Medical", 650, "ARG", "cust_014", "2023-08-15", "2024-01-08", -123456, 0, 7, "Negative 6 digits", "2017-11-25", "Plexira", 1142.47),
    # Edge: error on invoice_number exceeds bigint (simulate as string input)
    (1015, "ErrBig", "Rx", 420, "UAE", "cust_015", "2023-12-11", "2024-01-10", "92233720368547758070", 0, 10, "Exceeds bigint", "2016-03-08", "Aspirin", 93.20),
    # Edge: special/multibyte chars in product/customer fields
    (1016, "Ωmega", "Rx", 17800, "JPN", "cust_Ω16", "2020-12-23", "2024-03-15", 42217, 0, 5, "サプリメント", "2023-08-03", "β-Med", 1988.77),
    (1017, "Demo💊", "Utility", 2000, "KOR", "cust_\u2603", "2024-03-01", "2024-03-24", 7890, 1, 0, "Testing snowman ☃", "2024-02-24", "Demo", 7.77),
    (1018, "D'Neutra", "Rx", 1875, "FRA", "cust_018", "2022-07-19", "2024-02-29", 100005, 0, 9, "Name w/ apostrophe", "2020-04-27", "D'Neutra", 210.99),
    (1019, "Gena$$a", "Vitamins", 4700, "BRA", "cust_019", "2021-04-25", "2024-03-03", 8751, 1, 4, "Dollar$$", "2018-12-19", "Gena$$a", 100.00),
    # Edge: all NULLs for customer/product-related fields, valid invoice_number
    (1020, None, None, 100, None, None, None, None, 123456, None, None, None, None, None, None),
    # Error: invalid input types for invoice_number (None handled, string overflows marked for validation)
    (1021, "EdgeCase", "Rx", 1000, "USA", "cust_021", "2023-12-15", "2024-03-10", None, 0, 7, "NULL invoice", "2012-01-01", "Plexira", 0.0),
    # Edge: random mix length, sign, NULL
    (1022, "Abc", "Type1", 3400, "USA", "cust_022", "2018-05-05", "2024-01-30", 1, 0, 7, "Len=1", "2018-08-01", "BetaFlu", 5.0),
    (1023, "Def", "Type2", 9300, "USA", "cust_023", "2017-04-17", "2024-01-20", -1, 0, 2, "Len=1 (neg)", "2018-07-13", "Demo", 0.2),
    (1024, "--Special", "--", 77, "--", "--", "2021-06-06", "2024-01-12", 0, 0, 0, "Zero invoice", "2021-06-06", "--", 0.0),
]

schema = StructType([
    StructField("product_id", LongType(), True),
    StructField("product_name", StringType(), True),
    StructField("product_type", StringType(), True),
    StructField("revenue", LongType(), True),
    StructField("country", StringType(), True),
    StructField("customer_id", StringType(), True),
    StructField("purchased_date", StringType(), True),   # load as string, will cast to date
    StructField("invoice_date", StringType(), True),      # load as string, will cast to date
    StructField("invoice_number", StringType(), True),    # load as string for overflow test
    StructField("is_returned", LongType(), True),
    StructField("customer_satisfaction_score", LongType(), True),
    StructField("product_details", StringType(), True),
    StructField("customer_first_purchased_date", StringType(), True),
    StructField("customer_first_product", StringType(), True),
    StructField("customer_first_revenue", DoubleType(), True)
])

df_td = spark.createDataFrame(test_data, schema=schema)

# Convert dates to actual DateType
for dcol in ['purchased_date', 'invoice_date', 'customer_first_purchased_date']:
    df_td = df_td.withColumn(dcol, col(dcol).cast(DateType()))

# --- Define the masking UDF following all business rules ---
def mask_invoice_number(val):
    if val is None:
        return None
    # Handle non-numeric entries (such as overflowed string sentinel)
    if isinstance(val, str):
        try:
            # handle error test record for overflow (should raise)
            int_val = int(val)
        except Exception:
            raise ValueError("invoice_number value exceeds valid bigint range")
    else:
        int_val = val

    # Check for exceeding BIGINT at runtime (simulate overflow check)
    if isinstance(val, str):
        # already checked above
        int_val = int(val)
    if int_val is not None:
        if int_val > 9223372036854775807 or int_val < -9223372036854775808:
            raise ValueError("invoice_number value exceeds valid bigint range")
    
    # Determine sign and abs digits
    abs_val = abs(int_val)
    abs_digits = str(abs_val)
    sign = '-' if int_val < 0 else ''
    n_digits = len(abs_digits)
    if n_digits >= 4:
        masked = abs_digits[:-4] + '*'*4
    else:
        masked = '*'*n_digits
    return sign + masked if masked else None

mask_invoice_number_udf = udf(mask_invoice_number, StringType())
    
# --- Apply masking transformation ---
df_masked = (
    df_td
    .withColumn(
        "invoice_number", 
        when(col("invoice_number").isNull(), None)
        .otherwise(mask_invoice_number_udf(col("invoice_number").cast(LongType())))
    )
)

# Ensure invoice_number output is always StringType
df_masked = df_masked.withColumn("invoice_number", col("invoice_number").cast(StringType()))

# --- Write test data to clone target table (overwrite for pipeline behavior) ---
df_masked.write.format("delta").mode("overwrite").saveAsTable(target_table)

# --- CTE for validation query: show test rows and masked invoice_number ---
validation_sql = f"""
WITH masked_data AS (
    SELECT 
        product_id,
        product_name,
        product_type,
        revenue,
        country,
        customer_id,
        purchased_date,
        invoice_date,
        invoice_number,
        is_returned,
        customer_satisfaction_score,
        product_details,
        customer_first_purchased_date,
        customer_first_product,
        customer_first_revenue
    FROM {target_table}
)
SELECT * FROM masked_data
ORDER BY product_id
"""

validation_df = spark.sql(validation_sql)
validation_df.show(30, truncate=False)