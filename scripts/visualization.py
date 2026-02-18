import duckdb
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(project_root, 'dev.duckdb')

print("Select the visualization to generate:")
print("1: Cumulative Hires by Source")
print("2: Monthly Active Pipeline")
choice = input("Enter your choice (1 or 2): ").strip()

con = duckdb.connect(db_path)

if choice == '1':
    query = """
        SELECT 
            source, 
            hire_month, 
            cumulative_hires 
        FROM dm_cumulative_hires 
        ORDER BY hire_month
    """

    df = con.execute(query).df()

    if df.empty:
        print("No data found to display. Please ensure 'dbt run' has been executed successfully.")
        con.close()
        sys.exit()

    plt.figure(figsize=(12, 6))
    sns.set_theme(style="whitegrid")

    plot = sns.lineplot(
        data=df, 
        x='hire_month', 
        y='cumulative_hires', 
        hue='source',     
        marker='o',        
        linewidth=2.5
    )

    plot.set_title('Cumulative Hires by Source', fontsize=16)
    plot.set_xlabel('Month', fontsize=12)
    plot.set_ylabel('Total Hires (Cumulative)', fontsize=12)

    plot.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plot.xaxis.set_major_locator(mdates.MonthLocator())
    plt.xticks(rotation=45)

    plt.legend(title='Source', title_fontsize='12', loc='upper left')

    plt.tight_layout()
    plt.show()

elif choice == '2':
    query = """
        SELECT 
            report_month, 
            active_applications
        FROM dm_monthly_active_pipeline 
        ORDER BY report_month
    """

    df = con.execute(query).df()

    if df.empty:
        print("No data found to display. Please ensure 'dbt run' has been executed successfully.")
        con.close()
        sys.exit()

    plt.figure(figsize=(12, 6))
    sns.set_theme(style="whitegrid")

    plot = sns.lineplot(
        data=df, 
        x='report_month', 
        y='active_applications', 
        marker='o',        
        linewidth=2.5,
        color='teal'
    )

    plot.set_title('Monthly Active Pipeline', fontsize=16)
    plot.set_xlabel('Month', fontsize=12)
    plot.set_ylabel('Active Applications', fontsize=12)

    plot.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plot.xaxis.set_major_locator(mdates.MonthLocator())
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

else:
    print("Invalid selection. Please run the script again and select 1 or 2.")

con.close()