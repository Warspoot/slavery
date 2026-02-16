# Wayland Setup Guide

PyAutoGUI has limited Wayland support. This guide helps you get screenshots working on Wayland.

## Quick Fix (Recommended)

Install `grim` - a native Wayland screenshot tool:

```bash
sudo pacman -S grim
```

The automation will automatically detect Wayland and use `grim` instead of PyAutoGUI for screenshots.

## Test Wayland Support

```bash
# Check if you're on Wayland
echo $XDG_SESSION_TYPE  # Should output: wayland

# Test grim
python wayland_screenshot.py
```

This should create test screenshots if `grim` is working correctly.

## Alternative: Use X11 Session

For maximum compatibility, you can use an X11 session instead:

1. Log out
2. At the login screen, select "Plasma (X11)" or "GNOME on Xorg"
3. Log back in
4. Run the automation normally

## Troubleshooting

### "grim not found" error

```bash
sudo pacman -S grim
```

### Screenshots still fail

Try running with explicit Wayland support:

```bash
# This forces the use of grim
python test_automation.py
```

### Mouse clicking not working

PyAutoGUI mouse control should work on Wayland through compatibility layers, but if it doesn't:

```bash
# Install additional tools
sudo pacman -S ydotool
```

Then you may need to modify the automation to use ydotool instead of pyautogui for clicks.

## What Gets Installed

- **grim**: Wayland-native screenshot utility
- Works with: Sway, Hyprland, and other wlroots compositors
- Also works with: KDE Plasma Wayland, GNOME Wayland (with some limitations)

## Verification

After installing grim:

```bash
# Test the wrapper
python wayland_screenshot.py

# Should see:
# ✓ grim is installed
# ✓ Saved test_wayland_full.png
# ✓ Saved test_wayland_crop.png

# Run the full test suite
python test_automation.py
```

All tests should now pass!
