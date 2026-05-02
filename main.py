from src.setup_schemas import create_schemas
from src.create_mock_data import create_mocks
from src.pipeline import run_pipeline

if __name__ == "__main__":
    print("========================================")
    print(" DATABRICKS JOB STARTING")
    print("========================================")
    
    # Step 1: Ensure schemas exist
    create_schemas()
    
    # Step 2: (Optional for testing) Populate mock source tables
    # create_mocks()
    
    # Step 3: Run the core transformation logic
    run_pipeline()
    
    print("========================================")
    print(" DATABRICKS JOB FINISHED")
    print("========================================")
