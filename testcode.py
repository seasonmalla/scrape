import json
import pandas as pd


import os
import json

# Path to the folder containing JSON files
folder_path = "json_data"

# List to store all parsed JSON objects
all_data = []

rows = []
# Loop through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        file_path = os.path.join(folder_path, filename)
        
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                for entry in data.get('data', []):
                    fiscal_report = entry.get('fiscalReport', {})
                    quarter_master = fiscal_report.get('quarterMaster', {})
                    quarter_name = quarter_master.get('quarterName') if quarter_master else None
                    row = {
                        'pe_value': fiscal_report.get('peValue'),
                        'eps_value': fiscal_report.get('epsValue'),
                        'netWorth_per_share': fiscal_report.get('netWorthPerShare'),
                        'quarter_name':quarter_name,
                        'report_name':fiscal_report.get('reportTypeMaster',{}).get('reportName')
                    }
                    rows.append(row)
            except json.JSONDecodeError as e:
                print(f"Error reading {filename}: {e}")

df = pd.DataFrame(rows)
df.to_csv('output.csv', index=False)  # Save DataFrame to CSV

# # Step 1: Read JSON file
# with open('json_data/131_data.json', 'r') as file:
#     json_data = json.load(file)  # Load JSON into a Python list/dict

# # Step 2: Extract relevant fields (if nested)
# rows = []
# for entry in json_data['131']:
#     fiscal_report = entry.get('fiscalReport', {})
#     quarter_master = fiscal_report.get('quarterMaster', {})
#     quarter_name = quarter_master.get('quarterName') if quarter_master else None
#     row = {
#         'pe_value': fiscal_report.get('peValue'),
#         'eps_value': fiscal_report.get('epsValue'),
#         'netWorth_per_share': fiscal_report.get('netWorthPerShare'),
#         'quarter_name':quarter_name,
#         'report_name':fiscal_report.get('reportTypeMaster',{}).get('reportName')
#     }
#     rows.append(row)

# # Step 3: Convert to DataFrame
# df = pd.DataFrame(rows)

print(df.head())