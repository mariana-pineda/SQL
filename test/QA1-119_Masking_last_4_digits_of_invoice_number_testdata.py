from pyspark.sql.types import StructType, StructField, StringType, LongType, DoubleType, DateType
from pyspark.sql import Row
from datetime import datetime

# Define the schema for purgo_playground.d_product_revenue_clone
schema = StructType([
    StructField("product_id", LongType(), False),
    StructField("product_name", StringType(), False),
    StructField("product_type", StringType(), False),
    StructField("revenue", LongType(), False),
    StructField("country", StringType(), False),
    StructField("customer_id", StringType(), False),
    StructField("purchased_date", DateType(), False),
    StructField("invoice_date", DateType(), False),
    StructField("invoice_number", StringType(), True),
    StructField("is_returned", LongType(), False),
    StructField("customer_satisfaction_score", LongType(), False),
    StructField("product_details", StringType(), False),
    StructField("customer_first_purchased_date", DateType(), False),
    StructField("customer_first_product", StringType(), False),
    StructField("customer_first_revenue", DoubleType(), False)
])

# Create test data covering various scenarios
data = [
    # Happy Path: Valid invoice numbers with more than four digits
    Row(1, "Product A", "Type 1", 1000, "USA", "CUST001", datetime.strptime("2024-01-10", "%Y-%m-%d").date(),
        datetime.strptime("2024-01-15", "%Y-%m-%d").date(), "1234567890", 0, 5, "Details A",
        datetime.strptime("2023-12-01", "%Y-%m-%d").date(), "Product X", 500.0),
    
    # Edge Case: Invoice number with exactly four digits
    Row(2, "Product B", "Type 2", 2000, "Canada", "CUST002", datetime.strptime("2024-02-20", "%Y-%m-%d").date(),
        datetime.strptime("2024-02-25", "%Y-%m-%d").date(), "5678", 1, 4, "Details B",
        datetime.strptime("2023-11-05", "%Y-%m-%d").date(), "Product Y", 750.0),
    
    # Error Case: Invoice number with fewer than four digits
    Row(3, "Product C", "Type 1", 1500, "UK", "CUST003", datetime.strptime("2024-03-15", "%Y-%m-%d").date(),
        datetime.strptime("2024-03-20", "%Y-%m-%d").date(), "123", 0, 3, "Details C",
        datetime.strptime("2023-10-10", "%Y-%m-%d").date(), "Product Z", 300.0),
    
    # NULL Handling: Invoice number is NULL
    Row(4, "Product D", "Type 3", 2500, "Germany", "CUST004", datetime.strptime("2024-04-05", "%Y-%m-%d").date(),
        datetime.strptime("2024-04-10", "%Y-%m-%d").date(), None, 0, 5, "Details D",
        datetime.strptime("2023-09-15", "%Y-%m-%d").date(), "Product W", 1200.0),
    
    # Special Characters: Invoice number with special characters
    Row(5, "Product E", "Type 2", 3000, "France", "CUST005", datetime.strptime("2024-05-25", "%Y-%m-%d").date(),
        datetime.strptime("2024-05-30", "%Y-%m-%d").date(), "ABCDEF1234", 1, 2, "Details E",
        datetime.strptime("2023-08-20", "%Y-%m-%d").date(), "Product V", 950.0),
    
    # Multi-byte Characters: Invoice number with multi-byte characters
    Row(6, "Product F", "Type 1", 1800, "Japan", "CUST006", datetime.strptime("2024-06-10", "%Y-%m-%d").date(),
        datetime.strptime("2024-06-15", "%Y-%m-%d").date(), "１２３４５６７８９０", 0, 4, "Details F",
        datetime.strptime("2023-07-25", "%Y-%m-%d").date(), "Product U", 640.0),
    
    # Happy Path: Another valid invoice number
    Row(7, "Product G", "Type 3", 2200, "Australia", "CUST007", datetime.strptime("2024-07-18", "%Y-%m-%d").date(),
        datetime.strptime("2024-07-23", "%Y-%m-%d").date(), "98765432101234", 1, 5, "Details G",
        datetime.strptime("2023-06-30", "%Y-%m-%d").date(), "Product T", 880.0),
    
    # Edge Case: Invoice number with leading zeros
    Row(8, "Product H", "Type 2", 1300, "India", "CUST008", datetime.strptime("2024-08-22", "%Y-%m-%d").date(),
        datetime.strptime("2024-08-27", "%Y-%m-%d").date(), "00001234", 0, 3, "Details H",
        datetime.strptime("2023-06-05", "%Y-%m-%d").date(), "Product S", 510.0),
    
    # Error Case: Non-numeric invoice number
    Row(9, "Product I", "Type 1", 1700, "Brazil", "CUST009", datetime.strptime("2024-09-14", "%Y-%m-%d").date(),
        datetime.strptime("2024-09-19", "%Y-%m-%d").date(), "INV1234ABCD", 0, 2, "Details I",
        datetime.strptime("2023-05-10", "%Y-%m-%d").date(), "Product R", 430.0),
    
    # NULL Handling: Another NULL invoice number
    Row(10, "Product J", "Type 3", 2600, "Spain", "CUST010", datetime.strptime("2024-10-30", "%Y-%m-%d").date(),
        datetime.strptime("2024-11-04", "%Y-%m-%d").date(), None, 1, 4, "Details J",
        datetime.strptime("2023-04-15", "%Y-%m-%d").date(), "Product Q", 780.0),
    
    # Special Characters: Invoice number with mix of letters and numbers
    Row(11, "Product K", "Type 2", 1900, "Italy", "CUST011", datetime.strptime("2024-11-11", "%Y-%m-%d").date(),
        datetime.strptime("2024-11-16", "%Y-%m-%d").date(), "A1B2C3D4E5", 0, 5, "Details K",
        datetime.strptime("2023-03-20", "%Y-%m-%d").date(), "Product P", 610.0),
    
    # Multi-byte Characters: Another multi-byte invoice number
    Row(12, "Product L", "Type 1", 2100, "China", "CUST012", datetime.strptime("2024-12-05", "%Y-%m-%d").date(),
        datetime.strptime("2024-12-10", "%Y-%m-%d").date(), "ａｂｃ１２３４", 1, 3, "Details L",
        datetime.strptime("2023-02-25", "%Y-%m-%d").date(), "Product O", 920.0),
    
    # Happy Path: Long invoice number
    Row(13, "Product M", "Type 3", 2400, "Mexico", "CUST013", datetime.strptime("2025-01-20", "%Y-%m-%d").date(),
        datetime.strptime("2025-01-25", "%Y-%m-%d").date(), "1234567890123456", 0, 4, "Details M",
        datetime.strptime("2023-01-30", "%Y-%m-%d").date(), "Product N", 830.0),
    
    # Edge Case: Invoice number with spaces
    Row(14, "Product N", "Type 2", 1600, "Russia", "CUST014", datetime.strptime("2025-02-28", "%Y-%m-%d").date(),
        datetime.strptime("2025-03-05", "%Y-%m-%d").date(), "1234 5678", 1, 2, "Details N",
        datetime.strptime("2022-12-05", "%Y-%m-%d").date(), "Product M", 470.0),
    
    # Error Case: Invoice number with special symbols
    Row(15, "Product O", "Type 1", 2800, "Netherlands", "CUST015", datetime.strptime("2025-03-15", "%Y-%m-%d").date(),
        datetime.strptime("2025-03-20", "%Y-%m-%d").date(), "!@#$%^&*()", 0, 1, "Details O",
        datetime.strptime("2022-11-10", "%Y-%m-%d").date(), "Product L", 350.0),
    
    # NULL Handling: Yet another NULL invoice number
    Row(16, "Product P", "Type 3", 3100, "Sweden", "CUST016", datetime.strptime("2025-04-10", "%Y-%m-%d").date(),
        datetime.strptime("2025-04-15", "%Y-%m-%d").date(), None, 0, 5, "Details P",
        datetime.strptime("2022-10-15", "%Y-%m-%d").date(), "Product K", 690.0),
    
    # Special Characters: Invoice number with hyphens
    Row(17, "Product Q", "Type 2", 2300, "Poland", "CUST017", datetime.strptime("2025-05-22", "%Y-%m-%d").date(),
        datetime.strptime("2025-05-27", "%Y-%m-%d").date(), "1234-5678-9012", 1, 3, "Details Q",
        datetime.strptime("2022-09-20", "%Y-%m-%d").date(), "Product J", 550.0),
    
    # Multi-byte Characters: Invoice number with emojis
    Row(18, "Product R", "Type 1", 1750, "South Korea", "CUST018", datetime.strptime("2025-06-18", "%Y-%m-%d").date(),
        datetime.strptime("2025-06-23", "%Y-%m-%d").date(), "1234😊5678", 0, 4, "Details R",
        datetime.strptime("2022-08-25", "%Y-%m-%d").date(), "Product I", 710.0),
    
    # Happy Path: Invoice number with mixed length
    Row(19, "Product S", "Type 3", 1950, "Singapore", "CUST019", datetime.strptime("2025-07-30", "%Y-%m-%d").date(),
        datetime.strptime("2025-08-04", "%Y-%m-%d").date(), "9876543210", 1, 5, "Details S",
        datetime.strptime("2022-07-30", "%Y-%m-%d").date(), "Product H", 680.0),
    
    # Edge Case: Invoice number with maximum expected length
    Row(20, "Product T", "Type 2", 2600, "Switzerland", "CUST020", datetime.strptime("2025-08-25", "%Y-%m-%d").date(),
        datetime.strptime("2025-08-30", "%Y-%m-%d").date(), "12345678901234567890", 0, 2, "Details T",
        datetime.strptime("2022-07-05", "%Y-%m-%d").date(), "Product G", 820.0)
]

try:
    # Create DataFrame with the defined schema and test data
    df = spark.createDataFrame(data, schema)
    
    # Write the DataFrame to purgo_playground.d_product_revenue_clone table
    df.write.mode("overwrite").saveAsTable("purgo_playground.d_product_revenue_clone")
    
except Exception as e:
    # Handle any exceptions during the data generation process
    print(f"Error during test data generation: {e}")

# spark.stop()  # Commented out as per instructions