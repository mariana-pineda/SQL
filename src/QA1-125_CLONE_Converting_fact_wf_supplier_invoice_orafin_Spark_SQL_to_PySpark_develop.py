# /* 
#    PySpark Implementation for Converting Spark.SQL Notebook to PySpark
#    Unity Catalog: purgo_databricks
#    Unity Catalog Schema: purgo_playground
# */

# Import necessary modules
from datetime import datetime
from pyspark.sql.functions import col, row_number, date_format, concat_ws, coalesce, when
from pyspark.sql.window import Window

# /* 
#    Initialize Variables from Widgets
# */
try:
    target_table_path = dbutils.widgets.get("target_table_path")
    partition_key = dbutils.widgets.get("partition")
    table_format = dbutils.widgets.get("table_format")
    compression = dbutils.widgets.get("compression")
    table_name = dbutils.widgets.get("table_name")
    unity_catalog = dbutils.widgets.get("unity_catalog")
    environment = dbutils.widgets.get("environment")
    project = dbutils.widgets.get("project")
    load_type = dbutils.widgets.get("load_type")
    unity_path = f"{unity_catalog}.{table_name}"
    view_unity_catalog_name = dbutils.widgets.get("view_unity_catalog_name")
    raw_unity_catalog = dbutils.widgets.get("raw_unity_catalog")
    raw_unity_catalog_hist = dbutils.widgets.get("raw_unity_catalog_hist")
    config_unity_catalog = dbutils.widgets.get("config_unity_catalog")
    edp_lkp_unity_catalog = dbutils.widgets.get("edp_lkp_unity_catalog")
    dims_unity_catalog = dbutils.widgets.get("dims_unity_catalog")
    spark.conf.set("raw_catalog.schema", raw_unity_catalog)
    spark.conf.set("unity_catalog.schema", unity_catalog)
except Exception as e:
    # Handle missing or invalid widgets
    raise ValueError(f"Error initializing widgets: {e}")

# /* 
#    Set Spark Configuration
# */
spark.conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")

# /* 
#    Retrieve Job ID
# */
try: 
    jobId = dbutils.notebook.entry_point.getDbutils().notebook().getContext().jobId().get()
except: 
    jobId = -123 
baseUrl, JobsAPI_Secret = get_basejob_url(environment)
jobUrl = baseUrl + "/#job/" + str(jobId) + "/run/1"

# /* 
#    Read Control Table
# */
control_table = f"{config_unity_catalog}.{cl_control_table}"
ctrl_tbl_entry = read_control_table(project, table_name, load_type, control_table)

# /* 
#    Define CTE: dw_ap_sla_aging_invoice_ca_vw
# */
df_dw_ap_sla_aging_invoice_ca = spark.table(f"{raw_unity_catalog}.dw_ap_sla_aging_invoice_ca")

window_spec = Window.partitionBy("invoice_id").orderBy(col("snapshot_captured_date").desc())
df_dw_ap_sla_aging_invoice_ca_vw = df_dw_ap_sla_aging_invoice_ca.withColumn("RowNum", row_number().over(window_spec)).filter(col("RowNum") == 1).drop("RowNum")

# /* 
#    Define CTE: FAW
# */
df_dw_ap_sla_expense_dist_cf = spark.table(f"{raw_unity_catalog}.dw_ap_sla_expense_dist_cf")
window_spec_faw = Window.partitionBy(
    "invoice_distribution_id",
    "gl_balancing_segment",
    "cost_center_segment",
    "gl_segment1",
    "invoice_id",
    "distribution_line_number",
    "invoice_line_number",
    "invoice_accounting_date",
    "transaction_amount"
).orderBy(col("xla_manual_override_flag").desc())

df_dasedc = df_dw_ap_sla_expense_dist_cf.withColumn("RowNum", row_number().over(window_spec_faw)).filter(col("RowNum") == 1).drop("RowNum")

df_dpd = spark.table(f"{raw_unity_catalog}.dw_party_d")
df_dssd = spark.table(f"{raw_unity_catalog}.dw_supplier_site_d")

# /* 
#    Perform Joins and Select Required Columns for FAW
# */
df_faw = (
    df_dw_ap_sla_aging_invoice_ca_vw.alias("dasaic")
    .join(df_dasedc.alias("dasedc"), on="invoice_id", how="left")
    .join(df_dpd.alias("dpd"), on=col("dasaic.supplier_party_id") == col("dpd.party_id"), how="left")
    .join(df_dssd.alias("dssd"), on="supplier_site_id", how="left")
    .select(
        col("document_type").cast("string"),
        col("txn_ref_nbr").cast("string"),
        date_format(col("dasaic.invoiced_on_date"), "yyyyMM").alias("invc_entry_period"),
        col("po_nbr").cast("string"),
        col("po_line_nbr").cast("string"),
        when(lit(True), "usorafin").alias("src_sys_cd"),
        col("dasaic.invoice_id").cast("string").alias("vchr_nbr"),
        concat_ws("-", col("dasedc.invoice_line_number"), col("dasedc.distribution_line_number")).cast("string").alias("vchr_line_nbr"),
        date_format(col("dasedc.invoice_accounting_date"), "yyyy").cast("string").alias("fscl_yr_nbr"),
        col("dasaic.invoice_type_code").alias("vchr_type_cd"),
        col("vchr_status").cast("string"),
        col("item_nbr").cast("string"),
        col("item_desc").cast("string"),
        col("thermo_item_nbr").cast("string"),
        concat_ws("_", coalesce(col("dpd.supplier_number"), lit("0")), col("dssd.supplier_site_id")).alias("supplier_cd"),
        col("dpd.party_name").alias("supplier_name"),
        col("supplier_type_cd").cast("string"),
        col("buyer_cd").cast("string"),
        col("document_desc").cast("string"),
        col("invc_txn_type").cast("string"),
        col("buyer_nm").cast("string"),
        coalesce(col("dasedc.gl_balancing_segment"), col("dasaic.gl_balancing_segment")).alias("co_cd"),
        col("comp.co_nm").alias("co_name"),
        col("edp_lkup.lkup_val_03").alias("hfm_entity"),
        col("diodt.organization_name").alias("business_unit"),
        col("lcr_flag").cast("string"),
        col("lcr_region").cast("string"),
        col("vomi_flag").cast("string"),
        col("payment_compliance_flg").cast("string"),
        col("dasaic.transaction_currency_code").alias("po_curncy_cd"),
        col("dasaic.ledger_currency_code").alias("co_curncy_cd"),
        date_format(col("dasedc.invoice_accounting_date"), "yyyyMM").cast("string").alias("post_yr_mth_nbr"),
        date_format(col("dasaic.invoiced_on_date"), "yyyyMMdd").cast("string").alias("invc_entry_dt"),
        date_format(col("dasaic.invoice_schedule_due_date"), "yyyyMMdd").cast("string").alias("paymt_due_dt"),
        date_format(col("dasaic.invoice_accounting_date"), "yyyyMMdd").cast("string").alias("suplr_invc_dt"),
        col("aprval_dt").cast("string"),
        col("txn_orig_id").cast("string"),
        col("dasaic.invoice_number").alias("suplr_invc_nbr"),
        col("invc_apprv_id").cast("string"),
        col("dasedc.transaction_amount").cast("double").alias("unit_prc"),
        lit(1).cast("double").alias("invc_qty"),
        col("base_qty").cast("double"),
        col("dasedc.transaction_amount").cast("double").alias("invc_txn_amt"),
        col("dasedc.transaction_amount").cast("double").alias("invc_co_amt"),
        lit(None).cast("double").alias("invc_txn_pmar_amt"),
        lit(0).cast("double").alias("invc_co_pmar_amt"),
        lit(0).cast("double").alias("unit_prc_pmar_amt"),
        lit(0).cast("double").alias("txn_curncy_mth_rt"),
        lit(0).cast("double").alias("co_curncy_mth_rt"),
        col("uom_conv_factor").cast("double"),
        col("invc_uom_cd").cast("string"),
        col("base_uom_cd").cast("string"),
        col("profit_cntr").cast("string"),
        when(
            coalesce(col("edp_lkup_div.lkup_val_01"), col("edp_lkup_div_1.lkup_val_01")).isNull(),
            when(coalesce(col("dasedc.gl_balancing_segment"), col("dasaic.gl_balancing_segment")) == 400, "CCG Group")
            .when(coalesce(col("dasedc.gl_balancing_segment"), col("dasaic.gl_balancing_segment")) == 700, "Corporate")
        ).otherwise(coalesce(col("edp_lkup_div.lkup_val_01"), col("edp_lkup_div_1.lkup_val_01"))).alias("div_cd"),
        col("site_cd").cast("string"),
        col("site_name").cast("string"),
        col("reporting_site").cast("string"),
        col("warehouse").cast("string"),
        col("warehouse_nm").cast("string"),
        col("unit").cast("string"),
        col("nature").cast("string"),
        col("inv_flg").cast("string"),
        col("contract_start_date").cast("string"),
        col("contract_end_date").cast("string"),
        col("fk_orig").cast("string"),
        col("floor_stock_cd").cast("string"),
        col("sec_supp_cd").cast("string"),
        col("rpt_flex1").cast("string"),
        col("supplier_segment").cast("string"),
        col("inv_flg_text").cast("string"),
        col("invc_txn_amt_clsfctn").cast("string"),
        lit("NA").alias("source_country"),
        col("business_unit").cast("string"),
        col("ap_payment_term_cd").cast("string"),
        coalesce(col("datdt.payment_term_description"), col("edp_lkup_payment.lkup_val_01")).alias("ap_payment_term_desc"),
        date_format(col("daspc.check_date"), "yyyy-MM-dd").cast("string").alias("actual_payment_dt")
    )
)

# /* 
#    Select Final DataFrame and Write to Target Table
# */
try:
    # Validate the number of columns matches the target schema
    target_schema = spark.table("purgo_playground.supplier_invoice_orig").schema
    if len(df_faw.columns) != len(target_schema.fields):
        raise ValueError("Column count mismatch between source data and target table schema.")

    # Convert data types to match target schema
    for field in target_schema.fields:
        df_faw = df_faw.withColumn(field.name, col(field.name).cast(field.dataType))

    # Write DataFrame to target table
    df_faw.write.mode("overwrite").format(table_format).option("compression", compression).partitionBy(partition_key).saveAsTable(f"{unity_catalog}.{table_name}")
except Exception as e:
    # Handle errors during write operation
    raise RuntimeError(f"Error writing to target table: {e}")

# /* 
#    End of PySpark Script
# */