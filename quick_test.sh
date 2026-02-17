#!/usr/bin/env fish
# Quick test for color detection debugging

source venv/bin/activate.fish

echo "=== Running debug_detection.py ==="
echo "" | python debug_detection.py 2>&1 | tail -30

echo ""
echo "=== Check output files ==="
ls -lh debug*.png 2>/dev/null