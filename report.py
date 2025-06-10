import pandas as pd
import os

def generate_report():
    """Generate a power consumption report from the CSV data"""
    
    # Check if file exists and has data
    if not os.path.exists("browser_power_results.csv"):
        print("❌ Error: browser_power_results.csv not found!")
        print("Please run the benchmark first: sudo python browser_bench.py")
        return
    
    try:
        # Load the CSV
        df = pd.read_csv("browser_power_results.csv")
        
        # Check if we have any data
        if df.empty or len(df) == 0:
            print("❌ No data found in browser_power_results.csv")
            print("The CSV file exists but contains no power measurements.")
            print("Please run the benchmark first: sudo python browser_bench.py")
            return
        
        # Check if we have the expected columns
        if "Browser" not in df.columns or "Power(mW)" not in df.columns:
            print("❌ Invalid CSV format!")
            print(f"Expected columns: Browser, Timestamp, Power(mW)")
            print(f"Found columns: {list(df.columns)}")
            return
        
        # Group by browser and calculate statistics
        summary = df.groupby("Browser")["Power(mW)"].agg(
            Mean_mW="mean",
            Min_mW="min",
            Max_mW="max",
            StdDev_mW="std"
        )
        
        # Print results
        print("🔋 Browser Power Consumption Report")
        print("=" * 50)
        print(f"📊 Total measurements: {len(df)}")
        print(f"🌐 Browsers tested: {', '.join(summary.index)}")
        print(f"📈 Data collected from: {df['Timestamp'].min()} to {df['Timestamp'].max()}")
        print()
        
        # Print markdown-style table
        print("| Browser | Mean Power (mW) | Min Power (mW) | Max Power (mW) | Std Dev (mW) | Measurements |")
        print("|---------|-----------------|----------------|----------------|--------------|--------------|")
        
        for browser, row in summary.iterrows():
            count = len(df[df["Browser"] == browser])
            print(f"| {browser} | {row['Mean_mW']:.2f} | {row['Min_mW']:.0f} | {row['Max_mW']:.0f} | {row['StdDev_mW']:.2f} | {count} |")
        
        print()
        
        # Calculate efficiency comparison if we have multiple browsers
        if len(summary) > 1:
            print("⚡ Efficiency Analysis:")
            browsers = summary.index.tolist()
            most_efficient = summary["Mean_mW"].idxmin()
            least_efficient = summary["Mean_mW"].idxmax()
            
            efficiency_diff = summary.loc[least_efficient, "Mean_mW"] - summary.loc[most_efficient, "Mean_mW"]
            efficiency_percent = (efficiency_diff / summary.loc[least_efficient, "Mean_mW"]) * 100
            
            print(f"🏆 Most efficient: {most_efficient} ({summary.loc[most_efficient, 'Mean_mW']:.0f} mW avg)")
            print(f"🔥 Least efficient: {least_efficient} ({summary.loc[least_efficient, 'Mean_mW']:.0f} mW avg)")
            print(f"💡 Efficiency difference: {efficiency_diff:.0f} mW ({efficiency_percent:.1f}% improvement)")
            
            # Battery life estimation (assuming 50Wh battery)
            battery_wh = 50
            print(f"\n🔋 Estimated battery life (50Wh battery):")
            for browser, row in summary.iterrows():
                hours = battery_wh / (row['Mean_mW'] / 1000)
                print(f"   {browser}: ~{hours:.1f} hours")
        
    except Exception as e:
        print(f"❌ Error processing data: {e}")
        print("Please check the CSV file format and try again.")

if __name__ == "__main__":
    generate_report()