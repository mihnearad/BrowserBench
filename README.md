# Browser Power Benchmark

A comprehensive tool to measure and compare real-world power consumption of different web browsers on macOS.

## Overview

This benchmark simulates browsing behavior (tab switching, scrolling) while measuring  power consumption using macOS's built-in `powermetrics` utility. The tool provides analysis to compare browser efficiency and battery life impact.

## Features

- **Realistic browser automation** using AppleScript
- **Precise power monitoring** with CPU + GPU measurements
- **Active browsing simulation** (tab cycling and scrolling)
- **Statistical analysis** with mean, min, max, and standard deviation
- **Clean test isolation** between different browsers

## Requirements

- macOS (tested on recent versions)
- Python 3.7+
- Safari and/or Brave Browser installed
- Administrator privileges (for `powermetrics`)

## Quick Start

1. **Clone and setup**:
   ```bash
   cd BrowserBench
   python -m venv .venv
   source .venv/bin/activate
   ```

2. **Run the benchmark** (requires sudo for power monitoring):
   ```bash
   sudo python browser_bench.py
   ```

3. **Generate report**:
   ```bash
   python report.py
   ```

## Files

- `browser_bench.py` - Main benchmark script
- `sites.txt` - List of websites to test with
- `report.py` - Analysis and reporting tool
- `test_browser_automation.py` - Browser automation test script
- `browser_power_results.csv` - Generated power measurement data

## Sample Results

| Browser | Average Power | Battery Life* |
|---------|---------------|---------------|
| Brave   | 743 mW        | ~67 hours     |
| Safari  | 1,356 mW      | ~37 hours     |

*Based on 50Wh battery capacity

## Configuration

Edit `browser_bench.py` to customize:
- Test duration (`POWERMETRICS_DURATION_SEC`)
- Active browsing time (`TAB_ACTIVITY_DURATION`)
- Target websites (`sites.txt`)
- Additional browsers (`BROWSERS` dictionary)

## How It Works

1. **Opens multiple tabs** with real websites
2. **Simulates active browsing** by cycling through tabs and scrolling
3. **Monitors power consumption** every second using `powermetrics`
4. **Collects statistical data** over 2-minute test periods
5. **Generates comparative analysis** between browsers

## Technical Details

- Uses AppleScript for native browser control
- Concurrent power monitoring and browsing simulation
- Real-time CSV data logging
- Automated cleanup between tests

## Adding New Browsers

Add browser entries to the `BROWSERS` dictionary in `browser_bench.py`:

```python
BROWSERS = {
    "Safari": "safari",
    "Brave": "brave-browser",
    "Chrome": "google-chrome"  # Example
}
```

Then implement the corresponding AppleScript commands in the automation functions.

## License

MIT License - Feel free to use and modify for your own browser testing needs.
