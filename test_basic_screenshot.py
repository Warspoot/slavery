#!/usr/bin/env python3
"""Simple test to verify screenshot capability."""

import sys

print("Testing basic screenshot capability...")
print()

try:
    import pyautogui
    print(f"✓ PyAutoGUI imported (version {pyautogui.__version__})")

    print("Attempting to take a screenshot...")
    screenshot = pyautogui.screenshot()

    print(f"✓ Screenshot successful!")
    print(f"  Screen size: {screenshot.size}")

    # Save it
    screenshot.save('/tmp/test_screenshot.png')
    print(f"  Saved to: /tmp/test_screenshot.png")
    print()
    print("SUCCESS! Screenshot capability is working.")

except Exception as e:
    print(f"✗ Screenshot FAILED: {e}")
    print()
    print("Possible fixes:")
    print("1. Install scrot: sudo pacman -S scrot")
    print("2. Make sure you're on X11 (not Wayland)")
    print("3. Set DISPLAY: export DISPLAY=:0")
    print("4. Reinstall Pillow: pip install --force-reinstall pillow")
    sys.exit(1)
