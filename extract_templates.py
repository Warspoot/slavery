#!/usr/bin/env python3
"""Copy all button templates from examples/button templates/ to templates/."""

import shutil
from pathlib import Path


def main():
    """Copy all .png files from examples/button templates/ to templates/."""

    # Create templates directory
    templates_dir = Path("templates")
    templates_dir.mkdir(exist_ok=True)

    # Source directory with manually cropped buttons
    button_templates_dir = Path("examples/button templates")

    if not button_templates_dir.exists():
        print(f"ERROR: {button_templates_dir} not found!")
        print("Make sure you have the 'button templates' folder in examples/")
        return

    print("=" * 70)
    print("EXTRACTING BUTTON TEMPLATES")
    print("=" * 70)
    print()
    print("Copying all .png files from examples/button templates/ to templates/")
    print()

    # Get all .png files from source directory
    template_files = sorted(button_templates_dir.glob("*.png"))

    if not template_files:
        print("✗ No .png files found in examples/button templates/")
        return

    copied_count = 0

    for source_path in template_files:
        dest_path = templates_dir / source_path.name

        try:
            shutil.copy2(source_path, dest_path)
            # Get image dimensions
            from PIL import Image
            with Image.open(dest_path) as img:
                width, height = img.size
            print(f"✓ {source_path.name:50} ({width:4}x{height:<4})")
            copied_count += 1
        except Exception as e:
            print(f"✗ ERROR copying {source_path.name}: {e}")

    print()
    print("=" * 70)
    print(f"EXTRACTION COMPLETE")
    print("=" * 70)
    print(f"✓ Copied: {copied_count} templates")
    print()
    print(f"Templates saved to: {templates_dir.absolute()}/")
    print()
    print("Next steps:")
    print("  1. python debug_detection.py     - Test template detection")
    print("  2. python umamusume_autoplay.py --continuous  - Run automation")


if __name__ == "__main__":
    main()
