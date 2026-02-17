# How to Debug Color Detection

## The Issue
You're seeing GREEN areas being detected when you expect different behavior.

## Why This Happens
Looking at your screenshot:
- Large bright green UI elements (training button, progress bars)
- The color detection is picking up these green areas
- Pink detection might not be working if there's no sufficiently large pink area

## Debug Steps

### 1. Test Pink Button Detection
```bash
source venv/bin/activate
./debug_color_detection.py
```

This will:
- Show all pink contours found
- Display their sizes
- Show which one would be selected as the "button"
- Create visualization files

### 2. Test All Color Ranges
```bash
source venv/bin/activate
./debug_all_colors.py
```

This will:
- Test pink, green, bright_green, blue, cyan detection
- Show you exactly what areas match each color range
- Create separate mask and visualization files for each color

### 3. Analyze Output Files

After running the scripts, check these files:
- `debug_color_mask_pink.png` - White areas show detected pink
- `debug_color_mask_green.png` - White areas show detected green
- `debug_color_visualization.png` - Annotated with contours
- `debug_all_colors_combined.png` - All colors overlaid

## Understanding The Results

### If green areas are huge:
The green UI elements (training button, progress bars) are being detected.
This is EXPECTED based on your screenshot.

### If you want to detect a specific button:
You need to either:
1. **Narrow the HSV range** to be more selective
2. **Add position filtering** (only look in specific area)
3. **Add size constraints** (filter by min/max area)
4. **Use template matching instead** for that specific button

## Fixing Color Detection

### Option 1: Adjust HSV Range
In [color_detection.py](color_detection.py:28-29), change:
```python
lower_pink = np.array([140, 50, 150])   # More restrictive
upper_pink = np.array([170, 255, 255])  # More restrictive
```

### Option 2: Add Region Filter
Only look in bottom half of screen, or specific button area.

### Option 3: Use Template Matching
For consistent buttons like "育成開始" (Training Start), template matching
is more reliable than color detection.

## Common Issues

1. **"Why is green detected?"**
   - Because there ARE large green elements in your screenshot
   - This is normal behavior

2. **"Pink not detected"**
   - Check if pink areas are large enough (>1000 pixels)
   - Check if HSV range matches your pink color
   - Run debug_color_detection.py to see actual pink mask

3. **"Wrong button selected"**
   - Color detection picks the LARGEST matching area
   - Add position/size filters to be more specific