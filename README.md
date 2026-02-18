# JetBrains Internship Task #2

This repository contains the technical implementation for the Data Cleaning, Modeling, and Advanced Analytical SQL task. I utilized **dbt (Data Build Tool)** with **DuckDB** for this project, as experience with dbt was noted as a preferred skill for the position.

### Data Generation
Since a raw dataset was not provided with the task assignment, I developed a Python script to generate synthetic data. This script creates `raw_candidates`, `raw_applications`, and `raw_interviews` CSV files that match the specified schema and include edge cases to test data quality logic.

### Data Quality and Business Logic
I implemented a robust data quality strategy using dbt tests and filtering logic. Tests configured with `severity: warn` allow the pipeline to continue running while alerting on low-quality raw data. Subsequent models actively filter out rows that fail these checks, such as interviews occurring before the application date, ensuring only valid data reaches the final Data Marts.

For the **Monthly Active Pipeline** metric, I applied a specific business rule: applications older than 90 days are automatically considered closed. Without this logic, the active pipeline count would accumulate indefinitely, creating a "snowball effect" of stale data month over month.

### Project Structure
The project follows a three-layer architecture:
*   **Staging:** Handles deduplication, type casting, and standardizing values (e.g., Source fields).
*   **Intermediate:** Joins tables to link candidates with applications and applies business logic filters to remove invalid records.
*   **Mart:** Aggregates the clean data into final tables (`dm_hiring_process`, `dm_cumulative_hires`, `dm_monthly_active_pipeline`) ready for analysis.

### How to Run

Execute the following commands in your terminal to set up the environment, generate data, build the models, and run visualizations.
Initialization of the virtual environment is recommended before these steps.

```bash
# 1. Install dependencies
pip install pandas faker matplotlib seaborn duckdb dbt-duckdb

# 2. Install dbt packages
dbt deps

# 3. Generate synthetic data (move resulting .csv files to the raw_data/ folder)
python scripts/fake_data_generator.py

# 4. Build dbt models and run tests
dbt build

# 5. Visualize results
python scripts/visualization.py
```