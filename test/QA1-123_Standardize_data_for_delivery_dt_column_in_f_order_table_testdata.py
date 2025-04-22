from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, LongType, DecimalType, StringType, TimestampType
from pyspark.sql import functions as F

# Initialize Spark session
spark = SparkSession.builder.appName("TestDataGeneration").getOrCreate()

# Define the schema with Databricks native data types
schema = StructType([
    StructField("order_id", LongType(), False),
    StructField("customer_id", LongType(), False),
    StructField("delivery_dt", DecimalType(38,0), True),
    StructField("order_amount", DecimalType(10,2), False),
    StructField("order_status", StringType(), False),
    StructField("order_date", TimestampType(), False)
])

# Create test data covering various scenarios
data = [
    # Happy Path Test Data (Valid Scenarios)
    (1, 1001, 20240321, 250.75, "Shipped", "2024-03-20T10:00:00.000+0000"),
    (2, 1002, 20240430, 150.00, "Delivered", "2024-04-29T11:30:00.000+0000"),
    (3, 1003, 20240515, 300.50, "Processing", "2024-05-14T09:15:00.000+0000"),
    (4, 1004, 20240601, 500.00, "Shipped", "2024-05-31T14:45:00.000+0000"),
    (5, 1005, 20240704, 400.00, "Delivered", "2024-07-03T08:20:00.000+0000"),
    
    # Edge Cases (Boundary Conditions)
    (6, 1006, 99991231, 1000.00, "Delivered", "9999-12-30T12:00:00.000+0000"),  # Maximum valid date
    (7, 1007, 00010101, 50.00, "Processing", "0001-01-01T00:00:00.000+0000"),    # Minimum valid date
    (8, 1008, 20240229, 200.00, "Delivered", "2024-02-28T16:30:00.000+0000"),  # Leap day
    (9, 1009, 20241130, 175.25, "Shipped", "2024-11-29T13:15:00.000+0000"),   # End of month
    (10, 1010, 20240930, 225.50, "Delivered", "2024-09-29T10:45:00.000+0000"),# End of September
    
    # Error Cases (Invalid Inputs)
    (11, 1011, None, 300.00, "Cancelled", "2024-03-15T09:15:00.000+0000"),     # NULL delivery_dt
    (12, 1012, -20240910, 500.00, "Shipped", "2024-04-10T14:45:00.000+0000"),# Negative delivery_dt
    (13, 1013, 20240931, 400.00, "Shipped", "2024-09-30T08:20:00.000+0000"), # Invalid date
    (14, 1014, 20240000, 350.00, "Processing", "2024-03-20T11:00:00.000+0000"),# Invalid date
    (15, 1015, 20241301, 275.00, "Delivered", "2024-12-31T07:30:00.000+0000"),# Invalid month
    (16, 1016, 2024091, 125.00, "Shipped", "2024-09-01T05:45:00.000+0000"),   # Incorrect format
    (17, 1017, 2024091001, 225.00, "Delivered", "2024-09-10T19:20:00.000+0000"),# Extra digits
    (18, 1018, 202409A0, 175.00, "Processing", "2024-09-10T22:10:00.000+0000"),# Non-numeric characters
    
    # NULL Handling Scenarios
    (19, 1019, None, 600.00, "Cancelled", "2024-06-15T12:30:00.000+0000"),
    (20, 1020, None, 800.00, "Shipped", "2024-07-20T14:50:00.000+0000"),
    
    # Special Characters and Multi-byte Characters
    (21, 1021, 20241010, 100.00, "Delivered 🚚", "2024-10-05T12:00:00.000+0000"),  # Emoji in status
    (22, 1022, 20241111, 150.00, "Procèsing", "2024-11-10T16:30:00.000+0000"),  # Accent character
    (23, 1023, 20241212, 200.00, "Shipped™", "2024-12-11T09:15:00.000+0000"),   # Trademark symbol
    (24, 1024, 20241313, 250.00, "Delivered\nOn Time", "2024-13-12T18:45:00.000+0000"),# Newline character and invalid month
    (25, 1025, 20241414, 300.00, "Processing\tPending", "2024-14-13T07:20:00.000+0000"),# Tab character and invalid month
    
    # Additional Valid and Invalid Entries
    (26, 1026, 20240715, 350.00, "Delivered", "2024-07-14T10:10:00.000+0000"),
    (27, 1027, 20240820, 400.00, "Shipped", "2024-08-19T11:25:00.000+0000"),
    (28, 1028, 20240925, 450.00, "Processing", "2024-09-24T13:35:00.000+0000"),
    (29, 1029, 20241030, 500.00, "Delivered", "2024-10-29T15:45:00.000+0000"),
    (30, 1030, 20241105, 550.00, "Cancelled", "2024-11-04T17:55:00.000+0000")
]

# Function to safely parse timestamp strings
def parse_timestamp(timestamp_str):
    try:
        return F.to_timestamp(F.lit(timestamp_str), "yyyy-MM-dd'T'HH:mm:ss.SSSZ")
    except:
        return None

# Create DataFrame with the defined schema
df = spark.createDataFrame(data, schema)

# Convert order_date strings to TimestampType
df = df.withColumn("order_date", F.to_timestamp("order_date", "yyyy-MM-dd'T'HH:mm:ss.SSSZ"))

# Handle special characters and multi-byte characters if necessary
df = df.withColumn("order_status", F.regexp_replace("order_status", "\\\\n", "\n")) \
       .withColumn("order_status", F.regexp_replace("order_status", "\\\\t", "\t"))

# Write the test data to the target table in Unity Catalog
try:
    df.write.format("delta").mode("overwrite").saveAsTable("purgo_databricks.purgo_playground.f_order_test")
except Exception as e:
    print(f"Error writing test data: {e}")