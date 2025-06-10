import pandas as pd

# Load your CSV
df = pd.read_csv("browser_power_results.csv")

# Group by browser
summary = df.groupby("Browser")["Power(mW)"].agg(
    Mean_mW="mean",
    Min_mW="min",
    Max_mW="max",
    StdDev_mW="std"
)

# Print markdown-style table
print("| Browser | Mean Power (mW) | Min Power (mW) | Max Power (mW) | Std Dev (mW) |")
print("|---------|-----------------|----------------|----------------|--------------|")

for browser, row in summary.iterrows():
    print(f"| {browser} | {row['Mean_mW']:.2f} | {row['Min_mW']} | {row['Max_mW']} | {row['StdDev_mW']:.2f} |")