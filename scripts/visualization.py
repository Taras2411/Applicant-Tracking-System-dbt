import duckdb
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(project_root, 'dev.duckdb')

con = duckdb.connect(db_path)


query = """
    SELECT 
        source, 
        hire_month, 
        cumulative_hires 
    FROM dm_cumulative_hires 
    ORDER BY hire_month
"""

df = con.execute(query).df()
con.close()

if df.empty:
    print("No data found to display. Please ensure 'dbt run' has been executed successfully.")
    exit()


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