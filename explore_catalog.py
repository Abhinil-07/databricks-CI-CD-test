import os
import warnings
from dotenv import load_dotenv
from databricks.connect import DatabricksSession

# Suppress warnings to keep output clean
warnings.filterwarnings("ignore")

load_dotenv()
spark = DatabricksSession.builder.getOrCreate()

print("====================================")
print(" FETCHING DATABRICKS CATALOGS")
print("====================================")
spark.sql("SHOW CATALOGS").show(truncate=False)

print("====================================")
print(" SCHEMAS IN 'main' CATALOG")
print("====================================")
try:
    spark.sql("SHOW SCHEMAS IN main").show(truncate=False)
    
    print("====================================")
    print(" TABLES IN 'main.default'")
    print("====================================")
    spark.sql("SHOW TABLES IN main.default").show(truncate=False)
except Exception as e:
    print(f"Could not fetch 'main' catalog data: {e}\n")

print("====================================")
print(" SCHEMAS IN 'hive_metastore' (Legacy)")
print("====================================")
try:
    spark.sql("SHOW SCHEMAS IN hive_metastore").show(truncate=False)
    
    print("====================================")
    print(" TABLES IN 'hive_metastore.default'")
    print("====================================")
    spark.sql("SHOW TABLES IN hive_metastore.default").show(truncate=False)
except Exception as e:
    print(f"Could not fetch 'hive_metastore' data: {e}\n")
