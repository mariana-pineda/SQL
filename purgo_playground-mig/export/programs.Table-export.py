import sys
import os
from pandas import DataFrame
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

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

connect = 'postgresql://' + redshiftUser + ':' + redshiftPassword + "@" + redshiftHost + ":" + redshiftPort + "/" +  redshiftDB  
redshiftEngine = create_engine(connect)

with redshiftEngine.connect() as connection:
	result = connection.execute('select * from purgo_playground.[programs]')
	df = DataFrame(result)
	df.to_parquet("programs.parquet", index=False)
