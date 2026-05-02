import os
import warnings
from dotenv import load_dotenv
from databricks.connect import DatabricksSession

def get_spark_session():
    """Initializes and returns the Databricks Connect Spark session."""
    warnings.filterwarnings("ignore")
    load_dotenv()
    
    spark = DatabricksSession.builder.getOrCreate()
    return spark
