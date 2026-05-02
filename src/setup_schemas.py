from src.spark_utils import get_spark_session

def create_schemas():
    spark = get_spark_session()
    
    print(" Creating schemas...")
    
    # In Databricks, CREATE SCHEMA does not support multi-level catalogs implicitly without USE CATALOG.
    # We will assume 'workspace' catalog since the user wants 'workspace.default.*'
    
    # We will create the schemas inside the 'test' catalog. 
    # But wait, Unity Catalog needs catalogs to be explicitly created. 
    # If the user doesn't have a 'test' catalog, this will fail. 
    # We will create the schemas inside the default catalog for now, or just try to create them.
    # Let's use spark.sql to create them. If 'test' is meant to be a catalog, we should create a catalog.
    # The user wrote 'test.sales.cumulative_sales', meaning 'test' is the catalog, 'sales' is the schema.
    
    spark.sql("CREATE CATALOG IF NOT EXISTS test")
    spark.sql("CREATE SCHEMA IF NOT EXISTS test.sales")
    spark.sql("CREATE SCHEMA IF NOT EXISTS test.product")
    
    print(" Schemas `test.sales` and `test.product` created successfully with service principal!")

if __name__ == "__main__":
    create_schemas()
