import os
import sys
import csv
import pyodbc
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

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

databricksConnection =  "databricks://token:" + databricksToken + "@" + databricksHost + ":" + databricksPort + "?http_path=" + databricksHttpPath + "&catalog=" + databricksCatalog + "&schema=" + databricksSchema
databricksEngine = create_engine(url = databricksConnection, echo=True)

df = pd.read_parquet("Cateries.parquet")
df.to_sql("Cateries", databricksEngine, if_exists='replace', index=False)