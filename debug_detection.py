#!/usr/bin/env python3
"""Debug tool to see what templates are matching and where."""

import yaml
import sys
from pathlib import Path
from screen_detector import ScreenDetector, GameScreen
from image_utils import ImageMatcher, take_screenshot
import cv2
import numpy as np

def main():
    """Debug screen detection."""

    # Load config
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    confidence = config.get('confidence_threshold', 0.8)
    search_region = config.get('search_region', None)

    print("=" * 70)
    print("SCREEN DETECTION DEBUG TOOL")
    print("=" * 70)
    print()
    print(f"Confidence threshold: {confidence}")
    print(f"Search region: {search_region}")
    print()
    print("This tool will:")
    print("1. Take a screenshot of your current game screen")
    print("2. Test ALL templates against it")
    print("3. Show which templates match and their confidence scores")
    print("4. Save a visualization with match locations")
    print()

    input("Make sure the game is visible, then press ENTER...")
    print()

    # Initialize detector and matcher
    detector = ScreenDetector(confidence=confidence)
    matcher = ImageMatcher(confidence=confidence)

    # Take screenshot
    print("Taking screenshot...")
    screenshot = take_screenshot(region=search_region)
    screenshot_np = np.array(screenshot)
    screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

    # Save screenshot
    cv2.imwrite('debug_current_screen.png', screenshot_cv)
    print(f"✓ Saved screenshot to: debug_current_screen.png")
    print()

    # Convert screenshot to grayscale for matching
    screenshot_gray = cv2.cvtColor(screenshot_cv, cv2.COLOR_BGR2GRAY)

    # Test all templates
    templates_dir = Path("templates")
    all_templates = sorted(templates_dir.glob("*.png"))

    print("=" * 70)
    print("TESTING ALL TEMPLATES (MULTI-METHOD MATCHING)")
    print("=" * 70)
    print()

    matches = []

    for template_path in all_templates:
        template_name = template_path.name

        # Load template
        template = cv2.imread(str(template_path))
        if template is None:
            continue

        # Convert template to grayscale
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        # Try multiple matching methods
        methods_results = []

        # Method 1: Grayscale
        result_gray = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        _, max_val_gray, _, max_loc_gray = cv2.minMaxLoc(result_gray)
        methods_results.append(('gray', max_val_gray, max_loc_gray))

        # Method 2: Color
        result_color = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
        _, max_val_color, _, max_loc_color = cv2.minMaxLoc(result_color)
        methods_results.append(('color', max_val_color, max_loc_color))

        # Method 3: Edges
        screenshot_edges = cv2.Canny(screenshot_gray, 50, 150)
        template_edges = cv2.Canny(template_gray, 50, 150)
        result_edges = cv2.matchTemplate(screenshot_edges, template_edges, cv2.TM_CCOEFF_NORMED)
        _, max_val_edges, _, max_loc_edges = cv2.minMaxLoc(result_edges)
        methods_results.append(('edges', max_val_edges, max_loc_edges))

        # Use best result
        best_method, max_val, max_loc = max(methods_results, key=lambda x: x[1])

        # Check if it matches
        matched = max_val >= confidence

        status = "✓ MATCH" if matched else "✗ no match"
        color = "\033[92m" if matched else "\033[91m"
        reset = "\033[0m"

        # Show which method worked best and all scores
        method_scores = f"[G:{max_val_gray:.2f} C:{max_val_color:.2f} E:{max_val_edges:.2f}]"
        print(f"{color}{status}{reset} {template_name:40s} best: {best_method:5s} {max_val:.3f} {method_scores}")

        if matched:
            matches.append({
                'name': template_name,
                'confidence': max_val,
                'location': max_loc,
                'size': (template.shape[1], template.shape[0])
            })

    print()
    print("=" * 70)
    print("MATCHES SUMMARY")
    print("=" * 70)
    print()

    if not matches:
        print("No templates matched! Try lowering confidence_threshold in config.yaml")
    else:
        print(f"Found {len(matches)} matching templates:")
        print()

        # Sort by confidence
        matches.sort(key=lambda x: x['confidence'], reverse=True)

        for i, match in enumerate(matches, 1):
            print(f"{i}. {match['name']}")
            print(f"   Confidence: {match['confidence']:.3f}")
            print(f"   Location: {match['location']}")
            print()

        # Create visualization
        print("Creating visualization...")
        vis = screenshot_cv.copy()

        colors = [
            (0, 255, 0),    # Green
            (255, 0, 0),    # Blue
            (0, 0, 255),    # Red
            (255, 255, 0),  # Cyan
            (255, 0, 255),  # Magenta
            (0, 255, 255),  # Yellow
        ]

        for i, match in enumerate(matches):
            x, y = match['location']
            w, h = match['size']
            color = colors[i % len(colors)]

            # Draw rectangle
            cv2.rectangle(vis, (x, y), (x + w, y + h), color, 3)

            # Add label
            label = f"{i+1}. {match['name'][:20]}"
            cv2.putText(vis, label, (x, y - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        cv2.imwrite('debug_matches_visualization.png', vis)
        print(f"✓ Saved visualization to: debug_matches_visualization.png")
        print()

    # Detect current screen
    print("=" * 70)
    print("SCREEN DETECTOR RESULT")
    print("=" * 70)
    print()

    detected = detector.detect_current_screen(region=search_region)
    print(f"Detected screen: {detected.value}")
    print()

    if detected == GameScreen.UNKNOWN:
        print("⚠️  Screen not recognized!")
        print()
        print("Possible causes:")
        print("1. No templates matched with sufficient confidence")
        print("2. Game is on an unsupported screen")
        print("3. Confidence threshold is too high")
        print()
        print("Try:")
        print("- Lower confidence_threshold in config.yaml")
        print("- Add templates for this screen")
        print("- Check that templates were extracted correctly")

    print()
    print("=" * 70)
    print("FILES CREATED")
    print("=" * 70)
    print()
    print("1. debug_current_screen.png - Your current screen")
    print("2. debug_matches_visualization.png - Visualization of all matches")
    print()
    print("Open these images to see what the automation is detecting!")
    print()

if __name__ == "__main__":
    main()
