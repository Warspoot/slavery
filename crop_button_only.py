#!/usr/bin/env python3
"""Crop just the white button part from fast_forward.png to improve matching."""

from PIL import Image

# Load the current template
img = Image.open("templates/fast_forward.png")

# The white circle button is roughly in the center
# Let's crop to just the white circle with the icon
# Based on the image, the button appears to be around 60x60 in the center

width, height = img.size
print(f"Original size: {width}x{height}")

# Crop to center circle (adjust these values if needed)
# Typically the button circle is in the center
button_size = 60
left = (width - button_size) // 2
top = (height - button_size) // 2
right = left + button_size
bottom = top + button_size

cropped = img.crop((left, top, right, bottom))

# Save
cropped.save("templates/fast_forward_button_only.png")
print(f"Saved cropped button: templates/fast_forward_button_only.png")
print(f"New size: {cropped.size[0]}x{cropped.size[1]}")

# Keep the original as backup
img.save("templates/fast_forward_with_bg.png")
print("Original saved as: templates/fast_forward_with_bg.png")
