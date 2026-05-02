import os
from dotenv import load_dotenv
from databricks.connect import DatabricksSession
import warnings

warnings.filterwarnings("ignore")
load_dotenv()
spark = DatabricksSession.builder.getOrCreate()

print("\n--- SCHEMA FOR dltprac.source.customers ---")
try:
    spark.sql("DESCRIBE dltprac.source.customers").show(truncate=False)
except Exception as e:
    print(f"Error reading table: {e}")
