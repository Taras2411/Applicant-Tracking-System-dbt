Solution to Task #2 for JetBrains internship

How to Run the Project:
Create and activate venv

Install dependencies:
pip install pandas faker matplotlib seaborn duckdb dbt-duckdb
dbt deps

Generate fake data:
python scripts/fake_data_generator.py
move generated .csv to raw_data directory

Execute dbt:
dbt build

Visualisation of "Advanced Analytical SQL" results is posible via provided script
python scripts/visualization.py

