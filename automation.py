"""Button clicking automation for Umamusume."""

import time
import pyautogui
from typing import Optional, Tuple
from pathlib import Path
from image_utils import ImageMatcher


class ButtonClicker:
    """Handles clicking buttons on screen."""

    def __init__(self, templates_dir: str = "templates", confidence: float = 0.8, action_delay: float = 1.0):
        """
        Initialize the button clicker.

        Args:
            templates_dir: Directory containing template images
            confidence: Confidence threshold for image matching
            action_delay: Delay after each click
        """
        self.templates_dir = Path(templates_dir)
        self.matcher = ImageMatcher(confidence)
        self.action_delay = action_delay

        # Set PyAutoGUI settings
        pyautogui.FAILSAFE = True  # Move mouse to top-left corner to abort
        pyautogui.PAUSE = 0.1

    def click_button_with_retry(
        self,
        template_name: str,
        max_retries: int = 5,
        retry_delay: float = 2.0,
        region: Optional[Tuple[int, int, int, int]] = None
    ) -> bool:
        """
        Find and click a button, with retries.

        Args:
            template_name: Name of the template image file
            max_retries: Maximum number of retry attempts
            retry_delay: Delay between retries in seconds
            region: Optional region to search

        Returns:
            True if button was found and clicked, False otherwise
        """
        template_path = str(self.templates_dir / template_name)

        for attempt in range(max_retries):
            # Clear cache for fresh screenshot
            self.matcher.clear_cache()

            # Find the button
            center = self.matcher.find_center(template_path, region)

            if center:
                x, y = center
                print(f"  Clicking {template_name} at ({x}, {y})")
                pyautogui.click(x, y)
                time.sleep(self.action_delay)
                return True

            if attempt < max_retries - 1:
                print(f"  Button not found, retrying... ({attempt + 1}/{max_retries})")
                time.sleep(retry_delay)

        print(f"  ✗ Failed to find {template_name} after {max_retries} attempts")
        return False

    def click_at_position(self, x: int, y: int):
        """
        Click at a specific screen position.

        Args:
            x: X coordinate
            y: Y coordinate
        """
        pyautogui.click(x, y)
        time.sleep(self.action_delay)
