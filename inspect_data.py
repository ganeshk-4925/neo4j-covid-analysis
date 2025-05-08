import pandas as pd

# Load the CSV file
df = pd.read_csv("cleaned_covid_data.csv")

# Display number of rows and columns
print("✅ Number of Rows:", df.shape[0])
print("✅ Number of Columns:", df.shape[1])

# Display the first 5 rows
print("\n📌 Sample Data:")
print(df.head())
