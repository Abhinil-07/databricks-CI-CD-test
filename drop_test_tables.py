from src.spark_utils import get_spark_session

def drop_tables():
    spark = get_spark_session()
    print(" Cleaning up test tables and schemas...")

    try:
        spark.sql("DROP TABLE IF EXISTS test.sales.cumulative_sales")
        print("Dropped table: test.sales.cumulative_sales")
    except Exception as e:
        print(f"Skipped dropping cumulative_sales: {e}")

    try:
        spark.sql("DROP TABLE IF EXISTS test.product.total_sales")
        print("Dropped table: test.product.total_sales")
    except Exception as e:
        print(f"Skipped dropping total_sales: {e}")

    try:
        spark.sql("DROP SCHEMA IF EXISTS test.sales CASCADE")
        print("Dropped schema: test.sales")
    except Exception as e:
        print(f"Skipped dropping schema test.sales: {e}")

    try:
        spark.sql("DROP SCHEMA IF EXISTS test.product CASCADE")
        print("Dropped schema: test.product")
    except Exception as e:
        print(f"Skipped dropping schema test.product: {e}")

    print(" All test tables and schemas have been dropped!")

if __name__ == "__main__":
    drop_tables()
