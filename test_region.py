#!/usr/bin/env python3
"""Test and visualize the search region."""

import yaml
from pathlib import Path
from image_utils import take_screenshot
from PIL import Image, ImageDraw


def main():
    """Test the configured search region."""

    print("=" * 70)
    print("SEARCH REGION TEST")
    print("=" * 70)
    print()

    # Load config
    config_path = Path("config.yaml")
    if not config_path.exists():
        print("❌ config.yaml not found!")
        return

    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    search_region = config.get('search_region')

    if not search_region:
        print("ℹ️  search_region is set to null (full screen mode)")
        print()
        print("Taking full screen screenshot...")
        try:
            screenshot = take_screenshot()
            screenshot.save("test_region_fullscreen.png")
            print(f"✓ Saved: test_region_fullscreen.png")
            print(f"  Size: {screenshot.size[0]}x{screenshot.size[1]} pixels")
        except Exception as e:
            print(f"❌ Error: {e}")
        return

    # Parse region
    if len(search_region) != 4:
        print(f"❌ Invalid search_region format: {search_region}")
        print("   Expected: [x, y, width, height]")
        return

    x, y, width, height = search_region

    print(f"Configured search region:")
    print(f"  Position: ({x}, {y})")
    print(f"  Size: {width}x{height} pixels")
    print()

    # Take screenshots
    print("Taking screenshots...")
    print()

    try:
        # Full screen with region marked
        print("1. Full screen with region marked...")
        full_screenshot = take_screenshot()
        draw = ImageDraw.Draw(full_screenshot)

        # Draw rectangle showing the region
        draw.rectangle([x, y, x + width, y + height], outline='red', width=5)

        # Draw corner markers
        marker_size = 20
        draw.line([(x, y), (x + marker_size, y)], fill='red', width=3)
        draw.line([(x, y), (x, y + marker_size)], fill='red', width=3)
        draw.text((x + 10, y + 10), "TOP-LEFT", fill='red')

        draw.line([(x + width, y + height), (x + width - marker_size, y + height)], fill='red', width=3)
        draw.line([(x + width, y + height), (x + width, y + height - marker_size)], fill='red', width=3)
        draw.text((x + width - 100, y + height - 30), "BOTTOM-RIGHT", fill='red')

        full_screenshot.save("test_region_marked.png")
        print(f"   ✓ Saved: test_region_marked.png")
        print(f"     Full screen size: {full_screenshot.size[0]}x{full_screenshot.size[1]}")

        # Cropped region only
        print()
        print("2. Cropped region (what automation sees)...")
        cropped = take_screenshot(region=(x, y, width, height))
        cropped.save("test_region_cropped.png")
        print(f"   ✓ Saved: test_region_cropped.png")
        print(f"     Region size: {cropped.size[0]}x{cropped.size[1]}")

        print()
        print("=" * 70)
        print("VALIDATION")
        print("=" * 70)
        print()

        # Check if region is reasonable
        issues = []

        if width < 800:
            issues.append(f"⚠️  Width ({width}px) seems small for a game window")

        if height < 600:
            issues.append(f"⚠️  Height ({height}px) seems small for a game window")

        if x + width > full_screenshot.size[0]:
            issues.append(f"❌ Region extends beyond screen width!")

        if y + height > full_screenshot.size[1]:
            issues.append(f"❌ Region extends beyond screen height!")

        if issues:
            print("Issues found:")
            for issue in issues:
                print(f"  {issue}")
            print()
            print("Recommendation:")
            print("  Run: python find_play_area_simple.py")
            print("  to set the correct region")
        else:
            print("✓ Region looks good!")
            print()
            print("Next steps:")
            print("  1. Open test_region_marked.png - verify red box is around game")
            print("  2. Open test_region_cropped.png - verify you can see the game")
            print("  3. Run: python test_automation.py")

    except Exception as e:
        print(f"❌ Error taking screenshot: {e}")
        import traceback
        traceback.print_exc()

    print()
    print("=" * 70)


if __name__ == "__main__":
    main()
