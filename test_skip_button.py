#!/usr/bin/env python3
"""Test finding the skip/fast-forward button."""

import yaml
from image_utils import ImageMatcher, take_screenshot
from pathlib import Path


def main():
    """Test skip button detection."""

    print("=" * 70)
    print("SKIP/FAST-FORWARD BUTTON TEST")
    print("=" * 70)
    print()
    print("Make sure the game is showing a race with the skip button visible!")
    print("Waiting 3 seconds...")
    print()

    import time
    time.sleep(3)

    # Load config
    with open("config.yaml", 'r') as f:
        config = yaml.safe_load(f)

    confidence = config.get('confidence_threshold', 0.8)
    search_region = config.get('search_region')

    if search_region and len(search_region) == 4:
        search_region = tuple(search_region)
        print(f"Using search region: {search_region}")
    else:
        search_region = None
        print("Using full screen")

    print(f"Confidence threshold: {confidence}")
    print()

    # Try different confidence levels
    for conf in [confidence, 0.7, 0.6, 0.5]:
        print(f"\nTrying confidence: {conf}")
        matcher = ImageMatcher(confidence=conf)

        result = matcher.find_on_screen(
            "templates/fast_forward.png",
            region=search_region
        )

        if result:
            x, y, w, h = result
            center_x = x + w // 2
            center_y = y + h // 2
            print(f"  ✓ FOUND at ({x}, {y})")
            print(f"    Size: {w}x{h}")
            print(f"    Center: ({center_x}, {center_y})")
            print(f"    Would click here!")
            break
        else:
            print(f"  ✗ Not found")

    if not result:
        print()
        print("=" * 70)
        print("TROUBLESHOOTING")
        print("=" * 70)
        print()
        print("Button not found with any confidence level. Try:")
        print()
        print("1. Make sure the skip button is actually visible on screen")
        print("2. Take a screenshot during a race:")
        print("   python -c \"from image_utils import take_screenshot; take_screenshot().save('race_screen.png')\"")
        print()
        print("3. Check if the button looks different than the template")
        print("4. You may need to recrop just the white circle button")
        print("   (without the green background)")
    else:
        print()
        print(f"✓ Button found with confidence {conf}!")
        print()
        print("Update config.yaml:")
        print(f"  confidence_threshold: {conf}")


if __name__ == "__main__":
    main()
