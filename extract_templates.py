#!/usr/bin/env python3
"""Copy manually cropped button templates from examples/button templates/."""

import shutil
from pathlib import Path


def main():
    """Copy all button templates from examples/button templates/ to templates/."""

    # Create templates directory
    templates_dir = Path("templates")
    templates_dir.mkdir(exist_ok=True)

    # Source directory with manually cropped buttons
    button_templates_dir = Path("examples/button templates")

    if not button_templates_dir.exists():
        print(f"ERROR: {button_templates_dir} not found!")
        print("Make sure you have the 'button templates' folder in examples/")
        return

    # Template mappings from your manual crops to the expected names
    # Format: (source_filename, destination_filename, description)
    template_mappings = [
        # Critical: Bottle templates (ALWAYS use second option - タフネス30)
        ("bottle.png", "bottle_item.png", "Bottle item (タフネス30) - SECOND option in list"),
        ("bottle use.png", "bottle_use_button.png", "Use button (使う) for bottle"),

        # Main flow buttons
        ("pasted file.png", "training_育成開始_button.png", "Training start button (育成開始)"),
        ("Screenshot_20260203_120128.png", "ketteyi_button.png", "Confirm button (決定)"),
        ("Screenshot_20260216_121911.png", "home_育成_button.png", "Home screen training button (育成)"),
        ("Screenshot_20260216_135144.png", "home_育成_campaign_button.png", "Home screen training button with campaign (育成)"),

        # Support card and prep
        ("pasted file (1).png", "support_決定_button.png", "Support card confirm (決定)"),
        ("pasted file (2).png", "training_header.png", "Training prep header"),

        # Event skip
        ("pasted file (4).png", "skip_all_events.png", "Skip all events option"),
        ("pasted file (5).png", "event_skip_決定.png", "Event skip confirm (決定)"),

        # Race and fast forward
        ("pasted file (3).png", "fast_forward.png", "Fast forward button"),
        ("pasted file (6).png", "tojiru_button.png", "Close button (閉じる) - old"),
        ("Screenshot_20260216_134847.png", "tojiru_button.png", "Close button (閉じる) - updated"),

        # Omakase
        ("pasted file (7).png", "omakase_button.png", "Omakase button"),
        ("pasted file (8).png", "omakase_confirm.png", "Omakase confirm"),

        # TP Recovery flow
        ("Screenshot_20260203_114657.png", "kaifuku_button.png", "TP recovery button (回復する)"),
        ("tp_recovery_header.png", "tp_recovery_header.png", "TP recovery screen header (TP回復)"),
        ("Screenshot_20260203_114706.png", "tp_recovery_items_screen.png", "TP recovery items screen"),
        ("Screenshot_20260203_114722.png", "ok_button.png", "OK button"),

        # Cancel/close buttons
        ("Screenshot_20260203_104644.png", "cancel_button.png", "Cancel button (キャンセル)"),

        # Event banner
        ("Screenshot_20260216_121819.png", "event_banner_close.png", "Event banner close"),

        # Additional screens
        ("Screenshot_20260203_111718.png", "main_game_screen.png", "Main game screen"),

        # Training complete - text only (character artwork varies)
        ("pasted file (9).png", "training_complete_button.png", "Training complete button (育成完了)"),

        # Post-training flow
        ("Screenshot_20260216_143102.png", "kanryou_suru_full_button.png", "Complete button with artwork (完了する)"),
        ("Screenshot_20260216_143118.png", "kanryou_suru_button.png", "Complete button text only (完了する)"),
        ("Screenshot_20260216_143149.png", "inshi_kakutei_button.png", "Factor/inheritance confirm (因子確定)"),
        ("Screenshot_20260216_143219.png", "tsugi_e_button.png", "Next button (次へ)"),
    ]

    print("=" * 70)
    print("EXTRACTING MANUALLY CROPPED BUTTON TEMPLATES")
    print("=" * 70)
    print()
    print("⚠️  IMPORTANT: The automation will ALWAYS use the BOTTLE (タフネス30)")
    print("   which is the SECOND option in the TP recovery items list.")
    print()

    copied_count = 0
    missing_count = 0

    for source_name, dest_name, description in template_mappings:
        source_path = button_templates_dir / source_name
        dest_path = templates_dir / dest_name

        if source_path.exists():
            shutil.copy2(source_path, dest_path)
            # Get image dimensions
            from PIL import Image
            with Image.open(dest_path) as img:
                width, height = img.size
            print(f"✓ {dest_name:40} ({width:4}x{height:<4}) - {description}")
            copied_count += 1
        else:
            print(f"✗ MISSING: {source_name:30} -> {dest_name}")
            missing_count += 1

    print()
    print("=" * 70)
    print(f"EXTRACTION COMPLETE")
    print("=" * 70)
    print(f"✓ Copied: {copied_count} templates")
    if missing_count > 0:
        print(f"✗ Missing: {missing_count} templates")
    print()
    print(f"Templates saved to: {templates_dir.absolute()}/")
    print()

    if missing_count == 0:
        print("✓ All templates extracted successfully!")
        print()
        print("Next steps:")
        print("  1. python test_automation.py          - Test the setup")
        print("  2. python umamusume_autoplay.py --sequence  - Run automation")
    else:
        print("⚠️  Some templates are missing. Check the button templates folder.")


if __name__ == "__main__":
    main()
