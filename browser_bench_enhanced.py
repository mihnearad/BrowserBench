#!/usr/bin/env python3
"""
Enhanced Browser Power Benchmark with Advanced Browsing Simulation

This tool measures real-world power consumption of different web browsers on macOS
by simulating various realistic browsing behaviors and patterns.
"""

import subprocess
import time
import os
import random
from threading import Thread

# Configuration
BROWSERS = {
    "Safari": "safari",
    "Brave": "brave-browser"
}
POWERMETRICS_DURATION_SEC = 120  # 2 minutes of power monitoring
TAB_ACTIVITY_DURATION = 90  # 90 seconds of active browsing
SITES_FILE = "sites.txt"
OUTPUT_FILE = "browser_power_results.csv"

# Enhanced browsing patterns
BROWSING_PATTERNS = [
    "quick_scan",      # Fast scrolling through content
    "detailed_read",   # Slower, deliberate reading
    "search_mode",     # Using Cmd+F to search
    "link_navigation", # Tab navigation between links
    "reload_page",     # Refreshing content
    "zoom_adjust"      # Changing zoom levels
]

def open_tabs_in_browser(browser_name, sites):
    """Open multiple tabs with specified websites"""
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

def get_browsing_behavior(browser_name, pattern):
    """Generate AppleScript for different browsing behaviors"""
    browser_process = "Safari" if browser_name == "Safari" else "Brave Browser"
    
    behaviors = {
        "quick_scan": f'''
        tell application "System Events"
            tell process "{browser_process}"
                key code 125 using {{command down}}  -- Page Down
                delay 0.8
                key code 125 using {{command down}}  -- Page Down again
                delay 0.8
                key code 125 using {{command down}}  -- Page Down third time
                delay 0.5
                key code 126 using {{command down}}  -- Page Up
                delay 0.5
            end tell
        end tell
        ''',
        
        "detailed_read": f'''
        tell application "System Events"
            tell process "{browser_process}"
                key code 125  -- Small scroll down
                delay 2.5
                key code 125  -- Small scroll down
                delay 2.5
                key code 125  -- Small scroll down
                delay 2.0
                key code 126  -- Small scroll up
                delay 1.5
                key code 126  -- Small scroll up
                delay 1.5
            end tell
        end tell
        ''',
        
        "search_mode": f'''
        tell application "System Events"
            tell process "{browser_process}"
                key code 3 using {{command down}}  -- Cmd+F (Find)
                delay 1.0
                keystroke "news"  -- Type search term
                delay 1.0
                key code 36  -- Enter
                delay 1.0
                key code 53  -- Escape to close find
                delay 0.5
                key code 125 using {{command down}}  -- Page Down
                delay 1.5
            end tell
        end tell
        ''',
        
        "link_navigation": f'''
        tell application "System Events"
            tell process "{browser_process}"
                key code 48  -- Tab to navigate to links
                delay 0.8
                key code 48  -- Tab again
                delay 0.8
                key code 48  -- Tab again
                delay 0.8
                key code 125  -- Small scroll
                delay 1.0
                key code 48  -- Tab to more links
                delay 0.8
            end tell
        end tell
        ''',
        
        "reload_page": f'''
        tell application "System Events"
            tell process "{browser_process}"
                key code 15 using {{command down}}  -- Cmd+R (Reload)
                delay 3.0  -- Wait for page to reload
                key code 125 using {{command down}}  -- Page Down after reload
                delay 1.5
            end tell
        end tell
        ''',
        
        "zoom_adjust": f'''
        tell application "System Events"
            tell process "{browser_process}"
                key code 24 using {{command down}}  -- Cmd++ (Zoom in)
                delay 1.0
                key code 125  -- Scroll with new zoom
                delay 1.5
                key code 27 using {{command down}}  -- Cmd+- (Zoom out)
                delay 1.0
                key code 125  -- Scroll with reset zoom
                delay 1.5
            end tell
        end tell
        '''
    }
    
    return behaviors.get(pattern, behaviors["quick_scan"])

def simulate_active_browsing(browser_name, num_tabs, duration_sec):
    """Enhanced browsing simulation with multiple realistic behaviors"""
    print(f"Starting enhanced browsing simulation for {browser_name}...")
    
    start_time = time.time()
    tab_index = 1
    iteration = 0
    
    while time.time() - start_time < duration_sec:
        try:
            iteration += 1
            
            # Focus on current tab
            if browser_name == "Safari":
                focus_script = f'''
                tell application "Safari"
                    activate
                    set current tab of window 1 to tab {tab_index} of window 1
                end tell
                '''
            else:  # Brave
                focus_script = f'''
                tell application "Brave Browser"
                    activate
                    set active tab index of window 1 to {tab_index}
                end tell
                '''
            
            # Choose browsing pattern based on iteration to ensure variety
            if iteration % 8 == 0:
                pattern = "reload_page"  # Occasionally reload pages
            elif iteration % 6 == 0:
                pattern = "search_mode"  # Occasionally search
            elif iteration % 4 == 0:
                pattern = "zoom_adjust"  # Occasionally adjust zoom
            else:
                pattern = random.choice(["quick_scan", "detailed_read", "link_navigation"])
            
            # Get the behavior script
            behavior_script = get_browsing_behavior(browser_name, pattern)
            
            # Execute the scripts
            subprocess.run(["osascript", "-e", focus_script])
            time.sleep(random.uniform(0.5, 1.2))  # Variable pause after tab switch
            subprocess.run(["osascript", "-e", behavior_script])
            
            # Move to next tab
            tab_index = (tab_index % num_tabs) + 1
            
            # Variable wait time based on pattern
            wait_times = {
                "detailed_read": random.uniform(4, 7),
                "search_mode": random.uniform(3, 5),
                "reload_page": random.uniform(4, 6),
                "quick_scan": random.uniform(2, 4),
                "link_navigation": random.uniform(3, 5),
                "zoom_adjust": random.uniform(2, 4)
            }
            
            wait_time = wait_times.get(pattern, 3)
            time.sleep(wait_time)
            
            # Occasionally simulate back/forward navigation
            if random.random() < 0.1:  # 10% chance
                back_forward_script = f'''
                tell application "System Events"
                    tell process "{browser_name if browser_name == "Safari" else "Brave Browser"}"
                        key code 123 using {{command down}}  -- Cmd+Left (Back)
                        delay 1.5
                        key code 124 using {{command down}}  -- Cmd+Right (Forward)
                        delay 1.5
                    end tell
                end tell
                '''
                subprocess.run(["osascript", "-e", back_forward_script])
            
        except Exception as e:
            print(f"Error during browsing simulation: {e}")
            time.sleep(1)
    
    print(f"Enhanced browsing simulation completed for {browser_name}.")

def run_powermetrics(browser_name, num_tabs):
    """Run power monitoring while simulating browsing"""
    print(f"Running powermetrics for {browser_name}...")
    
    # Start browsing simulation in separate thread
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
                    if power_readings % 15 == 0:
                        print(f"  Collected {power_readings} power readings...")
                except ValueError as e:
                    print(f"  Warning: Could not parse power value: {line.strip()}")

        proc.terminate()
        proc.wait()
        
    browsing_thread.join(timeout=5)
    print(f"powermetrics for {browser_name} finished. Collected {power_readings} readings.")

def close_browser_tabs(browser_name):
    """Close all browser tabs and windows"""
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

def main():
    """Main benchmark execution"""
    print("=== Enhanced Browser Power Benchmark ===")
    print(f"Power monitoring: {POWERMETRICS_DURATION_SEC}s")
    print(f"Active browsing: {TAB_ACTIVITY_DURATION}s")
    print(f"Browsing patterns: {', '.join(BROWSING_PATTERNS)}")
    
    # Load test sites
    sites = []
    with open(SITES_FILE, "r") as f:
        sites = [line.strip() for line in f if line.strip()]
    
    print(f"Testing with {len(sites)} websites")

    # Initialize CSV
    with open(OUTPUT_FILE, "w") as f:
        f.write("Browser,Timestamp,Power(mW)\n")

    # Test each browser
    for browser in BROWSERS.keys():
        print(f"\n=== Starting {browser} test ===")
        
        close_browser_tabs(browser)
        time.sleep(2)
        
        open_tabs_in_browser(browser, sites)
        print(f"Waiting 12 seconds for {browser} to load content...")
        time.sleep(12)
        
        run_powermetrics(browser, len(sites))
        close_browser_tabs(browser)
        
        print(f"=== Finished {browser} test ===")
        if browser != list(BROWSERS.keys())[-1]:
            print("Waiting 15 seconds before next browser...")
            time.sleep(15)

    print("\n=== Enhanced Benchmark Complete! ===")
    print(f"Results saved to {OUTPUT_FILE}")
    print("Advanced browsing patterns were used for realistic power measurements.")

if __name__ == "__main__":
    main()
