#!/usr/bin/env python3
"""Diagnostic script to identify screenshot issues."""

import sys
import os

print("=" * 70)
print("SCREENSHOT DIAGNOSTICS")
print("=" * 70)
print()

# 1. Check session type
print("1. Session Type:")
session_type = os.environ.get('XDG_SESSION_TYPE', 'unknown')
print(f"   XDG_SESSION_TYPE: {session_type}")
display = os.environ.get('DISPLAY', 'not set')
print(f"   DISPLAY: {display}")
print()

# 2. Check Python dependencies
print("2. Python Dependencies:")
try:
    import PIL
    print(f"   ✓ PIL/Pillow: {PIL.__version__}")
except ImportError as e:
    print(f"   ✗ PIL/Pillow: NOT INSTALLED - {e}")

try:
    import pyautogui
    print(f"   ✓ PyAutoGUI: {pyautogui.__version__}")
except ImportError as e:
    print(f"   ✗ PyAutoGUI: NOT INSTALLED - {e}")

try:
    import Xlib
    print(f"   ✓ python-xlib: installed")
except ImportError as e:
    print(f"   ✗ python-xlib: NOT INSTALLED - {e}")

print()

# 3. Test PyAutoGUI screenshot methods
print("3. Testing PyAutoGUI Screenshot Methods:")
print()

try:
    import pyautogui

    # Method 1: Try default screenshot
    print("   Method 1: Default pyautogui.screenshot()")
    try:
        screenshot = pyautogui.screenshot()
        print(f"   ✓ SUCCESS - Size: {screenshot.size}")
    except Exception as e:
        print(f"   ✗ FAILED: {e}")
    print()

    # Method 2: Try with region
    print("   Method 2: Screenshot with region (100x100 at 0,0)")
    try:
        screenshot = pyautogui.screenshot(region=(0, 0, 100, 100))
        print(f"   ✓ SUCCESS - Size: {screenshot.size}")
    except Exception as e:
        print(f"   ✗ FAILED: {e}")
    print()

    # Method 3: Try PIL ImageGrab directly
    print("   Method 3: PIL ImageGrab.grab() directly")
    try:
        from PIL import ImageGrab
        screenshot = ImageGrab.grab()
        print(f"   ✓ SUCCESS - Size: {screenshot.size}")
    except Exception as e:
        print(f"   ✗ FAILED: {e}")
    print()

except ImportError:
    print("   ✗ Cannot test - PyAutoGUI not installed")
    print()

# 4. Check for screenshot tools
print("4. Available Screenshot Tools:")
import subprocess

tools = {
    'scrot': 'scrot --version',
    'gnome-screenshot': 'gnome-screenshot --version',
    'imagemagick': 'convert --version',
    'grim': 'grim -h',
}

for tool, cmd in tools.items():
    try:
        result = subprocess.run(cmd.split(), capture_output=True, timeout=2)
        if result.returncode == 0 or 'usage' in result.stdout.decode().lower() or 'usage' in result.stderr.decode().lower():
            print(f"   ✓ {tool}: installed")
        else:
            print(f"   ✗ {tool}: not installed")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print(f"   ✗ {tool}: not installed")

print()

# 5. Recommendations
print("=" * 70)
print("RECOMMENDATIONS:")
print("=" * 70)

if session_type != 'x11':
    print("⚠️  You are NOT on X11! Current session: " + session_type)
    print("   Switch to X11 session at login screen")
    print()

if display == 'not set':
    print("⚠️  DISPLAY environment variable not set!")
    print("   Run: export DISPLAY=:0")
    print()

# Check if scrot is missing
try:
    subprocess.run(['scrot', '--version'], capture_output=True, timeout=2)
except FileNotFoundError:
    print("⚠️  scrot is NOT installed (recommended for KDE Plasma)")
    print("   Install: sudo pacman -S scrot")
    print()

print("If all checks pass but screenshots still fail:")
print("1. Make sure you're logged into X11 session (not Wayland)")
print("2. Install scrot: sudo pacman -S scrot")
print("3. Reinstall requirements: pip install -r requirements.txt")
print("4. Try setting: export DISPLAY=:0")
print()
