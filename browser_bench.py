import subprocess
import time
import webbrowser
import os
from threading import Thread

# Configuration
BROWSERS = {
    "Safari": "safari",
    "Brave": "brave-browser"  # assumes Brave is installed from brew
}
POWERMETRICS_DURATION_SEC = 120  # Increased to 2 minutes for better measurement
TAB_ACTIVITY_DURATION = 90  # Duration to actively use tabs (scrolling, focusing)
SITES_FILE = "sites.txt"
OUTPUT_FILE = "browser_power_results.csv"

# Open 10 tabs in a browser using osascript (AppleScript)
def open_tabs_in_browser(browser_name, sites):
    print(f"Opening {len(sites)} tabs in {browser_name}...")
    if browser_name == "Safari":
        script = 'tell application "Safari" to activate\n'
        for site in sites:
            script += f'tell application "Safari" to open location "{site}"\n'
    elif browser_name == "Brave":
        script = 'tell application "Brave Browser" to activate\n'
        for site in sites:
            script += f'tell application "Brave Browser" to open location "{site}"\n'
    else:
        raise ValueError("Unsupported browser")

    subprocess.run(["osascript", "-e", script])
    print(f"Tabs opened in {browser_name}.")

# Simulate active browsing by focusing and scrolling through tabs
def simulate_active_browsing(browser_name, num_tabs, duration_sec):
    """
    Cycles through tabs and scrolls to simulate realistic browsing behavior
    """
    print(f"Starting active browsing simulation for {browser_name}...")
    
    start_time = time.time()
    tab_index = 1
    
    while time.time() - start_time < duration_sec:
        try:
            if browser_name == "Safari":
                # Focus on current tab
                focus_script = f'''
                tell application "Safari"
                    activate
                    set current tab of window 1 to tab {tab_index} of window 1
                end tell
                '''
                
                # Scroll down and up
                scroll_script = '''
                tell application "System Events"
                    tell process "Safari"
                        key code 125 using {command down}  -- Page Down
                        delay 0.5
                        key code 125 using {command down}  -- Page Down again
                        delay 0.5
                        key code 126 using {command down}  -- Page Up
                        delay 0.5
                    end tell
                end tell
                '''
                
            elif browser_name == "Brave":
                # Focus on current tab
                focus_script = f'''
                tell application "Brave Browser"
                    activate
                    set active tab index of window 1 to {tab_index}
                end tell
                '''
                
                # Scroll down and up
                scroll_script = '''
                tell application "System Events"
                    tell process "Brave Browser"
                        key code 125 using {command down}  -- Page Down
                        delay 0.5
                        key code 125 using {command down}  -- Page Down again
                        delay 0.5
                        key code 126 using {command down}  -- Page Up
                        delay 0.5
                    end tell
                end tell
                '''
            
            # Execute the scripts
            subprocess.run(["osascript", "-e", focus_script])
            time.sleep(0.5)  # Brief pause after tab switch
            subprocess.run(["osascript", "-e", scroll_script])
            
            # Move to next tab (cycle through all tabs)
            tab_index = (tab_index % num_tabs) + 1
            
            # Wait a bit before moving to next tab
            time.sleep(2)
            
        except Exception as e:
            print(f"Error during browsing simulation: {e}")
            time.sleep(1)
    
    print(f"Active browsing simulation completed for {browser_name}.")

# Run powermetrics and collect power data while simulating active browsing
def run_powermetrics(browser_name, num_tabs):
    print(f"Running powermetrics for {browser_name}...")
    
    # Start browsing simulation in a separate thread
    browsing_thread = Thread(target=simulate_active_browsing, 
                           args=(browser_name, num_tabs, TAB_ACTIVITY_DURATION))
    browsing_thread.daemon = True
    browsing_thread.start()
    
    with open(OUTPUT_FILE, "a") as f:
        proc = subprocess.Popen(
            ["sudo", "powermetrics", "-i", "1000", "--samplers", "cpu_power,gpu_power",
             "-a", "--hide-cpu-duty-cycle", "--show-usage-summary", "--show-extra-power-info"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        start_time = time.time()
        power_readings = 0
        
        while time.time() - start_time < POWERMETRICS_DURATION_SEC:
            line = proc.stdout.readline()
            if "Combined Power (CPU + GPU + ANE):" in line:
                try:
                    value = int(line.split(":")[1].strip().replace("mW", "").strip())
                    timestamp = int(time.time())
                    f.write(f"{browser_name},{timestamp},{value}\n")
                    f.flush()
                    power_readings += 1
                    if power_readings % 10 == 0:  # Progress indicator
                        print(f"  Collected {power_readings} power readings...")
                except ValueError as e:
                    print(f"  Warning: Could not parse power value from line: {line.strip()}")

        proc.terminate()
        proc.wait()  # Ensure process is fully terminated
        
    # Wait for browsing simulation to complete
    browsing_thread.join(timeout=5)
    
    print(f"powermetrics for {browser_name} finished. Collected {power_readings} readings.")

# Close all tabs in browser to clean up
def close_browser_tabs(browser_name):
    """Close all tabs in the specified browser"""
    print(f"Closing tabs in {browser_name}...")
    try:
        if browser_name == "Safari":
            close_script = '''
            tell application "Safari"
                repeat with w in windows
                    close w
                end repeat
            end tell
            '''
        elif browser_name == "Brave":
            close_script = '''
            tell application "Brave Browser"
                repeat with w in windows
                    close w
                end repeat
            end tell
            '''
        
        subprocess.run(["osascript", "-e", close_script])
        print(f"Tabs closed in {browser_name}.")
    except Exception as e:
        print(f"Error closing tabs in {browser_name}: {e}")

# Main benchmark loop
def main():
    print("=== Enhanced Browser Power Benchmark ===")
    print(f"Power monitoring duration: {POWERMETRICS_DURATION_SEC} seconds")
    print(f"Active browsing duration: {TAB_ACTIVITY_DURATION} seconds")
    
    sites = []
    with open(SITES_FILE, "r") as f:
        sites = [line.strip() for line in f if line.strip()]
    
    print(f"Will test with {len(sites)} websites: {', '.join(sites[:3])}{'...' if len(sites) > 3 else ''}")

    # Prepare CSV output
    with open(OUTPUT_FILE, "w") as f:
        f.write("Browser,Timestamp,Power(mW)\n")

    for browser in BROWSERS.keys():
        print(f"\n=== Starting {browser} test ===")
        
        # Close any existing tabs first
        close_browser_tabs(browser)
        time.sleep(2)
        
        # Open tabs with all sites
        open_tabs_in_browser(browser, sites)
        print(f"Waiting 10 seconds for {browser} to fully load all tabs...")
        time.sleep(10)  # Increased wait time for all tabs to load
        
        # Run the power measurement with active browsing
        run_powermetrics(browser, len(sites))
        
        # Clean up
        close_browser_tabs(browser)
        
        print(f"=== Finished {browser} test ===")
        if browser != list(BROWSERS.keys())[-1]:  # Don't wait after the last browser
            print("Waiting 15 seconds before next browser...")
            time.sleep(15)

    print("\n=== Benchmark complete! ===")
    print(f"Results saved to {OUTPUT_FILE}")
    print("The browser tabs were actively used during testing for more realistic power measurements.")

if __name__ == "__main__":
    main()