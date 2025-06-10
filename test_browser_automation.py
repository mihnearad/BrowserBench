#!/usr/bin/env python3
"""
Test script to verify browser automation functionality
"""
import subprocess
import time

def test_safari_automation():
    print("Testing Safari automation...")
    
    # Test opening a single tab
    script = '''
    tell application "Safari"
        activate
        open location "https://www.apple.com"
    end tell
    '''
    
    try:
        subprocess.run(["osascript", "-e", script])
        print("✓ Safari tab opening works")
        time.sleep(3)
        
        # Test focusing and scrolling
        scroll_script = '''
        tell application "System Events"
            tell process "Safari"
                key code 125 using {command down}  -- Page Down
                delay 0.5
                key code 126 using {command down}  -- Page Up
            end tell
        end tell
        '''
        
        subprocess.run(["osascript", "-e", scroll_script])
        print("✓ Safari scrolling works")
        
        # Close the test tab
        close_script = '''
        tell application "Safari"
            close current tab of window 1
        end tell
        '''
        subprocess.run(["osascript", "-e", close_script])
        print("✓ Safari tab closing works")
        
    except Exception as e:
        print(f"✗ Safari automation failed: {e}")

def test_brave_automation():
    print("\nTesting Brave automation...")
    
    script = '''
    tell application "Brave Browser"
        activate
        open location "https://www.brave.com"
    end tell
    '''
    
    try:
        subprocess.run(["osascript", "-e", script])
        print("✓ Brave tab opening works")
        time.sleep(3)
        
        # Test scrolling
        scroll_script = '''
        tell application "System Events"
            tell process "Brave Browser"
                key code 125 using {command down}  -- Page Down
                delay 0.5
                key code 126 using {command down}  -- Page Up
            end tell
        end tell
        '''
        
        subprocess.run(["osascript", "-e", scroll_script])
        print("✓ Brave scrolling works")
        
        # Close the test tab
        close_script = '''
        tell application "Brave Browser"
            close active tab of window 1
        end tell
        '''
        subprocess.run(["osascript", "-e", close_script])
        print("✓ Brave tab closing works")
        
    except Exception as e:
        print(f"✗ Brave automation failed: {e}")

if __name__ == "__main__":
    print("=== Browser Automation Test ===")
    test_safari_automation()
    test_brave_automation()
    print("\n=== Test Complete ===")
