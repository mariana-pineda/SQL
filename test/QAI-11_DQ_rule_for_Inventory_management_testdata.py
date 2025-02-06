from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, count, lit

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Data Quality Checks") \
    .getOrCreate()

# Load the drug_inventory_management table
drug_inventory_df = spark.table("agilisium_playground.purgo_playground.drug_inventory_management")

# Define data quality rules based on DQ_rules_IM sheet
# Example rules (these should be replaced with actual rules from the Excel sheet)
rules = [
    {"check_name": "Check for non-null drug_id", "condition": col("drug_id").isNotNull()},
    {"check_name": "Check for positive quantity", "condition": col("quantity") > 0},
    {"check_name": "Check for valid expiration_date format", "condition": col("expiration_date").rlike(r"^\d{4}-\d{2}-\d{2}$")},
    # Add more rules as per the DQ_rules_IM sheet
]

# Initialize an empty list to store results
results = []

# Total number of rows in the dataframe
total_rows = drug_inventory_df.count()

# Apply each rule and calculate pass percentage
for rule in rules:
    check_name = rule["check_name"]
    condition = rule["condition"]
    
    # Calculate the number of rows passing the condition
    passing_rows = drug_inventory_df.filter(condition).count()
    
    # Calculate pass percentage
    pass_percentage = (passing_rows / total_rows) * 100
    
    # Determine result
    result = "pass" if pass_percentage == 100 else "fail"
    
    # Append the result to the list
    results.append((check_name, result, pass_percentage))

# Create a DataFrame from the results
dq_results_df = spark.createDataFrame(results, ["check_name", "result", "pass_%"])

# Show the data quality results
dq_results_df.show()

# Stop the Spark session
spark.stop()


This code snippet initializes a Spark session, loads the `drug_inventory_management` table, and applies a set of data quality rules defined in the `DQ_rules_IM` sheet. It calculates the pass percentage for each rule and determines whether the result is a "pass" or "fail". The results are stored in a DataFrame and displayed. The rules in the code are placeholders and should be replaced with actual rules from the Excel sheet.