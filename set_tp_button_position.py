#!/usr/bin/env python3
"""Helper tool to set the TP recovery button position."""

import yaml
import pyautogui
from pathlib import Path


def main():
    """Interactive tool to set TP recovery button coordinates."""

    print("=" * 70)
    print("TP RECOVERY BUTTON POSITION HELPER")
    print("=" * 70)
    print()
    print("This tool will help you set the exact position of the '使う' button")
    print("for the SECOND item (タフネス30 bottle) in the TP recovery screen.")
    print()

    # Load config
    config_path = Path("config.yaml")
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    search_region = config.get('search_region')
    if not search_region or len(search_region) != 4:
        print("ERROR: search_region not properly configured in config.yaml")
        return

    region_x, region_y, region_w, region_h = search_region

    print(f"Current search region: {search_region}")
    print(f"  X: {region_x}, Y: {region_y}")
    print(f"  Width: {region_w}, Height: {region_h}")
    print()

    current_x = config.get('tp_recovery_button_x', 0)
    current_y = config.get('tp_recovery_second_row_y', 0)

    print(f"Current button offsets:")
    print(f"  X offset: {current_x}")
    print(f"  Y offset: {current_y}")
    print(f"  Absolute position: ({region_x + current_x}, {region_y + current_y})")
    print()

    print("=" * 70)
    print("INSTRUCTIONS:")
    print("=" * 70)
    print()
    print("1. Open the TP recovery screen in the game")
    print("2. Make sure the TP回復 items list is visible")
    print("3. When ready, press ENTER to start positioning")
    print()
    input("Press ENTER to continue...")
    print()

    print("Now, move your mouse to the CENTER of the '使う' button")
    print("for the SECOND item (タフネス30 bottle).")
    print()
    print("You have 5 seconds to position your mouse...")
    print()

    import time
    for i in range(5, 0, -1):
        print(f"  {i}...")
        time.sleep(1)

    # Get mouse position
    mouse_x, mouse_y = pyautogui.position()
    print()
    print(f"✓ Captured mouse position: ({mouse_x}, {mouse_y})")
    print()

    # Calculate offsets relative to search region
    offset_x = mouse_x - region_x
    offset_y = mouse_y - region_y

    print(f"Calculated offsets from search region:")
    print(f"  X offset: {offset_x}")
    print(f"  Y offset: {offset_y}")
    print()

    # Validate offsets are within region
    if offset_x < 0 or offset_x > region_w:
        print(f"⚠️  WARNING: X offset ({offset_x}) is outside the search region width ({region_w})")
        print("   Make sure you clicked within the game window!")

    if offset_y < 0 or offset_y > region_h:
        print(f"⚠️  WARNING: Y offset ({offset_y}) is outside the search region height ({region_h})")
        print("   Make sure you clicked within the game window!")

    print()
    print("=" * 70)
    response = input("Save these coordinates to config.yaml? (y/n): ").strip().lower()

    if response == 'y':
        # Update config
        config['tp_recovery_button_x'] = offset_x
        config['tp_recovery_second_row_y'] = offset_y

        # Save config
        with open(config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)

        print()
        print("✓ Configuration saved!")
        print()
        print(f"Updated values in config.yaml:")
        print(f"  tp_recovery_button_x: {offset_x}")
        print(f"  tp_recovery_second_row_y: {offset_y}")
        print()
        print("The automation will now click at this position when selecting the bottle.")
    else:
        print()
        print("Coordinates NOT saved. No changes made.")

    print()


if __name__ == "__main__":
    main()
