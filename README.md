# Umamusume Pretty Derby Autoplay Automation

Automates the process of starting autoplay for the Japanese version of Umamusume Pretty Derby. This tool uses image recognition to detect game screens and automatically clicks the necessary buttons.

## Features

- Automatic screen detection using OpenCV template matching
- Handles the complete training workflow:
  - Event banner dismissal
  - Home screen navigation (育成 button)
  - Support card selection
  - Training preparation (育成開始)
  - My Ruler confirmation dialog
  - TP recovery confirmation
  - TP recovery item selection
  - Item quantity confirmation
  - Event skip settings (すべてのイベントを短縮)
  - Fast forward during races
  - Omakase (auto-select) menu
  - Race completion dialogs
- Two operation modes: sequence mode and continuous mode
- Configurable confidence thresholds and delays
- Debug mode with screenshot saving
- Failsafe protection (move mouse to top-left corner to stop)

## Requirements

### System Requirements (Arch Linux / KDE Plasma)
- **X11 session** (not Wayland - required for PyAutoGUI screenshots)
- **scrot** - Screenshot utility for X11
  ```bash
  sudo pacman -S scrot
  ```

### Python Requirements
- Python 3.8+
- OpenCV
- PyAutoGUI
- PIL/Pillow
- NumPy
- PyYAML
- python-xlib
- pynput

## Installation

### Quick Setup (Recommended)

Run the setup script to create a virtual environment and install dependencies:

```bash
./setup.sh
```

Or manually:

```bash
# 1. Install system dependencies (REQUIRED for screenshots)
sudo pacman -S scrot

# 2. Create virtual environment
python3 -m venv venv

# 3. Activate virtual environment
source venv/bin/activate

# 4. Install Python dependencies
pip install -r requirements.txt
```

### Important: X11 vs Wayland

This tool **requires X11** to function properly. PyAutoGUI cannot take screenshots on Wayland.

**To switch to X11 on KDE Plasma:**
1. Log out
2. At the login screen, look for a session selector (usually bottom-left)
3. Select "Plasma (X11)" instead of "Plasma (Wayland)"
4. Log in

**To verify you're on X11:**
```bash
echo $XDG_SESSION_TYPE  # Should output: x11
```

### Extract Templates

Extract button templates from example screenshots:

```bash
python extract_templates.py
```

This will create a `templates/` directory with all the button images needed for automation.

### Testing

Before running the full automation, test that everything works:

```bash
python test_automation.py
```

This will:
- Check if all templates were extracted correctly
- Test screenshot capture
- Test screen detection with your game
- Test template matching
- Provide an interactive button finder

**Important**: Make sure the game is visible (not minimized) when running tests!

## Configuration

Edit [config.yaml](config.yaml) to customize the automation behavior:

```yaml
# Confidence threshold for image matching (0.0 to 1.0)
confidence_threshold: 0.8

# Delay between actions (seconds)
action_delay: 1.0

# Screenshot delay (seconds)
screenshot_delay: 0.5

# Maximum retries for finding a button
max_retries: 5

# Retry delay (seconds)
retry_delay: 2.0

# Enable debug mode (saves screenshots)
debug: false

# Screen region to search (null for full screen)
# Format: [x, y, width, height]
search_region: null

# TP Recovery settings
auto_recover_tp: false  # Set to true to automatically use TP bottle when prompted
```

### Key Settings

- **confidence_threshold**: How closely the template must match (0.8 = 80% match required)
- **action_delay**: Wait time after each click
- **max_retries**: How many times to retry finding a button before giving up
- **debug**: Set to `true` to save debug screenshots
- **search_region**: Limit searching to a specific screen area (useful if running in a window)
- **auto_recover_tp**: Set to `true` to automatically use TP bottles when prompted. When `false`, the automation will click cancel/skip TP recovery dialogs (default: `false`)

## Usage

### Sequence Mode

Runs the full automation sequence once, handling all screens in order to start a training run:

```bash
python umamusume_autoplay.py --sequence
```

This mode follows the complete workflow:
1. Dismisses event banner (if present)
2. Clicks 育成 (training) button on home screen
3. Confirms support card selection (if needed)
4. Clicks 育成開始 (start training) on prep screen
5. Handles My Ruler confirmation (if present)
6. Handles TP recovery if needed
7. Sets event skip to "すべてのイベントを短縮" (skip all events)
8. Training begins with autoplay enabled!

### Continuous Mode

Continuously monitors the screen and handles any recognized screens automatically:

```bash
python umamusume_autoplay.py --continuous
```

This mode:
- Keeps running until stopped (Ctrl+C)
- Automatically detects and handles screens as they appear
- Clicks fast forward during races
- Handles race completion dialogs
- Manages TP recovery automatically
- Useful for fully automated training sessions

**Recommended for hands-free training!**

### Custom Configuration

Use a different configuration file:

```bash
python umamusume_autoplay.py --sequence --config my_config.yaml
```

## Safety Features

1. **Failsafe**: Move your mouse to the top-left corner of the screen to trigger PyAutoGUI's failsafe and stop automation
2. **Keyboard Interrupt**: Press Ctrl+C to stop the automation at any time
3. **Retry Limits**: The tool will give up after a configurable number of retries

## Project Structure

```
.
├── automation.py           # Button clicking and automation actions
├── config.yaml            # Configuration file
├── examples/              # Example screenshots (provided by you)
├── extract_templates.py   # Script to extract button templates
├── image_utils.py         # Image recognition utilities
├── README.md             # This file
├── requirements.txt      # Python dependencies
├── screen_detector.py    # Screen detection module
├── templates/            # Extracted button templates (generated)
└── umamusume_autoplay.py # Main automation script
```

## Troubleshooting

### "Failed to take screenshot" Error

This is the most common error on Linux. The issue is usually missing dependencies or running on Wayland.

**Solution:**
1. **Install scrot** (required for X11 screenshots):
   ```bash
   sudo pacman -S scrot
   ```

2. **Verify you're on X11** (not Wayland):
   ```bash
   echo $XDG_SESSION_TYPE  # Should say "x11"
   ```

3. **Switch to X11 if needed:**
   - Log out
   - At login screen, select "Plasma (X11)"
   - Log back in

4. **Reinstall Python dependencies:**
   ```bash
   source venv/bin/activate
   pip install --force-reinstall pillow pyautogui python-xlib
   ```

5. **Test screenshots:**
   ```bash
   python3 test_basic_screenshot.py
   ```

### Buttons Not Being Found

1. **Lower the confidence threshold** in config.yaml (try 0.7 or 0.6)
2. **Enable debug mode** to see what the tool is seeing:
   ```yaml
   debug: true
   ```
3. **Check template images** in the `templates/` directory to ensure they extracted correctly
4. **Verify screen resolution** - templates are extracted from specific screenshots and may not match if your game resolution is different

### Clicking Wrong Locations

1. **Increase confidence threshold** to be more strict (try 0.85 or 0.9)
2. **Use search_region** to limit where the tool looks:
   ```yaml
   search_region: [100, 100, 800, 600]  # [x, y, width, height]
   ```

### Too Fast/Too Slow

Adjust timing in config.yaml:
```yaml
action_delay: 1.5  # Increase for slower automation
retry_delay: 1.0   # Decrease for faster retries
```

## Complete Workflow

The automation handles the entire process from home screen to autoplay:

```
Home Screen → Support Cards → Training Prep → (TP Recovery) → Event Skip → Training Starts
```

During training, continuous mode also handles:
- Fast forward button during races
- Race completion dialogs
- Omakase (auto-select) menus
- Additional TP recovery prompts

## How It Works

1. **Template Extraction**: Button images are extracted from your example screenshots
2. **Screen Detection**: OpenCV's template matching finds buttons on screen in real-time
3. **Screen Recognition**: Multiple templates identify which screen is currently showing
4. **Automation Flow**: The tool clicks buttons in the correct sequence based on detected screens
5. **State Management**: Waits for each screen before proceeding to the next step

## Limitations

- Requires the game to be visible on screen (cannot be minimized or covered)
- Screen resolution should match the example screenshots (or adjust confidence threshold)
- Only handles the screens shown in examples folder
- Does not handle unexpected popups, errors, or new event types
- Assumes you have sufficient TP items for recovery

## Advanced Usage

### Custom Screen Region (Play Area)

If running the game in a window, you can limit the search to just that area for better performance and accuracy.

**Easy way (recommended):**

```bash
python find_play_area.py
```

This interactive tool helps you find the coordinates and updates config.yaml automatically.

**Manual way:**

Edit config.yaml:
```yaml
# Format: [x, y, width, height]
search_region: [100, 50, 800, 600]
```

**Programmatic way:**

```python
from umamusume_autoplay import UmamusumeAutoplay

autoplay = UmamusumeAutoplay("config.yaml")
# Override search region
autoplay.search_region = (100, 100, 800, 600)  # x, y, width, height
autoplay.run_automation_sequence()
```

### Adding New Screens

1. Take a screenshot of the new screen
2. Extract button templates using OpenCV or an image editor
3. Add templates to `templates/` directory
4. Add screen detection to [screen_detector.py](screen_detector.py)
5. Add handler method to [umamusume_autoplay.py](umamusume_autoplay.py)
6. Update the sequence in `run_automation_sequence()`

## License

This tool is for educational purposes. Use responsibly and in accordance with the game's terms of service.
