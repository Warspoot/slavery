#!/usr/bin/env python3
"""Helper tool to find the game window coordinates for search_region."""

import pyautogui
import time
from PIL import Image, ImageDraw, ImageFont


def get_mouse_position():
    """Get current mouse position."""
    return pyautogui.position()


def draw_crosshair(img, x, y, label):
    """Draw crosshair and label on image."""
    draw = ImageDraw.Draw(img)

    # Draw crosshair
    size = 20
    draw.line([(x - size, y), (x + size, y)], fill='red', width=2)
    draw.line([(x, y - size), (x, y + size)], fill='red', width=2)
    draw.ellipse([(x - 3, y - 3), (x + 3, y + 3)], fill='red')

    # Draw label
    draw.text((x + 10, y - 10), label, fill='red')


def main():
    """Interactive tool to find play area coordinates."""
    print("=" * 70)
    print("FIND PLAY AREA - Interactive Coordinate Finder")
    print("=" * 70)
    print()
    print("This tool helps you find the coordinates for your game window.")
    print()
    print("Instructions:")
    print("1. Position your game window where you want it")
    print("2. Move your mouse to the TOP-LEFT corner of the game window")
    print("3. Press Enter when ready")
    print()

    input("Press Enter when mouse is at TOP-LEFT corner... ")
    time.sleep(0.5)

    top_left = get_mouse_position()
    print(f"✓ Top-left corner: {top_left}")
    print()

    print("Now move your mouse to the BOTTOM-RIGHT corner of the game window")
    print("(Include the entire game area you want to monitor)")
    print()

    input("Press Enter when mouse is at BOTTOM-RIGHT corner... ")
    time.sleep(0.5)

    bottom_right = get_mouse_position()
    print(f"✓ Bottom-right corner: {bottom_right}")
    print()

    # Calculate region
    x = top_left[0]
    y = top_left[1]
    width = bottom_right[0] - top_left[0]
    height = bottom_right[1] - top_left[1]

    print("=" * 70)
    print("RESULTS")
    print("=" * 70)
    print()
    print(f"Top-left:     ({x}, {y})")
    print(f"Bottom-right: ({bottom_right[0]}, {bottom_right[1]})")
    print(f"Width:        {width}px")
    print(f"Height:       {height}px")
    print()
    print("Add this to your config.yaml:")
    print()
    print(f"search_region: [{x}, {y}, {width}, {height}]")
    print()

    # Take a screenshot to verify
    print("Taking a test screenshot of this region...")
    time.sleep(1)

    try:
        screenshot = pyautogui.screenshot(region=(x, y, width, height))

        # Draw markers on full screenshot
        full_screenshot = pyautogui.screenshot()
        draw_crosshair(full_screenshot, x, y, "TOP-LEFT")
        draw_crosshair(full_screenshot, bottom_right[0], bottom_right[1], "BOTTOM-RIGHT")

        # Draw rectangle
        draw = ImageDraw.Draw(full_screenshot)
        draw.rectangle([x, y, bottom_right[0], bottom_right[1]], outline='red', width=3)

        # Save screenshots
        screenshot.save("play_area_cropped.png")
        full_screenshot.save("play_area_fullscreen.png")

        print("✓ Saved test screenshots:")
        print("  - play_area_cropped.png (the game area only)")
        print("  - play_area_fullscreen.png (full screen with markers)")
        print()
        print("Open these images to verify the region is correct!")

    except Exception as e:
        print(f"⚠️  Could not save screenshot: {e}")

    print()
    print("=" * 70)
    print("QUICK SETUP")
    print("=" * 70)
    print()
    print("Copy this line to your config.yaml:")
    print()
    print(f"search_region: [{x}, {y}, {width}, {height}]")
    print()

    # Offer to update config automatically
    try:
        choice = input("Update config.yaml automatically? (y/n): ").strip().lower()
        if choice == 'y':
            import yaml
            from pathlib import Path

            config_path = Path("config.yaml")
            if config_path.exists():
                with open(config_path, 'r') as f:
                    config = yaml.safe_load(f)

                config['search_region'] = [x, y, width, height]

                with open(config_path, 'w') as f:
                    yaml.dump(config, f, default_flow_style=False, sort_keys=False)

                print("✓ config.yaml updated!")
                print()
                print("You can now run:")
                print("  python test_automation.py")
                print("  python umamusume_autoplay.py --sequence")
            else:
                print("⚠️  config.yaml not found")
    except Exception as e:
        print(f"Could not update config: {e}")
        print("Please update config.yaml manually")


if __name__ == "__main__":
    main()
