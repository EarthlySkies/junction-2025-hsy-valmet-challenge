import pandas as pd

excel_file = "Hackathon_HSY_data.xlsx"   # path to your file
csv_file = "Hackathon_HSY_data.csv"      # output filename

df = pd.read_excel(excel_file)          # by default reads the first sheet
df.to_csv(csv_file, index=False)