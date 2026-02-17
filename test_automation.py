#!/usr/bin/env python3
"""Test script to verify automation setup and template matching."""

import sys
from pathlib import Path
import pyautogui
from image_utils import ImageMatcher, save_screenshot
from screen_detector import ScreenDetector, GameScreen


def test_templates_exist():
    """Check if all required templates exist."""
    print("=" * 60)
    print("TEST 1: Checking if templates exist")
    print("=" * 60)

    templates_dir = Path("templates")
    if not templates_dir.exists():
        print("❌ Templates directory not found!")
        print("   Run: python extract_templates.py")
        return False

    required_templates = [
        "home_育成_button.png",
        "support_決定_button.png",
        "training_育成開始_button.png",
        "ketteyi_button.png",
        "kaifuku_button.png",
        "tsukau_button.png",
        "ok_button.png",
        "skip_all_events.png",
        "fast_forward.png",
        "tojiru_button.png",
        "omakase_button.png",
    ]

    missing = []
    for template in required_templates:
        if not (templates_dir / template).exists():
            missing.append(template)
            print(f"❌ Missing: {template}")
        else:
            print(f"✓ Found: {template}")

    if missing:
        print(f"\n❌ Missing {len(missing)} templates. Run: python extract_templates.py")
        return False
    else:
        print(f"\n✓ All {len(required_templates)} required templates found!")
        return True


def test_screenshot():
    """Test taking a screenshot."""
    print("\n" + "=" * 60)
    print("TEST 2: Taking a test screenshot")
    print("=" * 60)

    try:
        save_screenshot("test_screenshot.png")
        print("✓ Screenshot saved as test_screenshot.png")
        print("  Open this file to verify your screen is captured correctly")
        return True
    except Exception as e:
        print(f"❌ Failed to take screenshot: {e}")
        return False


def test_screen_detection():
    """Test detecting the current screen."""
    print("\n" + "=" * 60)
    print("TEST 3: Detecting current screen")
    print("=" * 60)
    print("Make sure the game is visible on screen!")
    print("Waiting 3 seconds for you to switch to the game window...")

    import time
    time.sleep(3)

    try:
        detector = ScreenDetector(confidence=0.7)  # Lower confidence for testing
        current_screen = detector.detect_current_screen()

        print(f"\nDetected screen: {current_screen.value}")

        if current_screen == GameScreen.UNKNOWN:
            print("⚠️  Unknown screen detected")
            print("   This is normal if you're not on a recognized game screen")
            print("   Try navigating to the home screen or training prep screen")
        else:
            print(f"✓ Successfully detected: {current_screen.value}")

        return True
    except Exception as e:
        print(f"❌ Error during detection: {e}")
        return False


def test_template_matching():
    """Test if a specific template can be found on screen."""
    print("\n" + "=" * 60)
    print("TEST 4: Template matching test")
    print("=" * 60)
    print("This will search for visible buttons on your current screen")
    print("Make sure the game is visible!")
    print("Waiting 3 seconds...")

    import time
    time.sleep(3)

    # Test with several common templates
    test_templates = [
        "home_育成_button.png",
        "training_育成開始_button.png",
        "ketteyi_button.png",
        "skip_all_events.png",
    ]

    matcher = ImageMatcher(confidence=0.7)
    found_any = False

    for template in test_templates:
        template_path = f"templates/{template}"
        if not Path(template_path).exists():
            continue

        result = matcher.find_on_screen(template_path)
        if result:
            x, y, w, h = result
            print(f"✓ Found {template} at position ({x}, {y})")
            found_any = True
        else:
            print(f"  {template} not visible on current screen")

    if not found_any:
        print("\n⚠️  No templates matched current screen")
        print("   This is normal if you're not on a game screen with these buttons")
    else:
        print("\n✓ Template matching is working!")

    return True


def test_click_safety():
    """Test that PyAutoGUI failsafe works."""
    print("\n" + "=" * 60)
    print("TEST 5: Safety features")
    print("=" * 60)

    print(f"✓ PyAutoGUI Failsafe: {pyautogui.FAILSAFE}")
    print("  Move mouse to top-left corner to stop automation")
    print(f"✓ PyAutoGUI Pause: {pyautogui.PAUSE}s between actions")

    return True


def interactive_test():
    """Interactive test mode - find a button on current screen."""
    print("\n" + "=" * 60)
    print("INTERACTIVE TEST: Find button on screen")
    print("=" * 60)

    templates_dir = Path("templates")
    templates = sorted([f.name for f in templates_dir.glob("*.png")])

    print("\nAvailable templates:")
    for i, template in enumerate(templates, 1):
        print(f"{i:2d}. {template}")

    try:
        choice = input("\nEnter template number to search for (or 'q' to quit): ").strip()
        if choice.lower() == 'q':
            return

        idx = int(choice) - 1
        if idx < 0 or idx >= len(templates):
            print("Invalid choice")
            return

        template = templates[idx]
        print(f"\nSearching for: {template}")
        print("Switch to game window now! Searching in 3 seconds...")

        import time
        time.sleep(3)

        matcher = ImageMatcher(confidence=0.7)
        result = matcher.find_on_screen(f"templates/{template}")

        if result:
            x, y, w, h = result
            center_x = x + w // 2
            center_y = y + h // 2
            print(f"✓ Found at position ({x}, {y}), size ({w}x{h})")
            print(f"  Center point: ({center_x}, {center_y})")
            print(f"  Would click here if automation was running")
        else:
            print("❌ Not found on current screen")
            print("   Try:")
            print("   - Lowering confidence in config.yaml")
            print("   - Making sure the button is visible")
            print("   - Checking if screen resolution matches examples")

    except (ValueError, KeyboardInterrupt):
        print("\nTest cancelled")


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("UMAMUSUME AUTOPLAY - TEST SUITE")
    print("=" * 60)
    print()

    # Run tests
    tests_passed = 0
    tests_total = 5

    if test_templates_exist():
        tests_passed += 1

    if test_screenshot():
        tests_passed += 1

    if test_click_safety():
        tests_passed += 1

    if test_screen_detection():
        tests_passed += 1

    if test_template_matching():
        tests_passed += 1

    # Summary
    print("\n" + "=" * 60)
    print(f"TESTS COMPLETE: {tests_passed}/{tests_total} passed")
    print("=" * 60)

    if tests_passed == tests_total:
        print("\n✓ All tests passed! The automation should work.")
        print("\nNext steps:")
        print("1. Open the game to the home screen")
        print("2. Run: python umamusume_autoplay.py --sequence")
        print("   (This will start one training run)")
        print("3. Or run: python umamusume_autoplay.py --continuous")
        print("   (This will keep automating until you stop it)")
    else:
        print("\n⚠️  Some tests failed. Fix issues before running automation.")

    # Interactive test option
    print("\n" + "=" * 60)
    choice = input("\nRun interactive button finder? (y/n): ").strip().lower()
    if choice == 'y':
        interactive_test()


if __name__ == "__main__":
    main()
