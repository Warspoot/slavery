"""Color-based button detection for dynamic buttons."""

import cv2
import numpy as np
from typing import Optional, Tuple
from image_utils import take_screenshot


def find_pink_button(region: Optional[Tuple[int, int, int, int]] = None) -> Optional[Tuple[int, int]]:
    """
    Find the pink training complete button by color.

    Args:
        region: Optional search region

    Returns:
        (x, y) center coordinates if found, None otherwise
    """
    # Take screenshot
    screenshot = take_screenshot(region=region)
    screenshot_np = np.array(screenshot)
    screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

    # Convert to HSV for color detection
    hsv = cv2.cvtColor(screenshot_cv, cv2.COLOR_BGR2HSV)

    # Pink color range (adjust these if needed)
    lower_pink = np.array([140, 50, 150])   # Lower bound for pink
    upper_pink = np.array([170, 255, 255])  # Upper bound for pink

    # Create mask for pink areas
    mask = cv2.inRange(hsv, lower_pink, upper_pink)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None

    # Find the largest pink area (likely the button)
    largest_contour = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(largest_contour)

    # Minimum size check (button should be reasonably large)
    if area < 1000:  # Adjust threshold as needed
        return None

    # Get center of the contour
    M = cv2.moments(largest_contour)
    if M["m00"] == 0:
        return None

    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])

    # Adjust for region offset
    if region:
        cx += region[0]
        cy += region[1]

    return (cx, cy)
