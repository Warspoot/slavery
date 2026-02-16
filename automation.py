"""Button clicking and automation actions."""

import time
import pyautogui
from typing import Optional, Tuple
from pathlib import Path
from image_utils import ImageMatcher


class ButtonClicker:
    """Handles button clicking automation."""

    def __init__(
        self,
        templates_dir: str = "templates",
        confidence: float = 0.8,
        action_delay: float = 1.0
    ):
        """
        Initialize the button clicker.

        Args:
            templates_dir: Directory containing button template images
            confidence: Confidence threshold for image matching
            action_delay: Delay after each action in seconds
        """
        self.templates_dir = Path(templates_dir)
        self.matcher = ImageMatcher(confidence)
        self.action_delay = action_delay

        # PyAutoGUI settings
        pyautogui.PAUSE = 0.05  # Reduced from 0.1 for faster clicks
        pyautogui.FAILSAFE = False  # Disabled - use Ctrl+C instead (more reliable)

    def click_button(
        self,
        button_template: str,
        region: Optional[Tuple[int, int, int, int]] = None,
        wait_after: Optional[float] = None
    ) -> bool:
        """
        Find and click a button.

        Args:
            button_template: Filename of the button template
            region: Optional region to search
            wait_after: Optional wait time after clicking (uses action_delay if None)

        Returns:
            True if button was found and clicked, False otherwise
        """
        template_path = str(self.templates_dir / button_template)
        center = self.matcher.find_center(template_path, region)

        if center:
            x, y = center
            print(f"Clicking button '{button_template}' at ({x}, {y})")
            pyautogui.click(x, y)

            # Wait after action
            wait_time = wait_after if wait_after is not None else self.action_delay
            time.sleep(wait_time)
            return True

        print(f"Button '{button_template}' not found")
        return False

    def click_at_position(
        self,
        x: int,
        y: int,
        wait_after: Optional[float] = None
    ):
        """
        Click at a specific position.

        Args:
            x: X coordinate
            y: Y coordinate
            wait_after: Optional wait time after clicking
        """
        print(f"Clicking at position ({x}, {y})")
        pyautogui.click(x, y)

        wait_time = wait_after if wait_after is not None else self.action_delay
        time.sleep(wait_time)

    def click_button_with_retry(
        self,
        button_template: str,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        region: Optional[Tuple[int, int, int, int]] = None,
        quick_fail: bool = False
    ) -> bool:
        """
        Try to click a button with retries.

        Args:
            button_template: Filename of the button template
            max_retries: Maximum number of retry attempts
            retry_delay: Delay between retries in seconds
            region: Optional region to search
            quick_fail: If True, only tries once (no retries)

        Returns:
            True if button was clicked, False if all retries failed
        """
        attempts = 1 if quick_fail else max_retries

        for attempt in range(attempts):
            # Clear cache before each attempt to get fresh screenshot
            self.matcher.clear_cache()

            if self.click_button(button_template, region, wait_after=0):
                time.sleep(self.action_delay)
                return True

            if attempt < attempts - 1:
                print(f"Retry {attempt + 1}/{attempts} after {retry_delay}s...")
                time.sleep(retry_delay)

        if quick_fail:
            print(f"Button '{button_template}' not found (quick fail)")
        else:
            print(f"Failed to click button '{button_template}' after {attempts} attempts")
        return False

    def wait_and_click(
        self,
        button_template: str,
        timeout: int = 10,
        check_interval: float = 0.5,
        region: Optional[Tuple[int, int, int, int]] = None
    ) -> bool:
        """
        Wait for a button to appear and then click it.

        Args:
            button_template: Filename of the button template
            timeout: Maximum time to wait in seconds
            check_interval: Time between checks in seconds
            region: Optional region to search

        Returns:
            True if button was found and clicked, False otherwise
        """
        template_path = str(self.templates_dir / button_template)
        match = self.matcher.wait_for_image(
            template_path,
            timeout=timeout,
            check_interval=check_interval,
            region=region
        )

        if match:
            x, y, w, h = match
            center_x = x + w // 2
            center_y = y + h // 2
            print(f"Button '{button_template}' appeared, clicking at ({center_x}, {center_y})")
            pyautogui.click(center_x, center_y)
            time.sleep(self.action_delay)
            return True

        print(f"Button '{button_template}' did not appear within {timeout}s")
        return False
