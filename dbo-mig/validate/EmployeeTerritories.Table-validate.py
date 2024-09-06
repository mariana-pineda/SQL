import sys
import os
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, select
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

df = pd.read_sql('select top 0 * from dbo.employeeterritories', sqlServerEngine)
sqlServerCols = sorted(df)

df = pd.read_sql('select count(*) as COUNT from dbo.employeeterritories', sqlServerEngine)
sqlServerCount = df.at[0,'COUNT']

# Databricks

databricksConnection =  "databricks://token:" + databricksToken + "@" + databricksHost + ":" + databricksPort + "?http_path=" + databricksHttpPath + "&catalog=" + databricksCatalog + "&schema=" + databricksSchema
databricksEngine = create_engine(url = databricksConnection)

Session = sessionmaker(bind=databricksEngine)
session = Session()
metadata = MetaData()

metadata.reflect(bind=databricksEngine)
metatable = metadata.tables.get("dbo.employeeterritories")
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
