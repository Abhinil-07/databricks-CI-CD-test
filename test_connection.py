import os
from dotenv import load_dotenv
from databricks.connect import DatabricksSession

# Load environment variables from .env file
load_dotenv()

def test_connection():
    print("Connecting to Databricks...")
    # The builder automatically looks for DATABRICKS_HOST, DATABRICKS_TOKEN, and DATABRICKS_CLUSTER_ID
    spark = DatabricksSession.builder.getOrCreate()

    print("Executing query on the cloud cluster...")
    df = spark.sql("SELECT 'Databricks Connect is working perfectly!' as Message")
    df2 = spark.sql("select * from dltprac.source.customers")
    df.show()
    df2.show()
    # df = spark.sql("select * from ")

if __name__ == "__main__":
    test_connection()
