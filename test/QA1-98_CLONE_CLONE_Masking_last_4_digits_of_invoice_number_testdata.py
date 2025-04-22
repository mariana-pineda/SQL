from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, LongType, StringType, DoubleType, DateType
from pyspark.sql.functions import col, when, regexp_replace, lpad, lit
from pyspark.sql.utils import AnalysisException

spark = SparkSession.builder.appName("MaskInvoiceNumber").getOrCreate()

# Define schema for d_product_revenue_clone
schema = StructType([
    StructField("product_id", LongType(), True),
    StructField("product_name", StringType(), True),
    StructField("product_type", StringType(), True),
    StructField("revenue", LongType(), True),
    StructField("country", StringType(), True),
    StructField("customer_id", StringType(), True),
    StructField("purchased_date", DateType(), True),
    StructField("invoice_date", DateType(), True),
    StructField("invoice_number", StringType(), True),
    StructField("is_returned", LongType(), True),
    StructField("customer_satisfaction_score", LongType(), True),
    StructField("product_details", StringType(), True),
    StructField("customer_first_purchased_date", DateType(), True),
    StructField("customer_first_product", StringType(), True),
    StructField("customer_first_revenue", DoubleType(), True)
])

# Sample test data with diverse scenarios
test_data = [
    # Happy path
    (1, "Product A", "Type 1", 1000, "USA", "C001", "2024-01-15", "2024-01-16", "123456789012", 0, 5, "Detail A", "2023-12-01", "Product A", 500.0),
    (2, "Product B", "Type 2", 2000, "Canada", "C002", "2024-02-20", "2024-02-21", "987654321098", 0, 4, "Detail B", "2023-11-05", "Product B", 1500.0),
    
    # Edge cases
    (3, "Product C", "Type 1", 1500, "UK", "C003", "2024-03-10", "2024-03-11", "1234", 1, 3, "Detail C", "2023-10-10", "Product C", 750.0),
    (4, "Product D", "Type 3", 2500, "Germany", "C004", "2024-04-25", "2024-04-26", "567890", 0, 5, "Detail D", "2023-09-15", "Product D", 2000.0),
    
    # Error cases
    (5, "Product E", "Type 2", 3000, "France", "C005", "2024-05-05", "2024-05-06", "ABCDE12345", 1, 2, "Detail E", "2023-08-20", "Product E", 2500.0),
    (6, "Product F", "Type 1", 3500, "Italy", "C006", "2024-06-18", "2024-06-19", "9999999999999999", 0, 1, "Detail F", "2023-07-25", "Product F", 3000.0),
    
    # NULL handling
    (7, "Product G", "Type 3", 4000, "Spain", "C007", None, "2024-07-21", "12345678", 0, 4, "Detail G", "2023-06-30", "Product G", 3500.0),
    (8, None, "Type 2", 4500, "Netherlands", "C008", "2024-08-30", "2024-08-31", "87654321", 1, 3, "Detail H", "2023-05-10", "Product H", 4000.0),
    
    # Special characters and multi-byte characters
    (9, "产品I", "类型1", 5000, "中国", "C009", "2024-09-15", "2024-09-16", "112233445566", 0, 5, "细节I", "2023-04-20", "产品I", 4500.0),
    (10, "Product J", "Type 4", 5500, "Japan", "C010", "2024-10-10", "2024-10-11", "998877665544", 0, 4, "Detail J", "2023-03-25", "Product J", 5000.0),
    
    # Additional diverse test cases
    (11, "Product K", "Type 1", 6000, "Australia", "C011", "2024-11-05", "2024-11-06", "1234567890", 1, 2, "Detail K", "2023-02-15", "Product K", 5500.0),
    (12, "Product L", "Type 2", 6500, "Brazil", "C012", "2024-12-20", "2024-12-21", "abcdefghij", 0, 3, "Detail L", "2023-01-10", "Product L", 6000.0),
    (13, "Product M", "Type 3", 7000, "India", "C013", "2025-01-25", "2025-01-26", "1234abcd5678", 0, 5, "Detail M", "2022-12-05", "Product M", 6500.0),
    (14, "Product N", "Type 4", 7500, "Russia", "C014", "2025-02-14", "2025-02-15", "5678901234", 1, 1, "Detail N", "2022-11-20", "Product N", 7000.0),
    (15, "Product O", "Type 1", 8000, "Mexico", "C015", "2025-03-03", "2025-03-04", "abcdefgh1234", 0, 4, "Detail O", "2022-10-30", "Product O", 7500.0),
    (16, "Product P", "Type 2", 8500, "South Korea", "C016", "2025-04-18", "2025-04-19", "12345678", 0, 2, "Detail P", "2022-09-15", "Product P", 8000.0),
    (17, "Product Q", "Type 3", 9000, "Sweden", "C017", "2025-05-22", "2025-05-23", "876543210987", 1, 3, "Detail Q", "2022-08-25", "Product Q", 8500.0),
    (18, "Product R", "Type 4", 9500, "Norway", "C018", "2025-06-30", "2025-07-01", "1122", 0, 5, "Detail R", "2022-07-10", "Product R", 9000.0),
    (19, "Product S", "Type 1", 10000, "Switzerland", "C019", "2025-07-15", "2025-07-16", "3344556677", 0, 4, "Detail S", "2022-06-20", "Product S", 9500.0),
    (20, "Product T", "Type 2", 10500, "Singapore", "C020", "2025-08-25", "2025-08-26", "9988", 1, 2, "Detail T", "2022-05-05", "Product T", 10000.0)
]

try:
    # Create DataFrame with test data
    df = spark.createDataFrame(data=test_data, schema=schema)
    
    # Mask the last 4 characters of invoice_number
    df_masked = df.withColumn(
        "invoice_number",
        when(
            col("invoice_number").isNotNull() & (length(col("invoice_number")) >= 4),
            concat(substring(col("invoice_number"), 1, length(col("invoice_number")) - 4), lit("****"))
        ).otherwise(col("invoice_number"))
    )
    
    # Drop the clone table if it exists
    try:
        spark.sql("DROP TABLE IF EXISTS purgo_databricks.purgo_playground.d_product_revenue_clone")
    except AnalysisException as e:
        print(f"Error dropping table: {e}")
    
    # Create the clone table with masked invoice_number
    df_masked.write.saveAsTable("purgo_databricks.purgo_playground.d_product_revenue_clone")
    
except Exception as e:
    print(f"An error occurred during test data generation: {e}")