"""Image recognition utilities for Umamusume automation."""

import cv2
import numpy as np
import pyautogui
import os
from typing import Optional, Tuple
from pathlib import Path


def take_screenshot(region: Optional[Tuple[int, int, int, int]] = None):
    """
    Take a screenshot with Wayland support.

    Args:
        region: Optional region (x, y, width, height)

    Returns:
        PIL Image object
    """
    # Check if running on Wayland
    session_type = os.environ.get('XDG_SESSION_TYPE', '').lower()

    if session_type == 'wayland':
        # Try to use grim for Wayland
        try:
            from wayland_screenshot import take_screenshot_wayland
            img = take_screenshot_wayland(region)
            if img:
                return img
        except ImportError:
            pass

    # Fall back to pyautogui (works on X11)
    return pyautogui.screenshot(region=region)


class ImageMatcher:
    """Handles image matching and screen recognition."""

    def __init__(self, confidence: float = 0.8):
        """
        Initialize the image matcher.

        Args:
            confidence: Minimum confidence threshold for matches (0.0 to 1.0)
        """
        self.confidence = confidence
        self._screenshot_cache = None
        self._cache_region = None

    def clear_cache(self):
        """Clear the screenshot cache."""
        self._screenshot_cache = None
        self._cache_region = None

    def _get_screenshot(self, region: Optional[Tuple[int, int, int, int]] = None):
        """
        Get screenshot with caching support.

        Args:
            region: Optional region to capture

        Returns:
            OpenCV format screenshot (BGR)
        """
        # Check if we can use cached screenshot
        if self._screenshot_cache is not None and self._cache_region == region:
            return self._screenshot_cache

        # Take new screenshot
        screenshot = take_screenshot(region=region)
        screenshot_np = np.array(screenshot)
        screenshot_cv = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)

        # Cache it
        self._screenshot_cache = screenshot_cv
        self._cache_region = region

        return screenshot_cv

    def find_on_screen(
        self,
        template_path: str,
        region: Optional[Tuple[int, int, int, int]] = None,
        grayscale: bool = True
    ) -> Optional[Tuple[int, int, int, int]]:
        """
        Find a template image on the screen.

        Args:
            template_path: Path to the template image
            region: Optional region to search (x, y, width, height)
            grayscale: Whether to use grayscale matching

        Returns:
            Tuple of (x, y, width, height) if found, None otherwise
        """
        try:
            # Get screenshot (cached if available)
            screenshot_cv = self._get_screenshot(region)

            # Load template
            template = cv2.imread(template_path)
            if template is None:
                raise ValueError(f"Could not load template: {template_path}")

            # Convert to grayscale if needed
            if grayscale:
                screenshot_cv = cv2.cvtColor(screenshot_cv, cv2.COLOR_BGR2GRAY)
                template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

            # Perform template matching
            result = cv2.matchTemplate(screenshot_cv, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            # Check if confidence threshold is met
            if max_val >= self.confidence:
                x, y = max_loc
                h, w = template.shape[:2]

                # Adjust coordinates if region was specified
                if region:
                    x += region[0]
                    y += region[1]

                return (x, y, w, h)

            return None

        except Exception as e:
            print(f"Error finding image: {e}")
            return None

    def find_center(
        self,
        template_path: str,
        region: Optional[Tuple[int, int, int, int]] = None,
        grayscale: bool = True
    ) -> Optional[Tuple[int, int]]:
        """
        Find the center point of a template image on screen.

        Args:
            template_path: Path to the template image
            region: Optional region to search
            grayscale: Whether to use grayscale matching

        Returns:
            Tuple of (center_x, center_y) if found, None otherwise
        """
        match = self.find_on_screen(template_path, region, grayscale)
        if match:
            x, y, w, h = match
            center_x = x + w // 2
            center_y = y + h // 2
            return (center_x, center_y)
        return None

    def wait_for_image(
        self,
        template_path: str,
        timeout: int = 10,
        check_interval: float = 0.5,
        region: Optional[Tuple[int, int, int, int]] = None
    ) -> Optional[Tuple[int, int, int, int]]:
        """
        Wait for an image to appear on screen.

        Args:
            template_path: Path to the template image
            timeout: Maximum time to wait in seconds
            check_interval: Time between checks in seconds
            region: Optional region to search

        Returns:
            Match location if found within timeout, None otherwise
        """
        import time

        elapsed = 0
        while elapsed < timeout:
            match = self.find_on_screen(template_path, region)
            if match:
                return match

            time.sleep(check_interval)
            elapsed += check_interval

        return None


def save_screenshot(filename: str, region: Optional[Tuple[int, int, int, int]] = None):
    """Save a screenshot for debugging purposes."""
    screenshot = take_screenshot(region=region)
    screenshot.save(filename)
    print(f"Screenshot saved: {filename}")
