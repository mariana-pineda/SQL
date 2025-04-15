from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, BigIntType, TimestampType, DateType, BooleanType

# Initialize Spark session
spark = SparkSession.builder.appName("GenerateTestData").getOrCreate()

# Define schema for "supplier_invoice"
supplier_invoice_schema = StructType([
    StructField("src_sys_cd", StringType(), True),
    StructField("po_nbr", StringType(), True),
    StructField("po_line_nbr", StringType(), True),
    StructField("invc_co_amt", DoubleType(), True),
    StructField("invc_txn_amt", DoubleType(), True),
    StructField("invc_txn_type", StringType(), True),
    StructField("document_type", StringType(), True),
    StructField("document_desc", StringType(), True),
    StructField("invc_entry_period", BigIntType(), True),
    StructField("vchr_nbr", BigIntType(), True),
    StructField("fscl_yr_nbr", BigIntType(), True),
    StructField("vchr_type_cd", StringType(), True),
    StructField("po_curncy_cd", StringType(), True),
    StructField("post_yr_mth_nbr", BigIntType(), True),
    StructField("invc_entry_dt", BigIntType(), True),
    StructField("paymt_due_dt", BigIntType(), True),
    StructField("txn_curncy_mth_rt", BigIntType(), True),
    StructField("inv_line_desc", StringType(), True),
    StructField("spend_type_cd", StringType(), True),
    StructField("supplier_cd", StringType(), True),
    StructField("suplr_invc_dt", BigIntType(), True),
    StructField("txn_orig_id", StringType(), True),
    StructField("suplr_invc_nbr", StringType(), True),
    StructField("remit_to_rgn_cd", StringType(), True),
    StructField("remit_to_rgn_nm", StringType(), True),
    StructField("suplr_paymt_terms_desc", StringType(), True),
    StructField("ap_payment_term_desc", StringType(), True),
    StructField("remit_to_cntry_nm", StringType(), True),
    StructField("supplier_type_cd", StringType(), True),
    StructField("suplr_paymt_terms_cd", StringType(), True),
    StructField("ap_payment_term_cd", StringType(), True),
    StructField("remit_to_addr_line_2", StringType(), True),
    StructField("remit_to_addr_line_3", StringType(), True),
    StructField("remit_to_addr_line_4", StringType(), True),
    StructField("remit_to_cntry_cd", StringType(), True),
    StructField("po_paymt_terms_cd", StringType(), True),
    StructField("po_paymt_terms_desc", StringType(), True),
    StructField("gl_acct_id", StringType(), True),
    StructField("cost_centre_cd", BigIntType(), True),
    StructField("co_cd", BigIntType(), True),
    StructField("co_curncy_cd", StringType(), True),
    StructField("pass_through_field", StringType(), True),
    StructField("pass_through_line", StringType(), True),
    StructField("item_nbr", StringType(), True),
    StructField("item_desc", StringType(), True),
    StructField("uom_conv_factor", StringType(), True),
    StructField("invc_uom_cd", StringType(), True),
    StructField("vendor_mat_no", StringType(), True),
    StructField("unit_prc", DoubleType(), True),
    StructField("invc_qty", BigIntType(), True),
    StructField("base_qty", StringType(), True),
    StructField("suplr_nm_src", StringType(), True),
    StructField("remit_to_st_cd", StringType(), True),
    StructField("part_rev_no", StringType(), True),
    StructField("contract_flag", StringType(), True),
    StructField("contract_type", StringType(), True),
    StructField("profit_cntr", StringType(), True),
    StructField("co_curncy_mth_rt", BigIntType(), True),
    StructField("invc_txn_pmar_amt", BigIntType(), True),
    StructField("invc_co_pmar_amt", BigIntType(), True),
    StructField("unit_prc_pmar_amt", StringType(), True),
    StructField("aprval_dt", StringType(), True),
    StructField("vomi_flag", StringType(), True),
    StructField("payment_compliance_flg", StringType(), True),
    StructField("vchr_line_nbr", BigIntType(), True),
    StructField("vchr_status", StringType(), True),
    StructField("thermo_item_nbr", StringType(), True),
    StructField("lcr_flag", StringType(), True),
    StructField("lcr_region", StringType(), True),
    StructField("invc_apprv_id", StringType(), True),
    StructField("reporting_site", StringType(), True),
    StructField("warehouse", StringType(), True),
    StructField("warehouse_nm", StringType(), True),
    StructField("unit", StringType(), True),
    StructField("nature", StringType(), True),
    StructField("inv_flg", StringType(), True),
    StructField("contract_start_date", StringType(), True),
    StructField("contract_end_date", StringType(), True),
    StructField("fk_orig", StringType(), True),
    StructField("floor_stock_cd", StringType(), True),
    StructField("sec_supp_cd", StringType(), True),
    StructField("rpt_flex1", StringType(), True),
    StructField("supplier_segment", StringType(), True),
    StructField("inv_flg_text", StringType(), True),
    StructField("invc_txn_amt_clsfctn", StringType(), True),
    StructField("source_country", StringType(), True),
    StructField("business_unit", StringType(), True),
    StructField("div_cd", StringType(), True)
])

# Generate 20-30 diverse test records
test_data = [
    ("usorafin", "PO123", "POLN1", 1500.05, 1500.05, "Invoice", "Type A", "Purchase order 123", 202403, 12345, 2024, "Type B", "USD", 202403, 20240321, 20240322, 1, "Line Description", "Indirect", "SUP123", 20240318, "TXN123", "INV123", None, "Region Name", "30 days", "Net 30", "Country Name", None, "30", None, None, None, "GL123", 123, 400, None, None, None, None, None, None, None, None, None, None, 0.0, 1, None, None, "State Code", None, None, None, None, None, None, None, None, None, None, None, None, None, 0, 0, None, None, None, None, 456, "Active", None, None, None, None, None, None, None, None, None, None, None, None, None, None, None),
    # Add more records for edge cases, error cases, special characters, NULL handling...
]

# Create DataFrame using the defined schema and test data
test_df = spark.createDataFrame(test_data, schema=supplier_invoice_schema)

# Save the DataFrame to the target location on Unity Catalog
try:
    test_df.write.format("delta").mode("overwrite").save("purgo_playground.purgo_playground.supplier_invoice")
except Exception as e:
    # Handle any errors during data writing
    print(f"Error in writing data: {e}")

# Stop the Spark session
spark.stop()