from pyspark.sql.types import StructType, StructField, StringType, LongType, DoubleType, DecimalType, TimestampType
from pyspark.sql import SparkSession
from pyspark.sql.functions import to_timestamp
from decimal import Decimal
import datetime

spark = SparkSession.builder.appName("TestDataGeneration").getOrCreate()

schema = StructType([
    StructField("order_nbr", StringType(), True),
    StructField("order_type", LongType(), True),
    StructField("delivery_dt", DecimalType(38,0), True),
    StructField("order_qty", DoubleType(), True),
    StructField("sched_dt", DecimalType(38,0), True),
    StructField("expected_shipped_dt", DecimalType(38,0), True),
    StructField("actual_shipped_dt", DecimalType(38,0), True),
    StructField("order_line_nbr", StringType(), True),
    StructField("loc_tracker_id", StringType(), True),
    StructField("shipping_add", StringType(), True),
    StructField("primary_qty", DoubleType(), True),
    StructField("open_qty", DoubleType(), True),
    StructField("shipped_qty", DoubleType(), True),
    StructField("order_desc", StringType(), True),
    StructField("flag_return", StringType(), True),
    StructField("flag_cancel", StringType(), True),
    StructField("cancel_dt", DecimalType(38,0), True),
    StructField("cancel_qty", DoubleType(), True),
    StructField("crt_dt", TimestampType(), True),
    StructField("updt_dt", TimestampType(), True)
])

data = [
    # Happy path
    ("ORD001", 1, Decimal("20240910"), 100.0, Decimal("20240905"), Decimal("20240915"), Decimal("20240914"), "LINE001", "LOC001", "123 Main St", 50.0, 50.0, 100.0, "Standard Order", "N", "N", Decimal("0"), 0.0, datetime.datetime.strptime("2024-03-21T00:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z"), datetime.datetime.strptime("2024-03-21T00:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z")),
    
    # Edge case: Minimum values
    ("ORD002", 0, Decimal("19000101"), 0.0, Decimal("19000101"), Decimal("19000101"), Decimal("19000101"), "LINE002", "LOC002", "456 Elm St", 0.0, 0.0, 0.0, "Edge Case Order", "N", "N", Decimal("0"), 0.0, datetime.datetime.strptime("1900-01-01T00:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z"), datetime.datetime.strptime("1900-01-01T00:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z")),
    
    # Edge case: Maximum values
    ("ORD003", 999999999, Decimal("99991231"), 1e12, Decimal("99991231"), Decimal("99991231"), Decimal("99991231"), "LINE003", "LOC003", "789 Oak St", 1e12, 1e12, 1e12, "Max Value Order", "N", "N", Decimal("0"), 0.0, datetime.datetime.strptime("9999-12-31T23:59:59.999+0000", "%Y-%m-%dT%H:%M:%S.%f%z"), datetime.datetime.strptime("9999-12-31T23:59:59.999+0000", "%Y-%m-%dT%H:%M:%S.%f%z")),
    
    # Error case: delivery_dt with invalid format (non-numeric)
    ("ORD004", 2, Decimal("ABCDEFGH"), 200.0, Decimal("20240505"), Decimal("20240515"), Decimal("20240514"), "LINE004", "LOC004", "321 Pine St", 100.0, 100.0, 200.0, "Invalid Delivery Date", "Y", "N", Decimal("20240910"), 10.0, datetime.datetime.strptime("2024-03-22T00:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z"), datetime.datetime.strptime("2024-03-22T00:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z")),
    
    # Error case: delivery_dt exceeds precision
    ("ORD005", 3, Decimal("202409100000000000"), 300.0, Decimal("20240605"), Decimal("20240615"), Decimal("20240614"), "LINE005", "LOC005", "654 Maple St", 150.0, 150.0, 300.0, "Exceeds Precision", "N", "Y", Decimal("20240910"), 20.0, datetime.datetime.strptime("2024-03-23T00:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z"), datetime.datetime.strptime("2024-03-23T00:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z")),
    
    # NULL handling: delivery_dt is NULL
    ("ORD006", 4, None, 400.0, Decimal("20240705"), Decimal("20240715"), Decimal("20240714"), "LINE006", "LOC006", "987 Birch St", 200.0, 200.0, 400.0, "NULL Delivery Date", "N", "N", Decimal("20240910"), 30.0, datetime.datetime.strptime("2024-03-24T00:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z"), datetime.datetime.strptime("2024-03-24T00:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z")),
    
    # Special characters in text fields
    ("ORD007", 5, Decimal("20240810"), 500.0, Decimal("20240805"), Decimal("20240815"), Decimal("20240814"), "LINE007", "LOC007", "123 @#! St", 250.0, 250.0, 500.0, "Special !@#$%^&*() Characters", "Y", "N", Decimal("20240910"), 40.0, datetime.datetime.strptime("2024-03-25T00:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z"), datetime.datetime.strptime("2024-03-25T00:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z")),
    
    # Multi-byte characters in text fields
    ("ORD008", 6, Decimal("20240710"), 600.0, Decimal("20240705"), Decimal("20240715"), Decimal("20240714"), "LINE008", "LOC008", "地址含有多字节字符", 300.0, 300.0, 600.0, "Multi-byte 漢字 Characters", "N", "Y", Decimal("20240910"), 50.0, datetime.datetime.strptime("2024-03-26T00:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z"), datetime.datetime.strptime("2024-03-26T00:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z")),
    
    # Error case: Invalid date in delivery_dt
    ("ORD009", 7, Decimal("20241301"), 700.0, Decimal("20240905"), Decimal("20240915"), Decimal("20240914"), "LINE009", "LOC009", "654 Cedar St", 350.0, 350.0, 700.0, "Invalid Date in Delivery", "N", "N", Decimal("20240910"), 60.0, datetime.datetime.strptime("2024-03-27T00:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z"), datetime.datetime.strptime("2024-03-27T00:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z")),
    
    # Error case: Non-numeric characters in delivery_dt
    ("ORD010", 8, Decimal("2024AB10"), 800.0, Decimal("20241005"), Decimal("20241015"), Decimal("20241014"), "LINE010", "LOC010", "321 Spruce St", 400.0, 400.0, 800.0, "Non-numeric Delivery Date", "Y", "N", Decimal("20240910"), 70.0, datetime.datetime.strptime("2024-03-28T00:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z"), datetime.datetime.strptime("2024-03-28T00:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z")),
    
    # Additional Happy path
    ("ORD011", 9, Decimal("20241010"), 900.0, Decimal("20241005"), Decimal("20241015"), Decimal("20241014"), "LINE011", "LOC011", "159 Willow St", 450.0, 450.0, 900.0, "Another Standard Order", "N", "N", Decimal("0"), 0.0, datetime.datetime.strptime("2024-03-29T00:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z"), datetime.datetime.strptime("2024-03-29T00:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z")),
    
    # NULL handling in multiple fields
    (None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None),
    
    # Mix of valid and invalid records
    ("ORD012", 10, Decimal("20241110"), 1000.0, Decimal("20241105"), Decimal("20241115"), Decimal("20241114"), "LINE012", "LOC012", "753 Aspen St", 500.0, 500.0, 1000.0, "Mixed Valid Order", "Y", "Y", Decimal("20240910"), 80.0, datetime.datetime.strptime("2024-03-30T00:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z"), datetime.datetime.strptime("2024-03-30T00:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z")),
    
    # Special characters and multi-byte characters
    ("ORD013", 11, Decimal("20241210"), 1100.0, Decimal("20241205"), Decimal("20241215"), Decimal("20241214"), "LINE013", "LOC013", "地址@#￥%……&*()Chinese字符", 550.0, 550.0, 1100.0, "Special & Multi-byte", "N", "N", Decimal("20240910"), 90.0, datetime.datetime.strptime("2024-03-31T00:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z"), datetime.datetime.strptime("2024-03-31T00:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z")),
    
    # Additional Error cases
    ("ORD014", 12, Decimal("20240230"), 1200.0, Decimal("20240225"), Decimal("20240305"), Decimal("20240304"), "LINE014", "LOC014", "852 Cypress St", 600.0, 600.0, 1200.0, "Invalid Date February", "Y", "N", Decimal("20240910"), 100.0, datetime.datetime.strptime("2024-04-01T00:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z"), datetime.datetime.strptime("2024-04-01T00:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z")),
    
    ("ORD015", 13, Decimal("20240631"), 1300.0, Decimal("20240625"), Decimal("20240705"), Decimal("20240704"), "LINE015", "LOC015", "951 Walnut St", 650.0, 650.0, 1300.0, "Invalid June Date", "N", "Y", Decimal("20240910"), 110.0, datetime.datetime.strptime("2024-04-02T00:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z"), datetime.datetime.strptime("2024-04-02T00:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z")),
    
    # Valid record with special numeric edge case
    ("ORD016", 14, Decimal("20240000"), 1400.0, Decimal("20240001"), Decimal("20240031"), Decimal("20240030"), "LINE016", "LOC016", "357 Poplar St", 700.0, 700.0, 1400.0, "Special Numeric Edge", "N", "N", Decimal("0"), 0.0, datetime.datetime.strptime("2024-04-03T00:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z"), datetime.datetime.strptime("2024-04-03T00:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z")),
    
    # Valid record with zero quantities
    ("ORD017", 15, Decimal("20240110"), 0.0, Decimal("20240105"), Decimal("20240115"), Decimal("20240114"), "LINE017", "LOC017", "258 Cherry St", 0.0, 0.0, 0.0, "Zero Quantities Order", "N", "N", Decimal("0"), 0.0, datetime.datetime.strptime("2024-04-04T00:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z"), datetime.datetime.strptime("2024-04-04T00:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z")),
    
    # Valid record with maximum string lengths
    ("ORD018" + "X"*50, 16, Decimal("20240210"), 1600.0, Decimal("20240205"), Decimal("20240215"), Decimal("20240214"), "LINE018" + "Y"*50, "LOC018" + "Z"*50, "1234567890"*5, 800.0, 800.0, 1600.0, "Max Length Order Description " + "A"*100, "Y", "N", Decimal("20240910"), 120.0, datetime.datetime.strptime("2024-04-05T00:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z"), datetime.datetime.strptime("2024-04-05T00:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z")),
    
    # Valid record with varied timestamps
    ("ORD019", 17, Decimal("20240310"), 1700.0, Decimal("20240305"), Decimal("20240315"), Decimal("20240314"), "LINE019", "LOC019", "369 Pineapple St", 850.0, 850.0, 1700.0, "Varied Timestamps Order", "N", "Y", Decimal("20240910"), 130.0, datetime.datetime.strptime("2024-04-06T12:34:56.789+0000", "%Y-%m-%dT%H:%M:%S.%f%z"), datetime.datetime.strptime("2024-04-06T12:34:56.789+0000", "%Y-%m-%dT%H:%M:%S.%f%z")),
    
    # Another NULL handling
    ("ORD020", 18, None, 1800.0, Decimal("20240405"), Decimal("20240415"), Decimal("20240414"), "LINE020", "LOC020", "741 Mango St", 900.0, 900.0, 1800.0, "Another NULL Delivery Date", "Y", "N", Decimal("20240910"), 140.0, datetime.datetime.strptime("2024-04-07T00:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z"), datetime.datetime.strptime("2024-04-07T00:00:00.000+0000", "%Y-%m-%dT%H:%M:%S.%f%z"))
]

df = spark.createDataFrame(data, schema)

# Try-except block to handle any potential errors during data insertion
try:
    df.write.mode("append").saveAsTable("purgo_databricks.purgo_playground.f_order")
except Exception as e:
    print(f"Error inserting test data: {e}")