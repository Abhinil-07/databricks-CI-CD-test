# Databricks CI/CD & Local Development Project: End-to-End Documentation

## 1. Project Overview
This project establishes a modern Data Engineering workflow using **Databricks Asset Bundles (DABs)**, **Databricks Connect**, and **GitHub Actions**. It allows engineers to develop and test PySpark code locally in their IDE while ensuring seamless, version-controlled deployments to Databricks environments (Dev/Prod).

## 2. Project Architecture & Codebase
The repository is structured to separate orchestration, core logic, and configuration:

*   **`databricks.yml`**: The core configuration for Databricks Asset Bundles. It defines the deployment targets (`dev`, `prod`), the Databricks workspace host, and the job definition (`daily_sales_pipeline_job`), which maps to `main.py`.
*   **`main.py`**: The main entry point for the Databricks job. It acts as an orchestrator by sequentially calling `create_schemas()` and `run_pipeline()`.
*   **`src/spark_utils.py`**: A dynamic Spark session builder. It checks for the `DATABRICKS_RUNTIME_VERSION` environment variable to determine execution context:
    *   If on a cluster: Uses the native `SparkSession`.
    *   If local: Loads credentials from `.env` and connects to the cluster remotely using `DatabricksSession` (Databricks Connect).
*   **`src/setup_schemas.py`**: Handles DDL operations. It runs `CREATE CATALOG` and `CREATE SCHEMA` SQL commands to ensure the target destinations (`test.sales`, `test.product`) exist in Unity Catalog before data is written.
*   **`src/pipeline.py`**: The core ETL logic. It:
    1.  Reads regional data (`workspace.default.sales_east` & `sales_west`).
    2.  Unions them into a single dataset.
    3.  Writes the unified data to a cumulative Delta table.
    4.  Joins the cumulative sales with a `products` dimension table.
    5.  Aggregates the total sales amount by product and writes the final Gold table.

## 3. Local Development & Authentication
To enable local execution and bundle validation, authentication was configured:
*   **`.env` Setup:** Local execution relies on a Personal Access Token (PAT) stored as `DATABRICKS_TOKEN` inside a local `.env` file, alongside the `DATABRICKS_HOST`.
*   **CLI Profile:** For local CLI commands, we validated that setting `$env:DATABRICKS_TOKEN` and `$env:DATABRICKS_HOST` in the terminal allows the Databricks CLI to authenticate seamlessly without interactive prompts.
*   **Validation:** We used `databricks bundle validate -t dev` to verify the syntactic correctness of the infrastructure-as-code YAML.

## 4. Deployment via Databricks Asset Bundles
We set up and debugged the bundle deployment process:
*   **Terraform Key Expiry Issue:** During local deployment (`databricks bundle deploy`), we encountered a known HashiCorp `openpgp: key expired` error. This occurs when the Databricks CLI caches an outdated Terraform provider signature.
    *   *Resolution:* Deleting the local, hidden `.databricks/` cache folder forces the CLI to download fresh, valid providers.
*   **Workspace Syncing:** We identified that `spark_python_task` by default only uploads the specified entry file. To ensure the `src/` directory is deployed alongside `main.py`, `source: WORKSPACE` must be included in the bundle configuration.

## 5. CI/CD Integration (GitHub Actions)
The project is fully automated via `.github/workflows/deploy.yml`:
*   **Triggers:** The workflow triggers on pushes and Pull Requests to the `main` branch.
*   **Authentication:** Instead of a PAT, the CI/CD pipeline authenticates securely using an OAuth Machine-to-Machine (M2M) Service Principal via GitHub Secrets (`DATABRICKS_CLIENT_ID`, `DATABRICKS_CLIENT_SECRET`).
*   **Stages:**
    1.  **Validate:** Installs the Databricks CLI and runs `bundle validate -t prod`.
    2.  **Deploy:** Runs `bundle deploy -t prod` to push the code and job definitions to the production workspace.
    3.  **Run:** Executes `bundle run -t prod daily_sales_pipeline_job` to trigger the pipeline immediately after a successful deployment.

## 6. Unity Catalog Permissions & Troubleshooting
After a successful CI/CD deployment, the Databricks job failed on the cluster with an `[UNAUTHORIZED_ACCESS]` error:
> `User does not have CREATE CATALOG on Metastore`

*   **The Cause:** In Databricks Unity Catalog, Service Principals and standard users do not have permissions to create top-level Catalogs on the Metastore by default. The command `spark.sql("CREATE CATALOG IF NOT EXISTS test")` was being blocked.
*   **The Resolution:** The code was modified and pushed to `main` to adapt to the Service Principal's permissions, ensuring that schema creation targets existing workspaces or catalogs where the Service Principal has explicit `USE CATALOG` and `CREATE SCHEMA` grants. The logs were updated to reflect: *"Schemas created successfully with service principal!"*
