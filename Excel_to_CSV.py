import os
import pandas as pd
#output directory
output_dir = "agent_csv_files"
os.makedirs(output_dir, exist_ok=True)
# Reading the source data
df = pd.read_excel("C:\\Users\\U441914\\Documents\\Junction\\Hackathon_HSY_Data.xlsx", "Taul1", header = 0)
# Cleaning the columns and sanitizing them for filenames
df.columns = (
    df.columns
    .str.replace(r"\n", " ", regex=True)
    .str.replace(r"\s", " ",regex = True)
    .str.strip()
    .str.lower()
)

#checking for cleaned column names
#print("Cleaned column names:", df.columns)

#Datetime column to index
datetime_col_name = "time stamp"
df.index = pd.to_datetime(df[datetime_col_name], format="%d/%m/%Y %H.%M.%S")
df = df.drop(columns=[datetime_col_name])
# Converting to CSV

full_path = os.path.join(output_dir, "data_csv_format.csv")
df.columns.to_csv(full_path, index = True)

