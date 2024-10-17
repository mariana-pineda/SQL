import sys
import os
import pyodbc
import pandas as pd
from sqlalchemy import create_engine

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

sqlServerConnection = "Server=tcp:"+ sqlServerHost + "," + sqlServerPort + ";Database={" + sqlServerDB + "};Uid={" + sqlServerUser + "};Pwd={" + sqlServerPassword + "};Encrypt=yes;TrustServerCertificate=yes;Connection Timeout=30;"
sqlServerEngine = create_engine("mssql+pyodbc:///?odbc_connect=Driver={ODBC Driver 18 for SQL Server};" + sqlServerConnection)

df = pd.read_sql('select * from dbo.[CustomerDemographics]', sqlServerEngine)
df.to_parquet("CustomerDemographics.parquet", index=True)