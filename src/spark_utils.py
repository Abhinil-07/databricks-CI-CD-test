import os
import warnings

def get_spark_session():
    """
    Returns the right SparkSession depending on where the code is running.
    - On Databricks (Job/Cluster): Uses the native SparkSession (already available).
    - Locally (VS Code + Databricks Connect): Uses DatabricksSession to bridge to the cloud.
    """
    warnings.filterwarnings("ignore")
    
    if "DATABRICKS_RUNTIME_VERSION" in os.environ:
        # We are running INSIDE Databricks (as a Job or on a cluster)
        from pyspark.sql import SparkSession
        return SparkSession.builder.getOrCreate()
    else:
        # We are running LOCALLY (VS Code + Databricks Connect)
        from dotenv import load_dotenv
        from databricks.connect import DatabricksSession
        load_dotenv()
        return DatabricksSession.builder.getOrCreate()
