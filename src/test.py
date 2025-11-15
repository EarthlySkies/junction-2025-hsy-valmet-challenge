import pandas as pd

csv_file = "Hackathon_HSY_data.csv"

# Read CSV
df = pd.read_csv(csv_file)

# Get last column name
last_col = df.columns[-1]

# Row 3 in Excel-style indexing = index 2 in pandas
start_index = 2
count = 96
end_index = start_index + count  # non-inclusive

# Slice and convert to list
values = df[last_col].iloc[start_index:end_index].tolist()

print(values)
print(len(values))  # should be 96