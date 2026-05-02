from src.spark_utils import get_spark_session

def create_mocks():
    spark = get_spark_session()
    print(" Creating mock source tables in workspace.default...")
    
    spark.sql("CREATE SCHEMA IF NOT EXISTS workspace.default")

    # Mock East Sales
    spark.sql("""
        CREATE OR REPLACE TABLE workspace.default.sales_east AS 
        SELECT 1 as transaction_id, 101 as product_id, 250.00 as sales_amount UNION ALL
        SELECT 2 as transaction_id, 102 as product_id, 150.50 as sales_amount
    """)
    
    # Mock West Sales
    spark.sql("""
        CREATE OR REPLACE TABLE workspace.default.sales_west AS 
        SELECT 3 as transaction_id, 101 as product_id, 300.00 as sales_amount UNION ALL
        SELECT 4 as transaction_id, 103 as product_id, 99.99 as sales_amount
    """)
    
    # Mock Products
    spark.sql("""
        CREATE OR REPLACE TABLE workspace.default.products AS 
        SELECT 101 as product_id, 'Laptop' as product_name UNION ALL
        SELECT 102 as product_id, 'Mouse' as product_name UNION ALL
        SELECT 103 as product_id, 'Keyboard' as product_name
    """)
    
    print(" Mock data tables `sales_east`, `sales_west`, and `products` created successfully!")

if __name__ == "__main__":
    create_mocks()
