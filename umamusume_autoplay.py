#!/usr/bin/env python3
"""Main automation script for Umamusume Pretty Derby autoplay."""

import time
import yaml
import signal
import sys
from pathlib import Path
from typing import Dict, Any
from pynput import keyboard

from automation import ButtonClicker
from screen_detector import ScreenDetector, GameScreen
from image_utils import save_screenshot


# Global flag for graceful shutdown
_should_stop = False
_hotkey_listener = None


def on_stop_hotkey():
    """Called when stop hotkey (Esc) is pressed."""
    global _should_stop
    if not _should_stop:
        _should_stop = True
        print("\n\n⚠️  Stop hotkey pressed - will stop after current action...")
        print("Press Esc again to force quit immediately")
    else:
        print("\n\n⚠️  Force quitting...")
        sys.exit(0)


def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully."""
    global _should_stop
    _should_stop = True
    print("\n\n⚠️  Stop signal received - will stop after current action...")
    print("Press Ctrl+C again to force quit immediately")

    # Second Ctrl+C will force quit
    signal.signal(signal.SIGINT, signal.SIG_DFL)


class UmamusumeAutoplay:
    """Main automation controller for Umamusume Pretty Derby."""

    def __init__(self, config_path: str = "config.yaml"):
        """
        Initialize the autoplay automation.

        Args:
            config_path: Path to the configuration file
        """
        self.config = self._load_config(config_path)

        confidence = self.config.get("confidence_threshold", 0.8)
        action_delay = self.config.get("action_delay", 1.0)

        self.clicker = ButtonClicker(
            templates_dir="templates",
            confidence=confidence,
            action_delay=action_delay
        )

        self.detector = ScreenDetector(
            templates_dir="templates",
            confidence=confidence
        )

        self.max_retries = self.config.get("max_retries", 5)
        self.retry_delay = self.config.get("retry_delay", 2.0)
        self.screen_change_delay = self.config.get("screen_change_delay", 1.5)
        self.cooldown_time = self.config.get("cooldown_time", 2.0)
        self.unknown_screen_delay = self.config.get("unknown_screen_delay", 0.5)
        self.debug = self.config.get("debug", False)
        self.search_region = self.config.get("search_region", None)

        # TP recovery position offsets (configurable per screen)
        self.tp_recovery_row_y = self.config.get("tp_recovery_second_row_y", 195)
        self.tp_recovery_button_x = self.config.get("tp_recovery_button_x", 350)
        self.auto_recover_tp = self.config.get("auto_recover_tp", False)

        print("Umamusume Autoplay initialized")
        print(f"Confidence threshold: {confidence}")
        print(f"Action delay: {action_delay}s")
        print(f"Debug mode: {self.debug}")
        print(f"Auto TP recovery: {self.auto_recover_tp}")

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            print(f"Config file not found: {config_path}, using defaults")
            return {}
        except Exception as e:
            print(f"Error loading config: {e}, using defaults")
            return {}

    def _debug_screenshot(self, prefix: str):
        """Save a debug screenshot if debug mode is enabled."""
        if self.debug:
            # Create debug directory if it doesn't exist
            debug_dir = Path("debug_screenshots")
            debug_dir.mkdir(exist_ok=True)

            timestamp = time.strftime("%Y%m%d_%H%M%S")
            filename = debug_dir / f"debug_{prefix}_{timestamp}.png"
            save_screenshot(str(filename), self.search_region)

    def handle_home_screen(self) -> bool:
        """
        Handle the home screen.
        Clicks the 育成 (training) button.

        Returns:
            True if handled successfully
        """
        print("Handling home screen...")
        self._debug_screenshot("home_screen")

        # TODO: Add home screen template
        print("⚠️  Home screen detection not yet implemented with new templates")
        return False

    def handle_support_card_selection(self) -> bool:
        """
        Handle the support card selection screen.
        Clicks the 決定 (confirm) button.

        Returns:
            True if handled successfully
        """
        print("Handling support card selection...")
        self._debug_screenshot("support_cards")

        # TODO: Add support card selection template
        print("⚠️  Support card selection not yet implemented with new templates")
        return False

    def handle_training_prep(self) -> bool:
        """
        Handle the training preparation screen.
        Clicks the 育成開始 (start training) button.

        Returns:
            True if handled successfully
        """
        print("Handling training preparation...")
        self._debug_screenshot("training_prep")

        # Try multiple button templates (button appears in different forms)
        button_templates = [
            "training_育成開始_button.png",
            "training_start_button_small.png",
        ]

        for template in button_templates:
            if self.clicker.click_button_with_retry(
                template,
                max_retries=self.max_retries,
                retry_delay=self.retry_delay,
                region=self.search_region
            ):
                return True

        print("⚠️  Could not find any training start button")
        return False

    def handle_event_banner(self) -> bool:
        """
        Handle event banner popup.
        Clicks the close button.

        Returns:
            True if handled successfully
        """
        print("Handling event banner...")
        self._debug_screenshot("event_banner")

        # TODO: Add event banner close template
        print("⚠️  Event banner close not yet implemented with new templates")
        return False

    def handle_my_ruler_confirm(self) -> bool:
        """
        Handle the 'My Ruler' confirmation dialog.
        Clicks the 決定 (confirm) button.

        Returns:
            True if handled successfully
        """
        print("Handling My Ruler confirmation...")
        self._debug_screenshot("my_ruler")

        return self.clicker.click_button_with_retry(
            "kettei_button.png",
            max_retries=self.max_retries,
            retry_delay=self.retry_delay,
            region=self.search_region
        )

    def handle_tp_recovery_confirm(self) -> bool:
        """
        Handle the TP recovery confirmation dialog.
        Clicks the 回復する (recover) button if auto_recover_tp is enabled.
        Otherwise, clicks cancel to skip TP recovery.

        Returns:
            True if handled successfully
        """
        print("Handling TP recovery confirmation...")
        self._debug_screenshot("tp_confirm")

        if not self.auto_recover_tp:
            print("⚠️  Auto TP recovery DISABLED - clicking cancel to skip")
            print("   (Set auto_recover_tp: true in config.yaml to enable)")
            # Click cancel button instead
            return self.clicker.click_button_with_retry(
                # TODO: Add cancel button template
                # "cancel_button.png",
                max_retries=self.max_retries,
                retry_delay=self.retry_delay,
                region=self.search_region
            )

        print("✓ Auto TP recovery ENABLED - clicking 回復する")
        return self.clicker.click_button_with_retry(
            "kaifuku_button.png",
            max_retries=self.max_retries,
            retry_delay=self.retry_delay,
            region=self.search_region
        )

    def handle_tp_recovery_items(self) -> bool:
        """
        Handle the TP recovery items screen.
        IMPORTANT: Always selects the BOTTLE (タフネス30) which is the SECOND option in the list.

        Returns:
            True if handled successfully
        """
        print("Handling TP recovery items selection...")
        print("⚠️  Clicking SECOND item (BOTTLE - タフネス30) by position")
        self._debug_screenshot("tp_items")

        # The TP recovery items screen has a consistent layout:
        # Each item row is approximately 90 pixels tall
        # We'll click the "使う" button for the SECOND row (bottle)

        if self.search_region:
            # Use search region coordinates with configurable offsets
            region_x, region_y, region_w, region_h = self.search_region

            # Use configured offsets (can be adjusted in config.yaml)
            click_x = region_x + self.tp_recovery_button_x
            click_y = region_y + self.tp_recovery_row_y
        else:
            # Fallback - shouldn't reach here if search_region is set
            print("⚠️ No search region defined, using fallback coordinates")
            click_x = 3000
            click_y = 1200

        print(f"Clicking 使う button for second item at ({click_x}, {click_y})")
        print(f"  Using offsets: X={self.tp_recovery_button_x}, Y={self.tp_recovery_row_y}")
        print(f"  (Adjust these in config.yaml if button position is wrong)")
        self.clicker.click_at_position(click_x, click_y)
        return True

    def handle_item_quantity(self) -> bool:
        """
        Handle the item quantity selection screen.
        Clicks OK to confirm the quantity.

        Returns:
            True if handled successfully
        """
        print("Handling item quantity confirmation...")
        self._debug_screenshot("item_quantity")

        return self.clicker.click_button_with_retry(
            # TODO: Add OK button template
            # "ok_button.png",
            max_retries=self.max_retries,
            retry_delay=self.retry_delay,
            region=self.search_region
        )

    def handle_event_skip_settings(self) -> bool:
        """
        Handle the event skip settings screen.
        Selects 'Skip all events' option and confirms.

        Returns:
            True if handled successfully
        """
        print("Handling event skip settings...")
        self._debug_screenshot("event_skip")

        # Click on "すべてのイベントを短縮" (skip all events)
        if self.clicker.click_button_with_retry(
            # TODO: Add skip all events template
            # "skip_all_events.png",
            max_retries=self.max_retries,
            retry_delay=self.retry_delay,
            region=self.search_region
        ):
            # Wait a bit and then click the 決定 button
            time.sleep(0.5)
            return self.clicker.click_button_with_retry(
                "kettei_button.png",
                max_retries=self.max_retries,
                retry_delay=self.retry_delay,
                region=self.search_region
            )

        return False

    def handle_fast_forward(self) -> bool:
        """
        Handle clicking the fast forward button during races.
        Clicks the >> button.

        Returns:
            True if handled successfully
        """
        print("Handling fast forward...")
        self._debug_screenshot("fast_forward")

        return self.clicker.click_button_with_retry(
            "fast_forward.png",
            max_retries=2,  # Don't retry too much for this
            retry_delay=0.5,
            region=self.search_region
        )

    def handle_omakase_menu(self) -> bool:
        """
        Handle the omakase (auto-select) menu.
        Clicks the おまかせ button itself.

        Returns:
            True if handled successfully
        """
        print("Handling omakase menu...")
        self._debug_screenshot("omakase")

        # Click the おまかせ button
        return self.clicker.click_button_with_retry(
            "omakase_button.png",
            max_retries=self.max_retries,
            retry_delay=self.retry_delay,
            region=self.search_region
        )

    def handle_race_completion(self) -> bool:
        """
        Handle the race completion dialog.
        Clicks the 閉じる (close) button.

        Returns:
            True if handled successfully
        """
        print("Handling race completion...")
        self._debug_screenshot("race_completion")

        return self.clicker.click_button_with_retry(
            "tojiru_button.png",
            max_retries=self.max_retries,
            retry_delay=self.retry_delay,
            region=self.search_region
        )

    def handle_training_complete(self) -> bool:
        """
        Handle the training complete screen.
        Clicks the 育成完了 button.

        Returns:
            True if handled successfully
        """
        print("Handling training complete...")
        self._debug_screenshot("training_complete")

        return self.clicker.click_button_with_retry(
            "training_complete_button.png",
            max_retries=self.max_retries,
            retry_delay=self.retry_delay,
            region=self.search_region
        )

    def handle_post_training_complete(self) -> bool:
        """
        Handle the post-training complete button.
        Clicks the 完了する button.

        Returns:
            True if handled successfully
        """
        print("Handling post-training complete...")
        self._debug_screenshot("post_training_complete")

        return self.clicker.click_button_with_retry(
            "kanryou_suru_button.png",
            max_retries=self.max_retries,
            retry_delay=self.retry_delay,
            region=self.search_region
        )

    def handle_factor_confirm(self) -> bool:
        """
        Handle the factor/inheritance confirmation.
        Clicks the 因子確定 button.

        Returns:
            True if handled successfully
        """
        print("Handling factor confirmation...")
        self._debug_screenshot("factor_confirm")

        return self.clicker.click_button_with_retry(
            "inshi_kakutei_button.png",
            max_retries=self.max_retries,
            retry_delay=self.retry_delay,
            region=self.search_region
        )

    def handle_post_training_next(self) -> bool:
        """
        Handle the post-training next button.
        Clicks the 次へ button.

        Returns:
            True if handled successfully
        """
        print("Handling post-training next...")
        self._debug_screenshot("post_training_next")

        # Try multiple button templates (button appears in different forms)
        button_templates = [
            "tsugi_e_button.png",
            "tsugi_e_corner.png",
        ]

        for template in button_templates:
            if self.clicker.click_button_with_retry(
                template,
                max_retries=self.max_retries,
                retry_delay=self.retry_delay,
                region=self.search_region
            ):
                return True

        print("⚠️  Could not find any 次へ button")
        return False

    def run_automation_sequence(self) -> bool:
        """
        Run the full automation sequence to start autoplay.

        Returns:
            True if sequence completed successfully
        """
        print("\n" + "=" * 50)
        print("Starting Umamusume Autoplay Automation")
        print("=" * 50 + "\n")
        print("Press Ctrl+C to stop at any time\n")

        time.sleep(2)  # Give user time to prepare

        sequence = [
            (GameScreen.EVENT_BANNER, self.handle_event_banner, True),  # Optional
            (GameScreen.HOME_SCREEN, self.handle_home_screen, False),
            (GameScreen.SUPPORT_CARD_SELECTION, self.handle_support_card_selection, True),  # Optional
            (GameScreen.TRAINING_PREP, self.handle_training_prep, False),
            (GameScreen.MY_RULER_CONFIRM, self.handle_my_ruler_confirm, True),  # Optional

            # TP Recovery - only appears if TP is empty
            (GameScreen.TP_RECOVERY_CONFIRM, self.handle_tp_recovery_confirm, True),  # Optional - only if TP empty
            (GameScreen.TP_RECOVERY_ITEMS, self.handle_tp_recovery_items, True),  # Optional - selects BOTTLE (2nd item)
            (GameScreen.ITEM_QUANTITY, self.handle_item_quantity, True),  # Optional - confirms quantity

            (GameScreen.EVENT_SKIP_SETTINGS, self.handle_event_skip_settings, False),
        ]

        for screen_type, handler, optional in sequence:
            print(f"\nWaiting for screen: {screen_type.value}")

            # Wait for the screen to appear
            if self.detector.wait_for_screen(
                screen_type,
                timeout=30,
                check_interval=0.5,
                region=self.search_region
            ):
                print(f"Screen detected: {screen_type.value}")

                # Handle the screen
                if not handler():
                    if not optional:
                        print(f"Failed to handle required screen: {screen_type.value}")
                        return False
                    else:
                        print(f"Failed to handle optional screen: {screen_type.value}")

                print(f"Successfully handled: {screen_type.value}")
            else:
                if optional:
                    print(f"Screen {screen_type.value} did not appear (optional)")
                else:
                    print(f"Required screen {screen_type.value} did not appear - continuing anyway")

        print("\n" + "=" * 50)
        print("Automation sequence completed!")
        print("=" * 50 + "\n")
        return True

    def run_continuous(self):
        """
        Run the automation continuously.
        This will keep detecting and handling screens in a loop.
        """
        global _should_stop, _hotkey_listener

        # Set up signal handler for graceful shutdown
        signal.signal(signal.SIGINT, signal_handler)

        # Set up global hotkey listener (works even when game window is focused)
        _hotkey_listener = keyboard.GlobalHotKeys({
            '<esc>': on_stop_hotkey
        })
        _hotkey_listener.start()

        print("\n" + "=" * 50)
        print("Starting Continuous Automation Mode")
        print("=" * 50 + "\n")
        print("This mode will automatically handle:")
        print("  - Training flow (home → support → prep → skip settings)")
        print("  - TP recovery (ONLY when prompted - uses BOTTLE/タフネス30)")
        print("  - Race fast forward and completion")
        print("  - Training completion and post-training flow")
        print("  - Omakase menus")
        print()
        print("⚠️  STOP AUTOMATION:")
        print("  - Press ESC key once for graceful stop (finishes current action)")
        print("  - Press ESC twice to force quit immediately")
        print("  - Or press Ctrl+C in terminal\n")

        try:
            last_action = None
            last_action_time = 0
            unknown_screen_count = 0

            while True:
                # Check for stop signal
                if _should_stop:
                    print("\n✓ Stopping automation gracefully...")
                    break

                current_screen = self.detector.detect_current_screen(self.search_region)

                # Prevent spam-clicking the same screen
                current_time = time.time()

                if current_screen == GameScreen.UNKNOWN:
                    unknown_screen_count += 1
                    if unknown_screen_count % 5 == 0:  # Log every 5 unknown screens
                        print(f"Waiting for recognized screen... ({unknown_screen_count})")
                    time.sleep(self.unknown_screen_delay)
                    continue
                else:
                    unknown_screen_count = 0

                if current_screen == last_action and (current_time - last_action_time) < self.cooldown_time:
                    # Same screen within cooldown, skip to prevent loops
                    time.sleep(0.3)
                    continue

                action_taken = False
                print(f"\n[{current_screen.value}] detected")

                if current_screen == GameScreen.AUTO_PLAY_IN_PROGRESS:
                    # Auto-play is active - wait until it finishes
                    print("⏸️  Auto-play in progress - waiting...")
                    time.sleep(1.0)  # Wait 1 second before checking again
                    action_taken = True  # Mark as action taken to avoid unknown screen delay
                elif current_screen == GameScreen.POST_TRAINING_NEXT:
                    # Post-training flow - 次へ button
                    self.handle_post_training_next()
                    action_taken = True
                elif current_screen == GameScreen.FACTOR_CONFIRM:
                    # Factor/inheritance confirmation
                    self.handle_factor_confirm()
                    action_taken = True
                elif current_screen == GameScreen.POST_TRAINING_COMPLETE:
                    # Post-training complete - 完了する button
                    self.handle_post_training_complete()
                    action_taken = True
                elif current_screen == GameScreen.TRAINING_COMPLETE:
                    # Training complete - 育成完了 button
                    self.handle_training_complete()
                    action_taken = True
                elif current_screen == GameScreen.RACE_COMPLETION:
                    # Prioritize race completion (閉じる button)
                    self.handle_race_completion()
                    action_taken = True
                elif current_screen == GameScreen.FAST_FORWARD_BUTTON:
                    self.handle_fast_forward()
                    action_taken = True
                elif current_screen == GameScreen.EVENT_BANNER:
                    self.handle_event_banner()
                    action_taken = True
                elif current_screen == GameScreen.HOME_SCREEN:
                    self.handle_home_screen()
                    action_taken = True
                elif current_screen == GameScreen.SUPPORT_CARD_SELECTION:
                    self.handle_support_card_selection()
                    action_taken = True
                elif current_screen == GameScreen.TRAINING_PREP:
                    self.handle_training_prep()
                    action_taken = True
                elif current_screen == GameScreen.MY_RULER_CONFIRM:
                    self.handle_my_ruler_confirm()
                    action_taken = True
                elif current_screen == GameScreen.TP_RECOVERY_CONFIRM:
                    self.handle_tp_recovery_confirm()  # Will click cancel if auto_recover_tp is False
                    action_taken = True
                elif current_screen == GameScreen.TP_RECOVERY_ITEMS:
                    if self.auto_recover_tp:
                        self.handle_tp_recovery_items()
                        action_taken = True
                    else:
                        print("⚠️  Skipping TP recovery items (auto_recover_tp is False)")
                        time.sleep(0.5)
                elif current_screen == GameScreen.ITEM_QUANTITY:
                    if self.auto_recover_tp:
                        self.handle_item_quantity()
                        action_taken = True
                    else:
                        print("⚠️  Skipping item quantity (auto_recover_tp is False)")
                        time.sleep(0.5)
                elif current_screen == GameScreen.EVENT_SKIP_SETTINGS:
                    self.handle_event_skip_settings()
                    action_taken = True
                elif current_screen == GameScreen.OMAKASE_MENU:
                    self.handle_omakase_menu()
                    action_taken = True
                else:
                    # Unknown screen, wait a bit
                    time.sleep(1)

                if action_taken:
                    last_action = current_screen
                    last_action_time = current_time
                    print(f"Action completed, waiting for next screen...")
                    time.sleep(self.screen_change_delay)

        except KeyboardInterrupt:
            print("\n\nAutomation stopped by user")
        finally:
            # Clean up hotkey listener
            if _hotkey_listener:
                _hotkey_listener.stop()
            print("✓ Automation stopped")


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Umamusume Pretty Derby Autoplay Automation"
    )
    parser.add_argument(
        "--config",
        default="config.yaml",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--continuous",
        action="store_true",
        help="Run in continuous mode (keeps monitoring and clicking)"
    )
    parser.add_argument(
        "--sequence",
        action="store_true",
        help="Run the full sequence once"
    )

    args = parser.parse_args()

    autoplay = UmamusumeAutoplay(args.config)

    if args.continuous:
        autoplay.run_continuous()
    elif args.sequence:
        autoplay.run_automation_sequence()
    else:
        print("Please specify --continuous or --sequence mode")
        print("Use --help for more information")


if __name__ == "__main__":
    main()
