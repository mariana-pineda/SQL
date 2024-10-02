import sys
import os
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, select, text
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import sessionmaker

sqlServerHost = os.getenv("PURGO_SQL_SERVER_HOST")
if not sqlServerHost:
	sys.exit("PURGO_SQL_SERVER_HOST env variable not set")

sqlServerPort = os.getenv("PURGO_SQL_SERVER_PORT")
if not sqlServerPort:
	sys.exit("PURGO_SQL_SERVER_PORT env variable not set")

sqlServerDB = os.getenv("PURGO_SQL_SERVER_DB")
if not sqlServerDB:
	sys.exit("PURGO_SQL_SERVER_DB env variable not set")

sqlServerUser = os.getenv("PURGO_SQL_SERVER_USER")
if not sqlServerUser:
	sys.exit("PURGO_SQL_SERVER_USER env variable not set")

sqlServerPassword = os.getenv("PURGO_SQL_SERVER_PASSWORD")
if not sqlServerPassword:
	sys.exit("PURGO_SQL_SERVER_PASSWORD env variable not set")

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

# SQLServer

sqlServerConnection = "Server=tcp:"+ sqlServerHost + "," + sqlServerPort + ";Database={" + sqlServerDB + "};Uid={" + sqlServerUser + "};Pwd={" + sqlServerPassword + "};Encrypt=yes;TrustServerCertificate=yes;Connection Timeout=30;"
sqlServerEngine = create_engine("mssql+pyodbc:///?odbc_connect=Driver={ODBC Driver 18 for SQL Server};" + sqlServerConnection)

sqlServerTablename = "dbo.[Quarterly Orders]"

df = pd.read_sql('select top 0 * from dbo.[Quarterly Orders]', sqlServerEngine)
sqlServerCols = sorted(df)

df = pd.read_sql('select count(*) as COUNT from dbo.[Quarterly Orders]', sqlServerEngine)
sqlServerCount = df.at[0,'COUNT']

sqlServerCharIntCols = list()
df = pd.read_sql("SELECT * FROM information_schema.columns WHERE table_schema = 'dbo' AND table_name = 'Quarterly Orders'", sqlServerEngine)
for index, row in df.iterrows():
	dataType = row["DATA_TYPE"]
	if "nvarchar" in dataType or "nchar" in dataType or "ntext" in dataType:
		sqlServerCharIntCols.append({"column" : row["COLUMN_NAME"], "type" : "char"})
	elif "varchar" in dataType or "char" in dataType or "text" in dataType:
		sqlServerCharIntCols.append({"column" : row["COLUMN_NAME"], "type" : "char"})
	elif "smallint" in dataType or "bigint" in dataType or "int" in dataType:
		sqlServerCharIntCols.append({"column" : row["COLUMN_NAME"], "type" : "int"})
	elif "tinyint" in dataType or "numeric" in dataType or "decimal" in dataType:
		sqlServerCharIntCols.append({"column" : row["COLUMN_NAME"], "type" : "int"})

# Databricks

databricksConnection =  "databricks://token:" + databricksToken + "@" + databricksHost + ":" + databricksPort + "?http_path=" + databricksHttpPath + "&catalog=" + databricksCatalog + "&schema=" + databricksSchema
databricksEngine = create_engine(url = databricksConnection)

Session = sessionmaker(bind=databricksEngine)
session = Session()
metadata = MetaData()

metadata.reflect(bind=databricksEngine)
metatable = metadata.tables.get("Quarterly Orders".replace(" ", "_").lower())
databricksTablename = databricksCatalog + "." + databricksSchema + "." + "Quarterly Orders".replace(" ", "_").lower()
databricksCols = list()
for col in metatable.columns:
	databricksCols.append(col.name)
databricksCols.sort()

databricksCount = session.query(func.count("*")).select_from(metatable).scalar()

if sqlServerCols == databricksCols:
	print("Columns are identical")
else:
	print("Columns mismatch")
	print("# of Columns in SQLServer: ", len(sqlServerCols))
	print("# of Columns in Databricks: ", len(databricksCols))
	print("SQLServer Columns: ", sqlServerCols)
	print("Databricks Columns: ", databricksCols)
	
if sqlServerCount == databricksCount:
	print("Number of rows match")
else:
	print("Row count mismatch")
	print("SQLServer Row count: ", sqlServerCount)
	print("Databricks Row count: ", databricksCount)

# Check each column
charColValidate = """SELECT COUNT(CASE WHEN COLNAME IS NULL THEN 1 END) as nullcount, ROUND(AVG(CAST(LEN(RTRIM(COLNAME)) as float)), 2) AS avg, min(len(rtrim(COLNAME))) as min, max(len(rtrim(COLNAME))) as max, round(stdev(len(rtrim(COLNAME))), 2) as stddev from """
intColValidate = """SELECT COUNT(CASE WHEN COLNAME IS NULL THEN 1 END) as nullcount, ROUND(AVG(CAST(COLNAME as float)), 2) AS avg, min(COLNAME) as min, max(COLNAME) as max, round(stdev(COLNAME), 2) as stddev from """

databricksCharColValidate = """select sum((COLNAME IS NULL)::int) as nullcount, round(avg(cast(len(rtrim(COLNAME)) as float)), 2) as avg, min(len(rtrim(COLNAME))) as min, max(len(rtrim(COLNAME))) as max, round(stddev(len(rtrim(COLNAME))), 2) as stddev from """
databricksIntColValidate = """select sum((COLNAME IS NULL)::int) as nullcount, round(avg(cast(COLNAME as float)), 2) as avg, min(COLNAME) as min, max(COLNAME) as max, round(stddev(COLNAME), 2) as stddev from """

sqlServerColValidate = charColValidate + sqlServerTablename
databricksColValidate = databricksCharColValidate + databricksTablename
sqlServerIntValidate = intColValidate + sqlServerTablename
databricksIntValidate = databricksIntColValidate + databricksTablename

for columnInfo in sqlServerCharIntCols:
	column = columnInfo["column"]
	type = columnInfo["type"]

	print("Validating column: ", column)
	sqlServerValidateSQL = sqlServerColValidate.replace("COLNAME", column)
	if type == "int":
		sqlServerValidateSQL = sqlServerIntValidate.replace("COLNAME", column)

	sqlServerNullCount = None
	sqlServerAvgVal = None
	sqlServerMinVal = None
	sqlServerMaxVal = None
	sqlServerStddevVal = None

	databricksValidateSQL = databricksColValidate.replace("COLNAME", column)
	if type == "int":
		databricksValidateSQL = databricksIntValidate.replace("COLNAME", column)

	databricksNullCount = None
	databricksAvgVal = None
	databricksMinVal = None
	databricksMaxVal = None
	databricksStddevVal = None

	print("Quering SQLServer Column: ", column)
	df = pd.read_sql(sqlServerValidateSQL, sqlServerEngine)
	for index, row in df.iterrows():
		sqlServerNullCount = row["nullcount"]
		sqlServerAvgVal = row["avg"]
		sqlServerMinVal = row["min"]
		sqlServerMaxVal = row["max"]
		sqlServerStddevVal = row["stddev"]

	print("Quering Databricks Column: ", column)
	with databricksEngine.connect() as connection:
		result = connection.execute(text(databricksValidateSQL))
		for row in result:
			databricksNullCount = row[0]
			databricksAvgVal = row[1]
			databricksMinVal = row[2]
			databricksMaxVal = row[3]
			databricksStddevVal = row[4]

	# If avg/min/max is negative, return value is a str
	if isinstance(databricksAvgVal, str):
		sqlServerAvgVal = str(sqlServerAvgVal)
	if isinstance(databricksMinVal, str):
		sqlServerMinVal = str(sqlServerMinVal)
	if isinstance(databricksMaxVal, str):
		sqlServerMaxVal = str(sqlServerMaxVal)

	if sqlServerNullCount != databricksNullCount or sqlServerAvgVal != databricksAvgVal or sqlServerMinVal != databricksMinVal or sqlServerMaxVal != databricksMaxVal or sqlServerStddevVal != databricksStddevVal:
		print("Found discrepancy in row values for column: ", column)

		print("sqlServerNullCount: ", sqlServerNullCount)
		print("sqlServerAvgVal: ", sqlServerAvgVal)
		print("sqlServerMinVal: ", sqlServerMinVal)
		print("sqlServerMaxVal: ", sqlServerMaxVal)
		print("sqlServerStddevVal: ", sqlServerStddevVal)

		print("databricksNullCount: ", databricksNullCount)
		print("databricksAvgVal: ", databricksAvgVal)
		print("databricksMinVal: ", databricksMinVal)
		print("databricksMaxVal: ", databricksMaxVal)
		print("databricksStddevVal: ", databricksStddevVal)
	else:
		print("Validate success for Column: ", column)