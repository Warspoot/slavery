"""Screen detection for different Umamusume game states."""

from enum import Enum
from typing import Optional, Tuple
from pathlib import Path
from image_utils import ImageMatcher


class GameScreen(Enum):
    """Enum for different game screens."""
    HOME_SCREEN = "home_screen"
    SUPPORT_CARD_SELECTION = "support_card_selection"
    TRAINING_PREP = "training_prep"
    EVENT_BANNER = "event_banner"
    MY_RULER_CONFIRM = "my_ruler_confirm"
    MAIN_GAME = "main_game"
    AUTO_PLAY_IN_PROGRESS = "auto_play_in_progress"  # Game is in auto-play mode, wait until it's done
    TP_RECOVERY_CONFIRM = "tp_recovery_confirm"
    TP_RECOVERY_ITEMS = "tp_recovery_items"
    ITEM_QUANTITY = "item_quantity"
    EVENT_SKIP_SETTINGS = "event_skip_settings"
    FAST_FORWARD_BUTTON = "fast_forward_button"
    OMAKASE_MENU = "omakase_menu"
    RACE_RETRY = "race_retry"
    RACE_COMPLETION = "race_completion"
    TRAINING_COMPLETE = "training_complete"
    POST_TRAINING_COMPLETE = "post_training_complete"
    FACTOR_CONFIRM = "factor_confirm"
    POST_TRAINING_NEXT = "post_training_next"
    UNKNOWN = "unknown"


class ScreenDetector:
    """Detects which screen is currently displayed."""

    def __init__(self, templates_dir: str = "templates", confidence: float = 0.8):
        """
        Initialize the screen detector.

        Args:
            templates_dir: Directory containing template images
            confidence: Confidence threshold for image matching
        """
        self.templates_dir = Path(templates_dir)
        self.matcher = ImageMatcher(confidence)

        # Template mappings for each screen
        self.screen_templates = {
            GameScreen.AUTO_PLAY_IN_PROGRESS: ["auto_play_inprogress.png"],  # Must check FIRST - blocks all input
            GameScreen.HOME_SCREEN: [],  # TODO: Add home screen templates
            GameScreen.SUPPORT_CARD_SELECTION: [],  # TODO: Add support card selection templates
            GameScreen.TRAINING_PREP: ["training_start_banner.png"],
            GameScreen.EVENT_BANNER: [],  # TODO: Add event banner templates
            GameScreen.MY_RULER_CONFIRM: ["kettei_button.png"],
            GameScreen.TP_RECOVERY_CONFIRM: ["kaifuku_button.png"],  # TP recovery confirmation dialog
            GameScreen.TP_RECOVERY_ITEMS: ["tp_recovery_header.png"],  # Items list - detected by header (static)
            GameScreen.ITEM_QUANTITY: [],  # TODO: Add item quantity templates
            GameScreen.EVENT_SKIP_SETTINGS: [],  # TODO: Add event skip templates
            GameScreen.FAST_FORWARD_BUTTON: ["fast_forward.png"],
            GameScreen.OMAKASE_MENU: ["omakase_button.png"],
            GameScreen.RACE_RETRY: ["mouichido_button.png"],
            GameScreen.RACE_COMPLETION: ["tojiru_button.png"],
            GameScreen.TRAINING_COMPLETE: ["training_complete_button.png"],
            GameScreen.POST_TRAINING_COMPLETE: ["kanryou_suru_button.png"],
            GameScreen.FACTOR_CONFIRM: ["inshi_kakutei_button.png"],
            GameScreen.POST_TRAINING_NEXT: ["tsugi_e_corner.png"],
        }

    def detect_current_screen(
        self,
        region: Optional[Tuple[int, int, int, int]] = None
    ) -> GameScreen:
        """
        Detect which screen is currently displayed.
        Checks dialogs/popups first, then background screens.

        Args:
            region: Optional region to search

        Returns:
            The detected GameScreen
        """
        # Clear screenshot cache to get fresh screenshot for this detection cycle
        self.matcher.clear_cache()

        # FIRST: Check if auto-play is in progress (must wait until it's done)
        auto_play_template = str(self.templates_dir / "auto_play_inprogress.png")
        if self.matcher.find_on_screen(auto_play_template, region):
            return GameScreen.AUTO_PLAY_IN_PROGRESS

        # Priority order: Check dialogs/popups FIRST before background screens
        priority_screens = [
            GameScreen.POST_TRAINING_NEXT,   # 次へ button (post-training)
            GameScreen.FACTOR_CONFIRM,       # 因子確定 button
            GameScreen.POST_TRAINING_COMPLETE,  # 完了する button (post-training)
            GameScreen.TRAINING_COMPLETE,    # 育成完了 button (training end)
            GameScreen.TP_RECOVERY_CONFIRM,  # TP recovery confirmation dialog (回復する button) - CHECK BEFORE TRAINING PREP
            GameScreen.TRAINING_PREP,        # 育成開始 button - CHECK BEFORE OMAKASE (both visible at same time)
            # GameScreen.MY_RULER_CONFIRM,     # 決定/キャンセル dialog - DISABLED (unreliable)
            GameScreen.TP_RECOVERY_ITEMS,    # TP items screen - check before RACE_COMPLETION (has 閉じる button)
            GameScreen.ITEM_QUANTITY,        # Item quantity dialog
            GameScreen.RACE_RETRY,           # もう一度 button - check BEFORE 閉じる
            GameScreen.RACE_COMPLETION,      # 閉じる dialog - moved after TP recovery screens
            GameScreen.EVENT_SKIP_SETTINGS,  # Event skip settings
            GameScreen.OMAKASE_MENU,         # Omakase menu - checked AFTER training prep
            GameScreen.EVENT_BANNER,         # Event banner popup
            GameScreen.FAST_FORWARD_BUTTON,  # Fast forward during race
        ]

        # Background screens (checked last)
        background_screens = [
            GameScreen.SUPPORT_CARD_SELECTION,
            GameScreen.HOME_SCREEN,
            GameScreen.MAIN_GAME,
        ]

        # Check priority screens first
        for screen in priority_screens:
            if screen in self.screen_templates:
                for template in self.screen_templates[screen]:
                    template_path = str(self.templates_dir / template)
                    if self.matcher.find_on_screen(template_path, region):
                        # Special validation for TP_RECOVERY_ITEMS to avoid false positives
                        if screen == GameScreen.TP_RECOVERY_ITEMS:
                            # Only accept if the 閉じる button is also present (unique to TP screen)
                            tojiru_path = str(self.templates_dir / "tojiru_button.png")
                            if not self.matcher.find_on_screen(tojiru_path, region):
                                continue  # False positive, skip this detection
                        return screen

        # Then check background screens
        for screen in background_screens:
            if screen in self.screen_templates:
                for template in self.screen_templates[screen]:
                    template_path = str(self.templates_dir / template)
                    if self.matcher.find_on_screen(template_path, region):
                        return screen

        return GameScreen.UNKNOWN

    def is_screen(
        self,
        screen: GameScreen,
        region: Optional[Tuple[int, int, int, int]] = None
    ) -> bool:
        """
        Check if the current screen matches the specified type.

        Args:
            screen: The screen type to check for
            region: Optional region to search

        Returns:
            True if the screen matches, False otherwise
        """
        if screen not in self.screen_templates:
            return False

        for template in self.screen_templates[screen]:
            template_path = str(self.templates_dir / template)
            if self.matcher.find_on_screen(template_path, region):
                return True

        return False

    def wait_for_screen(
        self,
        screen: GameScreen,
        timeout: int = 10,
        check_interval: float = 0.5,
        region: Optional[Tuple[int, int, int, int]] = None
    ) -> bool:
        """
        Wait for a specific screen to appear.

        Args:
            screen: The screen type to wait for
            timeout: Maximum time to wait in seconds
            check_interval: Time between checks in seconds
            region: Optional region to search

        Returns:
            True if screen appeared within timeout, False otherwise
        """
        import time

        elapsed = 0
        while elapsed < timeout:
            if self.is_screen(screen, region):
                return True

            time.sleep(check_interval)
            elapsed += check_interval

        return False
