# Browser Power Benchmark

A comprehensive tool to measure and compare real-world power consumption of different web browsers on macOS using advanced browsing simulation patterns.

## Overview

This benchmark simulates realistic browsing behavior (tab switching, scrolling, searching, page reloading) while measuring precise power consumption using macOS's built-in `powermetrics` utility. The tool provides statistical analysis to compare browser efficiency and real-world battery life impact.

## Features

- **🤖 Advanced browser automation** using AppleScript with 6 different browsing patterns
- **⚡ Precise power monitoring** with CPU + GPU + ANE measurements every second  
- **🌐 Active browsing simulation** (tab cycling, scrolling, searching, reloading, zoom adjustments)
- **📊 Statistical analysis** with mean, min, max, standard deviation, and efficiency comparisons
- **🧹 Clean test isolation** between different browsers with automated cleanup
- **🔋 Battery life estimation** based on actual power consumption data

## Browsing Patterns

The benchmark simulates six realistic browsing behaviors:

1. **Quick Scan** - Fast scrolling through content (like skimming news)
2. **Detailed Read** - Slower, deliberate reading with small scrolls
3. **Search Mode** - Using Cmd+F to search within pages
4. **Link Navigation** - Tab key navigation between clickable elements
5. **Page Reload** - Refreshing content (common on news/social sites)
6. **Zoom Adjust** - Changing zoom levels for better readability

## Requirements

- macOS (tested on macOS 12+)
- Python 3.7+
- Safari and/or Brave Browser installed
- Administrator privileges (for `powermetrics`)
- Pandas library for report generation

## Quick Start

1. **Setup the environment**:
   ```bash
   cd BrowserBench
   python -m venv .venv
   source .venv/bin/activate
   pip install pandas
   ```

2. **Test browser automation** (optional but recommended):
   ```bash
   python test_browser_automation.py
   ```

3. **Run the benchmark** (requires sudo for power monitoring):
   ```bash
   sudo python browser_bench.py
   ```

4. **Generate detailed report**:
   ```bash
   python report.py
   ```

## Files

- `browser_bench.py` - Enhanced benchmark script with advanced browsing patterns
- `sites.txt` - List of websites to test with (customizable)
- `report.py` - Enhanced analysis and reporting tool with battery life estimates
- `test_browser_automation.py` - Browser automation test script
- `browser_power_results.csv` - Generated power measurement data (created after benchmark)

## Sample Results

Recent benchmark results show significant differences in browser efficiency:

| Browser | Average Power | Min Power | Max Power | Battery Life* | Efficiency |
|---------|---------------|-----------|-----------|---------------|------------|
| Brave   | 743 mW        | 41 mW     | 8,293 mW  | ~67 hours     | 45% better |
| Safari  | 1,356 mW      | 44 mW     | 10,551 mW | ~37 hours     | Baseline   |

*Based on 50Wh battery capacity during active browsing

## Configuration

Customize the benchmark by editing `browser_bench.py`:

```python
# Test duration settings
POWERMETRICS_DURATION_SEC = 120  # Total monitoring time
TAB_ACTIVITY_DURATION = 90       # Active browsing time

# Browser configuration
BROWSERS = {
    "Safari": "safari",
    "Brave": "brave-browser",
    # Add more browsers here
}

# Browsing patterns (automatically rotated)
BROWSING_PATTERNS = [
    "quick_scan", "detailed_read", "search_mode",
    "link_navigation", "reload_page", "zoom_adjust"
]
```

Customize test websites by editing `sites.txt` (one URL per line).

## How It Works

1. **🌐 Opens multiple tabs** with real websites from `sites.txt`
2. **🎭 Simulates realistic browsing** using 6 different behavioral patterns
3. **📏 Monitors power consumption** every second using `powermetrics`
4. **📈 Collects statistical data** over configurable test periods
5. **🧮 Generates comparative analysis** with efficiency calculations and battery estimates
6. **🧹 Automatically cleans up** browser state between tests

## Technical Implementation

- **AppleScript Integration**: Native browser control for realistic automation
- **Concurrent Processing**: Browsing simulation runs parallel to power monitoring
- **Pattern Rotation**: Ensures variety with scheduled and random pattern selection
- **Robust Error Handling**: Graceful handling of automation and measurement errors
- **Real-time Data Logging**: CSV format with timestamps for detailed analysis

## Adding New Browsers

1. Add browser entry to the `BROWSERS` dictionary:
   ```python
   BROWSERS = {
       "Safari": "safari",
       "Brave": "brave-browser", 
       "Chrome": "google-chrome",  # Example
       "Firefox": "firefox"        # Example
   }
   ```

2. Update the AppleScript process names in the browsing behavior functions if needed.

## Troubleshooting

- **Permission Issues**: Ensure you run with `sudo` for powermetrics access
- **Browser Automation**: Test with `python test_browser_automation.py` first
- **Empty Results**: Check that browsers are installed and accessible
- **High CPU Usage**: Normal during testing due to active browsing simulation

## Real-World Impact

The benchmark results show that browser choice can significantly impact battery life:

- **45% power difference** between most and least efficient browsers
- **~30 hour difference** in battery life for typical usage
- **Consistent patterns** across different website types and usage scenarios

This data helps users make informed decisions about browser choice based on their priorities (battery life vs. features).

## License

MIT License - Feel free to use and modify for your own browser testing needs.

---

*Built with ❤️ for the macOS community. Contributions and improvements welcome!*
