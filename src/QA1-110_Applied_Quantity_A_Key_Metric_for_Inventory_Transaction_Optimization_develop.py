# PySpark Implementation of Applied Quantity Logic

# Import necessary modules
from pyspark.sql.functions import col, when, lit

# Use a try-except block for reading data
try:
    # Define schema for the inventory transaction table
    schema = """
        txn_id STRING,
        ref_txn_qty DECIMAL(3,1),
        cumulative_txn_qty DECIMAL(4,1),
        cumulative_ref_ord_sched_qty DECIMAL(4,1),
        ref_ord_sched_qty DECIMAL(3,1),
        prior_cumulative_txn_qty DECIMAL(3,1),
        prior_cumulative_ref_ord_sched_qty DECIMAL(3,1),
        apl_qty DECIMAL(5,1)
    """

    # Read inventory data into a DataFrame
    inventory_df = spark.read.format("delta").schema(schema).load("/path/to/inventory/data")

    # Calculate applied quantity (apl_qty) using when-otherwise logic
    result_df = inventory_df.withColumn(
        "apl_qty",
        when(
            (col("ref_txn_qty") > 0) &
            (col("cumulative_txn_qty") >= col("cumulative_ref_ord_sched_qty")) &
            (col("prior_cumulative_ref_ord_sched_qty") < col("prior_cumulative_txn_qty")),
            col("ref_ord_sched_qty") - (col("prior_cumulative_txn_qty") - col("prior_cumulative_ref_ord_sched_qty"))
        ).when(
            (col("ref_txn_qty") > 0) &
            (col("cumulative_txn_qty") >= col("cumulative_ref_ord_sched_qty")),
            col("ref_ord_sched_qty")
        ).when(
            (col("ref_txn_qty") > 0) &
            (col("cumulative_ref_ord_sched_qty") >= col("cumulative_txn_qty")) &
            (col("prior_cumulative_ref_ord_sched_qty") > col("prior_cumulative_txn_qty")),
            col("ref_txn_qty") - (col("prior_cumulative_ref_ord_sched_qty") - col("prior_cumulative_txn_qty"))
        ).when(
            (col("ref_txn_qty") > 0) &
            (col("cumulative_ref_ord_sched_qty") >= col("cumulative_txn_qty")),
            col("ref_txn_qty")
        ).when(
            (col("ref_txn_qty") < 0) &
            (col("cumulative_txn_qty") != 0) &
            (col("cumulative_ref_ord_sched_qty") > 0),
            col("ref_txn_qty")
        ).otherwise(lit(None))
    )

    # Display or store the result DataFrame as needed
    result_df.show()

except Exception as e:
    # Log or handle errors appropriately
    print(f"An error occurred: {e}")

# Ensure data consistency and fit by validating number of columns
assert len(result_df.columns) == len(inventory_df.columns), "Column count mismatch!"

# End of the PySpark script

