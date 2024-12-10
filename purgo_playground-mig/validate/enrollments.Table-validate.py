import sys
import os
from sqlalchemy import create_engine
from databricks import sql

redshiftHost = os.getenv("PURGO_REDSHIFT_HOST")
if not redshiftHost:
    sys.exit("PURGO_REDSHIFT_HOST env variable not set")

redshiftPort = os.getenv("PURGO_REDSHIFT_PORT")
if not redshiftPort:
    sys.exit("PURGO_REDSHIFT_PORT env variable not set")

redshiftDB = os.getenv("PURGO_REDSHIFT_DB")
if not redshiftDB:
    sys.exit("PURGO_REDSHIFT_DB env variable not set")

redshiftUser = os.getenv("PURGO_REDSHIFT_USER")
if not redshiftUser:
    sys.exit("PURGO_REDSHIFT_USER env variable not set")

redshiftPassword = os.getenv("PURGO_REDSHIFT_PASSWORD")
if not redshiftPassword:
    sys.exit("PURGO_REDSHIFT_PASSWORD env variable not set")

databricksToken = os.getenv("PURGO_DATABRICKS_TOKEN")
if not databricksToken:
	sys.exit("PURGO_DATABRICKS_TOKEN env variable not set")
	
databricksHost = os.getenv("PURGO_DATABRICKS_HOST")
if not databricksHost:
	sys.exit("PURGO_DATABRICKS_HOST env variable not set")

databricksPort = os.getenv("PURGO_DATABRICKS_PORT")
if not databricksPort:
	sys.exit("PURGO_DATABRICKS_PORT env variable not set")
	
databricksHttpPath = os.getenv("PURGO_DATABRICKS_HTTP_PATH")
if not databricksHttpPath:
	sys.exit("PURGO_DATABRICKS_HTTP_PATH env variable not set")
	
databricksCatalog = os.getenv("PURGO_DATABRICKS_CATALOG")
if not databricksCatalog:
	sys.exit("PURGO_DATABRICKS_CATALOG env variable not set")
	
databricksSchema = os.getenv("PURGO_DATABRICKS_SCHEMA")
if not databricksSchema:
	sys.exit("PURGO_DATABRICKS_SCHEMA env variable not set")

# Redshift

connect = 'postgresql://' + redshiftUser + ':' + redshiftPassword + "@" + redshiftHost + ":" + redshiftPort + "/" +  redshiftDB  
redshiftEngine = create_engine(connect)

redshiftCols = list()
redshiftCharIntCols = list()
with redshiftEngine.connect() as connection:
	result = connection.execute("SELECT * FROM information_schema.columns WHERE table_schema = 'purgo_playground' AND table_name = 'enrollments'")
	for row in result:
		redshiftCols.append(row["column_name"])
		dataType = row["data_type"]
		if "character" in dataType:
			redshiftCharIntCols.append({"column" : row["column_name"], "type" : "char"})
		elif "numeric" in dataType or "integer" in dataType:
			redshiftCharIntCols.append({"column" : row["column_name"], "type" : "int"})
		elif "smallint" in dataType or "bigint" in dataType:
			redshiftCharIntCols.append({"column" : row["column_name"], "type" : "int"})

redshiftCols.sort()

redshiftCount = 0
redshiftTablename = "purgo_playground.[enrollments]"
with redshiftEngine.connect() as connection:
	result = connection.execute("select count(*) as Count from " + redshiftTablename)
	for row in result:
		redshiftCount = row["count"]

# Databricks
databricksConnection = sql.connect(server_hostname = databricksHost, http_path = databricksHttpPath, access_token = databricksToken)              

databricksCols = list()
databricksTablename = databricksCatalog + "." + databricksSchema + "." + "enrollments".replace(" ", "_").lower()
query = "SHOW COLUMNS IN " + databricksTablename
with databricksConnection.cursor() as cursor:
	cursor.execute(query)
	result = cursor.fetchall()
	for row in result:
		databricksCols.append(row["col_name"])

databricksCols.sort()

databricksCount = 0
query = "select count(*) as Count from " + databricksTablename
with databricksConnection.cursor() as cursor:
	cursor.execute(query)
	result = cursor.fetchall()
	for row in result:
		databricksCount = row["Count"]

if redshiftCols == databricksCols:
	print("Columns are identical")
else:
	print("Columns mismatch")
	print("# of Columns in Redshift: ", len(redshiftCols))
	print("# of Columns in Databricks: ", len(databricksCols))
	print("Redshift Columns: ", redshiftCols)
	print("Databricks Columns: ", databricksCols)
	
if redshiftCount == databricksCount:
	print("Number of rows match")
else:
	print("Row count mismatch")
	print("Redshift Row count: ", redshiftCount)
	print("Databricks Row count: ", databricksCount)

# Check each column
charColValidate = """select sum((COLNAME IS NULL)::int) as nullcount, round(avg(cast(len(rtrim(COLNAME)) as float)), 2) as avg, min(len(rtrim(COLNAME))) as min, max(len(rtrim(COLNAME))) as max, round(stddev(len(rtrim(COLNAME))), 2) as stddev from """
intColValidate = """select sum((COLNAME IS NULL)::int) as nullcount, round(avg(cast(COLNAME as float)), 2) as avg, min(COLNAME) as min, max(COLNAME) as max, round(stddev(COLNAME), 2) as stddev from """
redshiftColValidate = charColValidate + redshiftTablename
databricksColValidate = charColValidate + databricksTablename
redshiftIntValidate = intColValidate + redshiftTablename
databricksIntValidate = intColValidate + databricksTablename

for columnInfo in redshiftCharIntCols:
	column = columnInfo["column"]
	type = columnInfo["type"]

	print("Validating column: ", column)
	redshiftValidateSQL = redshiftColValidate.replace("COLNAME", column)
	if type == "int":
		redshiftValidateSQL = redshiftIntValidate.replace("COLNAME", column)

	redshiftNullCount = None
	redshiftAvgVal = None
	redshiftMinVal = None
	redshiftMaxVal = None
	redshiftStddevVal = None

	databricksValidateSQL = databricksColValidate.replace("COLNAME", column)
	if type == "int":
		databricksValidateSQL = databricksIntValidate.replace("COLNAME", column)

	databricksNullCount = None
	databricksAvgVal = None
	databricksMinVal = None
	databricksMaxVal = None
	databricksStddevVal = None

	print("Quering Redshift Column: ", column)
	with redshiftEngine.connect() as connection:
		result = connection.execute(redshiftValidateSQL)
		for row in result:
			redshiftNullCount = row["nullcount"]
			redshiftAvgVal = row["avg"]
			redshiftMinVal = row["min"]
			redshiftMaxVal = row["max"]
			redshiftStddevVal = row["stddev"]

	print("Quering Databricks Column: ", column)
	with databricksConnection.cursor() as cursor:
		cursor.execute(databricksValidateSQL)
		result = cursor.fetchall()
		for row in result:
			databricksNullCount = row["nullcount"]
			databricksAvgVal = row["avg"]
			databricksMinVal = row["min"]
			databricksMaxVal = row["max"]
			databricksStddevVal = row["stddev"]

	# If avg/min/max is negative, return value is a str
	if isinstance(databricksAvgVal, str):
		redshiftAvgVal = str(redshiftAvgVal)
	if isinstance(databricksMinVal, str):
		redshiftMinVal = str(redshiftMinVal)
	if isinstance(databricksMaxVal, str):
		redshiftMaxVal = str(redshiftMaxVal)

	if redshiftNullCount != databricksNullCount or redshiftAvgVal != databricksAvgVal or redshiftMinVal != databricksMinVal or redshiftMaxVal != databricksMaxVal or redshiftStddevVal != databricksStddevVal:
		print("Found discrepancy in row values for column: ", column)

		print("redshiftNullCount: ", redshiftNullCount)
		print("redshiftAvgVal: ", redshiftAvgVal)
		print("redshiftMinVal: ", redshiftMinVal)
		print("redshiftMaxVal: ", redshiftMaxVal)
		print("redshiftStddevVal: ", redshiftStddevVal)

		print("databricksNullCount: ", databricksNullCount)
		print("databricksAvgVal: ", databricksAvgVal)
		print("databricksMinVal: ", databricksMinVal)
		print("databricksMaxVal: ", databricksMaxVal)
		print("databricksStddevVal: ", databricksStddevVal)
	else:
		print("Validate success for Column: ", column)