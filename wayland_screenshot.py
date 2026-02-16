"""Wayland-compatible screenshot wrapper using grim."""

import subprocess
import tempfile
from pathlib import Path
from PIL import Image
from typing import Optional, Tuple


def take_screenshot_wayland(region: Optional[Tuple[int, int, int, int]] = None) -> Optional[Image.Image]:
    """
    Take a screenshot using grim (Wayland native).

    Args:
        region: Optional (x, y, width, height) tuple for cropping

    Returns:
        PIL Image object or None on failure
    """
    try:
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            tmp_path = tmp.name

        if region:
            # grim supports geometry: "x,y widthxheight"
            x, y, w, h = region
            geometry = f"{x},{y} {w}x{h}"
            cmd = ['grim', '-g', geometry, tmp_path]
        else:
            cmd = ['grim', tmp_path]

        result = subprocess.run(cmd, capture_output=True, check=True)

        # Load the image
        img = Image.open(tmp_path)

        # Clean up temp file
        Path(tmp_path).unlink()

        return img

    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error taking screenshot with grim: {e}")
        print("Make sure grim is installed: sudo pacman -S grim")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def test_grim():
    """Test if grim is available."""
    try:
        result = subprocess.run(['grim', '--help'],
                              capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


if __name__ == "__main__":
    print("Testing grim screenshot tool...")

    if not test_grim():
        print("❌ grim not found!")
        print("Install it with: sudo pacman -S grim")
    else:
        print("✓ grim is installed")

        print("\nTaking full screenshot...")
        img = take_screenshot_wayland()
        if img:
            img.save("test_wayland_full.png")
            print(f"✓ Saved test_wayland_full.png ({img.size[0]}x{img.size[1]})")

        print("\nTaking cropped screenshot (100, 100, 400, 300)...")
        img = take_screenshot_wayland((100, 100, 400, 300))
        if img:
            img.save("test_wayland_crop.png")
            print(f"✓ Saved test_wayland_crop.png ({img.size[0]}x{img.size[1]})")
