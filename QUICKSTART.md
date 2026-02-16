# Quick Start Guide

## Step-by-Step Setup

### 1. Setup Virtual Environment

```bash
# Run the setup script
./setup.sh

# Or manually create venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Extract Button Templates

```bash
python extract_templates.py
```

You should see output like:
```
Extracting button templates from example screenshots...

Saved template: templates/home_育成_button.png (60x20)
Saved template: templates/support_決定_button.png (60x14)
...

Extracted 23 templates to templates/
```

### 3. (Optional) Define Play Area

If you want to limit the automation to only search within your game window (highly recommended):

```bash
python find_play_area.py
```

This interactive tool will:
1. Ask you to move your mouse to the **top-left** corner of your game window
2. Ask you to move your mouse to the **bottom-right** corner
3. Calculate and save the coordinates to config.yaml
4. Create test screenshots so you can verify the area

**Benefits:**
- ⚡ Faster (searches smaller area)
- 🎯 More accurate (won't match buttons from other windows)
- 💻 Better for windowed mode

### 4. Test the Setup

```bash
python test_automation.py
```

**Before running**: Open the game on your screen (don't minimize it!)

The test will:
1. ✓ Check all templates exist
2. ✓ Take a test screenshot
3. ✓ Verify safety features
4. ✓ Try to detect your current game screen
5. ✓ Test template matching

If all tests pass, you're ready to go!

### 5. Run Your First Test

#### Option A: Test with Interactive Mode

```bash
python test_automation.py
# Choose 'y' for interactive button finder
# This lets you test finding specific buttons
```

Steps:
1. Run the test script
2. Choose a template to search for (e.g., home_育成_button.png)
3. Switch to your game window within 3 seconds
4. The script will tell you if it found the button and where

#### Option B: Dry Run (Safe Testing)

Open the game to the **home screen** and run:

```bash
python umamusume_autoplay.py --sequence
```

Watch what it does:
- Does it find the buttons?
- Does it click in the right places?
- Are the timings good?

**Safety tip**: Keep your mouse near the top-left corner of the screen. Moving it there will trigger the failsafe and stop automation immediately!

### 6. Run Full Automation

Once you're confident it works:

**For starting a single training run:**
```bash
python umamusume_autoplay.py --sequence
```

**For continuous automation (hands-free):**
```bash
python umamusume_autoplay.py --continuous
```

## Troubleshooting Your First Run

### "Templates not found" error
```bash
# Make sure you extracted templates
python extract_templates.py

# Check they exist
ls -la templates/
```

### "Button not found" warnings

1. **Lower the confidence threshold**

Edit [config.yaml](config.yaml):
```yaml
confidence_threshold: 0.7  # Try lower values like 0.6 or 0.5
```

2. **Check your screen resolution**

The templates were extracted from specific screenshots. If your game resolution is different, the buttons might look different.

3. **Enable debug mode**

Edit [config.yaml](config.yaml):
```yaml
debug: true
```

Run automation again and check the `debug_*.png` screenshots to see what the tool is seeing.

### Clicks are in wrong positions

Your screen resolution might be different. You may need to:
1. Re-extract templates from screenshots taken at YOUR resolution
2. Or use the `search_region` setting to limit where it searches

### It's too fast/slow

Edit [config.yaml](config.yaml):
```yaml
action_delay: 2.0  # Increase for slower (default: 1.0)
retry_delay: 1.5   # Time between retries
```

## What to Expect

### Sequence Mode
```
Starting on home screen...
1. Clicks 育成 button → Support card screen
2. Clicks 決定 button → Training prep screen
3. Clicks 育成開始 button → TP recovery (if needed)
4. Handles TP recovery → Event skip settings
5. Selects "すべてのイベントを短縮" → Clicks 決定
6. Training begins!
```

Total time: ~30-60 seconds depending on which screens appear

### Continuous Mode
```
Monitors screen continuously...
- Handles any recognized screen automatically
- Clicks fast forward during races
- Handles race completion dialogs
- Manages TP recovery
- Keeps running until you press Ctrl+C
```

## Tips for Best Results

1. **Run the game in windowed mode** (easier to monitor)
2. **Don't minimize or cover the game window** (the tool can't see it)
3. **Start with sequence mode** to test before going fully automated
4. **Keep debug mode off** during normal use (saves disk space)
5. **Monitor the first few runs** to make sure it's working correctly

## Getting Help

If something doesn't work:

1. Check [README.md](README.md) troubleshooting section
2. Run `python test_automation.py` to diagnose issues
3. Enable debug mode and check the screenshots
4. Verify templates exist: `ls -la templates/`

## Daily Usage

Once everything is working, your typical workflow:

```bash
# Activate venv (if not already active)
source venv/bin/activate

# Start continuous automation
python umamusume_autoplay.py --continuous

# Let it run while you do other things
# Press Ctrl+C when done
```

Happy automating! 🏇
