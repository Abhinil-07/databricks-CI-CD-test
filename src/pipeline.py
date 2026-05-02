import pyspark.sql.functions as F
from src.spark_utils import get_spark_session

def run_pipeline():
    spark = get_spark_session()
    
    print(" Starting Data Pipeline...")

    # 1. Read regional sales tables
    print("1. Reading regional sales tables (`workspace.default.sales_east` and `workspace.default.sales_west`)...")
    df_east = spark.table("workspace.default.sales_east")
    df_west = spark.table("workspace.default.sales_west")
    
    # 2. Union the tables
    print("2. Unioning regional sales data...")
    df_cumulative = df_east.unionByName(df_west, allowMissingColumns=True)
    
    # 3. Write to cumulative table
    print("3. Saving to `test.sales.cumulative_sales`...")
    df_cumulative.write.format("delta").mode("overwrite").saveAsTable("test.sales.cumulative_sales")
    
    # 4. Read products table and join with cumulative sales
    print("4. Joining cumulative sales with `workspace.default.products`...")
    df_products = spark.table("workspace.default.products")
    df_sales_cumulative = spark.table("test.sales.cumulative_sales")
    
    # Perform a left join to keep all sales, even if a product ID is missing
    df_joined = df_sales_cumulative.join(df_products, on="product_id", how="left")
    
    # 5. Aggregate total sales by product
    print("5. Aggregating total sales by product...")
    df_total_sales = df_joined.groupBy("product_id", "product_name") \
                              .agg(F.sum("sales_amount").alias("total_sales_amount"))
                              
    # 6. Write final table
    print("6. Saving final aggregations to `test.product.total_sales`...")
    df_total_sales.write.format("delta").mode("overwrite").saveAsTable("test.product.total_sales")
    
    print(" Pipeline completed successfully!")
    
    # Show the final result for quick local validation
    print("\n--- FINAL TABLE PREVIEW ---")
    df_total_sales.show()

if __name__ == "__main__":
    run_pipeline()
